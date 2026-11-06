import itertools, shutil, subprocess, csv, json
from pathlib import Path
from config import *

def summarise(log_path):
    """Return the final 'result' event of a stream-json log."""
    for line in reversed(log_path.read_text().splitlines()):
        event = json.loads(line)
        if event.get("type") == "result":
            return event
    return {}  # if the run crashed before finishing

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
        # run claude in run directory
        # direct output to log file
        proc = subprocess.run(
            ["claude", "-p", f"Read AGENTS.md and follow it exactly.",
             "--model", model, "--effort", effort,
             "--allowedTools", "Read,Write,Edit,Bash",
             "--output-format", "stream-json", "--verbose"],
            cwd=active, stdout=out, stderr=subprocess.PIPE, text=True,
        )
    active.rename(final)
    print(f"{final.name}: exit {proc.returncode}")

    # record a summary of the log file 
    res = summarise(log)
    row = {
        "model": model, "effort": effort, "run": i,
        "exit": proc.returncode,
        "status": res.get("subtype"),
        "turns": res.get("num_turns"),
        "seconds": res.get("duration_ms", 0) / 1000,
        "cost_usd": res.get("total_cost_usd"),
        "output_tokens": res.get("usage", {}).get("output_tokens"),
    }
    summary = Path("summary.csv")
    new = not summary.exists()
    with open(summary, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=row.keys())
        if new:
            w.writeheader()
        w.writerow(row)
