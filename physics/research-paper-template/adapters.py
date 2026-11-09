"""
Adapters that turn Claude Code and Antigravity (Gemini) stream-json logs
into one common record, so both providers can share a summary.csv.

Each get_* function takes the list of parsed log events and returns
(texts, run_data):

    texts    : list of text blocks the agent wrote, in order
    run_data : dict with exactly the keys in RUN_FIELDS (None where unknown)
"""
import json
from collections import defaultdict

# Common columns to report 
RUN_FIELDS = [
    "status",           # "success" / "error" / ... (lowercased), None if the run never finished
    "n_results",        # number of 'result' events (>1 = agent was woken up again, e.g. background job)
    "model_calls",      # how many times the model generated a response
    "tool_calls",       # how many tool calls it made
    "model_seconds",    # time spent waiting on the model
    "input_fresh",      # input tokens processed at full price (incl. cache writes)
    "input_cached",     # input tokens read from cache (much cheaper)
    "output_tokens",    # everything generated, thinking included
    "thinking_tokens",  # the thinking part of output_tokens
    "final_text",       # the agent's final message
]

def read_events(log_path):
    """Parse a .jsonl log into a list of events, skipping blank lines"""
    return [json.loads(line)
            for line in log_path.read_text(encoding="utf-8").splitlines()
            if line.strip()]

def get_claude(events):
    """
    Extract Claude agent run data
    """
    texts, message_ids, tool_calls = [], set(), 0
    for ev in events:
        if ev.get("type") != "assistant":
            continue
        msg = ev.get("message", {})
        message_ids.add(msg.get("id")) # one model call can span several events
        for b in msg.get("content", []):
            if b.get("type") == "text":
                texts.append(b["text"])
            elif b.get("type") == "tool_use":
                tool_calls += 1

    results = [ev for ev in events if ev.get("type") == "result"]
    run_data = dict.fromkeys(RUN_FIELDS) # create dict with common fields
    run_data.update(model_calls=len(message_ids), tool_calls=tool_calls, n_results=len(results))
    if not results:
        return texts, run_data

    # sum usage and duration reported per run segment
    def total(key, sub=None):
        out = 0
        for r in results:
            usage = r.get("usage", {})
            if sub is None:
                value = usage.get(key, 0)
            else:
                inner = usage.get(sub) or {} # in case sub not in usage make sure return {} not None
                value = inner.get(key, 0)
            out += value
        return out

    run_data.update(
        status=(results[-1].get("subtype") or "").lower() or None,
        model_seconds=sum(r.get("duration_api_ms", 0) for r in results) / 1000,
        input_fresh=total("input_tokens") + total("cache_creation_input_tokens"),
        input_cached=total("cache_read_input_tokens"),
        output_tokens=total("output_tokens"),
        thinking_tokens=total("thinking_tokens", sub="output_tokens_details"),
        final_text=results[-1].get("result"),
    )
    return texts, run_data


def get_gemini(events):
    """
    Extract Gemini agent run data
    """
    deltas = defaultdict(list) # will store text_delta text fragments in a dict with keys step_index
    model_steps, tool_steps, results = [], [], []
    for ev in events:
        if ev.get("event") == "result":
            results.append(ev.get("result", {}))
            continue
        s = ev.get("step_update", {})
        if s.get("step_type") == "agent_response":
            if "text_delta" in s:
                deltas[s["step_index"]].append(s["text_delta"])
            if s.get("state") == "DONE":
                model_steps.append(s)
        elif s.get("step_type") == "tool" and s.get("state") == "DONE":
            tool_steps.append(s)

    texts = ["".join(parts) for _, parts in sorted(deltas.items())]
    run_data = dict.fromkeys(RUN_FIELDS)
    run_data.update(model_calls=len(model_steps),
                    tool_calls=len(tool_steps),
                    n_results=len(results),
                    model_seconds=sum(s.get("duration_seconds", 0) for s in model_steps))
    if not results:
        return texts, run_data

    def total(key):
        return sum(r.get("usage", {}).get(key, 0) for r in results)

    run_data.update(
        status=(results[-1].get("status") or "").lower() or None,
        input_fresh=total("input_tokens"), # Gemini reports cached tokens separately
        input_cached=total("cache_read_tokens"),
        output_tokens=total("output_tokens"),
        thinking_tokens=total("thinking_tokens"),
        final_text=results[-1].get("response"),
    )
    return texts, run_data

ADAPTERS = {"claude": get_claude, "gemini": get_gemini}

def summarise(log_path, family):
    return ADAPTERS[family](read_events(log_path))
