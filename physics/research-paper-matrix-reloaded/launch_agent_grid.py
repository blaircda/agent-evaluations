"""
Script to launch a grid of multiple agents (sequentially)

using Claude and Gemini models via Claude code and Antigravity CLIs, i.e. claude -p, agy -p 

************
Makes use of:

config.py
----------
Specifies model, effort, number of agents and files to be given to the agents

adapters.py
-----------
Contains functions to extract information about Claude/Gemini agent runs from jsonl output logs

************
Functionality:

Loops over model, effort and agent number
Copies AGENTS.md and files into a `sandbox' working directory
Runs agent, copies final state of working directory back to a final directory in runs/
Records logs to logs/
Records a summary of the log to summary.csv, summary.txt
"""
import itertools, shutil, subprocess, csv, json
from pathlib import Path
from time import perf_counter
from config import *
from adapters import summarise, RUN_FIELDS

FIELDS = ["model", "effort", "run", "exit", "wall_seconds", *RUN_FIELDS]

for model, effort, i in itertools.product(MODELS, EFFORTS, range(1, AGENTS + 1)):
    log = Path("logs") / f"{model}_{effort}_{i}.jsonl"

    SANDBOX = Path.home() / "agent_sandbox"   
    active  = SANDBOX / "work"

    final  = Path("runs") / f"{model}_{effort}_{i}"

    if active.exists() or final.exists():
        raise SystemExit("leftover folder: clean up first")

    active.mkdir(parents=True)
    final.parent.mkdir(parents=True, exist_ok=True)   # makes sure runs/ exists
    log.parent.mkdir(exist_ok=True) # create the parent logs directory
    
    for f in FILES: # copy the files into each run directiory
        shutil.copy(f, active)

    with open(log, "w") as out: # open the log file
        # run agent in run directory
        # direct output to log file
        model_family = model.split('-')[0]
        
        start = perf_counter()
        if model_family == "claude":
            proc = subprocess.run(
                ["claude", "-p", f"Read AGENTS.md and follow it exactly.",
                 "--model", model, "--effort", effort,
                 "--allowedTools", "Read,Write,Edit,Bash",
                 "--output-format", "stream-json", "--verbose"],
                cwd=active, stdout=out, stderr=subprocess.PIPE, text=True,
            )
        elif model_family == "gemini":
            settings = {"permissions": {"allow": ["command(*)", "write_file(*)", "read_file(*)", "edit_file(*)"]}}
            proc = subprocess.run(
                ["agy", "-p", f"Read AGENTS.md and follow it exactly.",
                 "--model", f"{model}-{effort}",
                 "--settings", json.dumps(settings),
                 "--output-format", "stream-json"],
                cwd=active, stdout=out, stderr=subprocess.PIPE, text=True,
            )            
        elapsed = perf_counter() - start
    active.rename(final)
    print(f"{final.name}: exit {proc.returncode}")

    # record a summary of the log file 
    outputs, run_data = summarise(log, model_family)
    final_text = run_data.pop("final_text")
    row = {
        "model": model,
        "effort": effort,
        "run": i,
        "exit": proc.returncode,
        "wall_seconds": elapsed,
        **run_data
    }
    summary = Path("summary.csv")
    new = not summary.exists()
    with open(summary, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[k for k in FIELDS if k != "final_text"],
                   restval="", extrasaction="ignore")
        if new:
            w.writeheader()
        w.writerow(row)
    summary_txt = Path("summary.txt")
    new = not summary_txt.exists()
    with open(summary_txt, "a", newline="") as f:
        f.write(f"\n===== {log} =====\n")
        for line in outputs:
            f.write(f"[Agent text output:] {line}\n")
        #f.write(f"{final_text}\n")

