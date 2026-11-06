import itertools, shutil, subprocess, csv, json
from pathlib import Path
from time import perf_counter
from config import *

def summarise(log_path):
    """
    Read a stream-json log and return (texts, run_data).

    texts    : every text block the agent wrote, in order
    run_data : totals across all 'result' events ({} if the run never finished)
    """
    events = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    texts = [
        b["text"]
        for ev in events if ev.get("type") == "assistant"
        for b in ev["message"].get("content", [])
        if b.get("type") == "text"
    ]

    results = [ev for ev in events if ev.get("type") == "result"]
    if not results:
        return texts, {}

    run_data = {
        "status":        results[-1].get("subtype"),
        "n_results":     len(results),
        "turns":         sum(r.get("num_turns", 0) for r in results),
        "api_seconds":   sum(r.get("duration_api_ms", 0) for r in results) / 1000,
        "cost_usd":      results[-1].get("total_cost_usd"),
        "output_tokens": sum(r.get("usage", {}).get("output_tokens", 0) for r in results),
    }
    
    return texts, run_data
    
for model, effort, i in itertools.product(MODELS, EFFORTS, range(1, AGENTS + 1)):
    log = Path("logs") / f"{model}_{effort}_{i}.jsonl"

    SANDBOX = Path.home() / "agent_sandbox"   
    active  = SANDBOX / "work"

    final  = Path("runs") / f"{model}_{effort}_{i}"

    if active.exists() or final.exists():
        raise SystemExit("leftover folder: clean up first")

    active.mkdir(parents=True)
    final.mkdir(parents=True)
    log.parent.mkdir(exist_ok=True) # create the parent logs directory
    
    for f in FILES: # copy the files into each run directiory
        shutil.copy(f, active)

    with open(log, "w") as out: # open the log file
        start = perf_counter()
        # run claude in run directory
        # direct output to log file
        proc = subprocess.run(
            ["claude", "-p", f"Read AGENTS.md and follow it exactly.",
             "--model", model, "--effort", effort,
             "--allowedTools", "Read,Write,Edit,Bash",
             "--output-format", "stream-json", "--verbose"],
            cwd=active, stdout=out, stderr=subprocess.PIPE, text=True,
        )
        elapsed = perf_counter() - start
    active.rename(final)
    print(f"{final.name}: exit {proc.returncode}")

    # record a summary of the log file 
    outputs, run_data = summarise(log)
    run_info = {"model": model, "effort": effort, "run": i,
        "exit": proc.returncode,
        "seconds": elapsed,
    }
    row = run_info | run_data
    summary = Path("summary.csv")
    new = not summary.exists()
    with open(summary, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=row.keys())
        if new:
            w.writeheader()
        w.writerow(row)
    summary_txt = Path("summary.csv")
    new = not summary_txt.exists()
    with open(summary_txt, "a", newline="") as f:
        f.write(f"\n===== {log} =====\n")
        for line in outputs:
            f.write(f"[Agent text output:] {line}\n")

summary_prompt = f"Please look inside the subdirectory runs/. There you will find a set of directories containing agent-generated report files on a scientific paper. Prepare a summary.tex here with a concise count of what each agent chose as success, drawback and next direction. Include tables breaking down what each agent chose by model and effort. Compile summary.tex to a pdf, delete the LaTeX auxiliary files that are produced."
summary_model = "claude-opus-5-5"
summary_effort = "medium"
summary_log = Path("logs") / f"summary_{summary_model}_{summary_effort}.jsonl"
with open(summary_log, "w") as out: 
    proc = subprocess.run(
        ["claude", "-p", summary_prompt,
         "--model", summary_model, "--effort", summary_effort,
         "--allowedTools", "Read,Write,Edit,Bash"
         ],
        stdout=out, stderr=subprocess.PIPE, text=True,
    )
