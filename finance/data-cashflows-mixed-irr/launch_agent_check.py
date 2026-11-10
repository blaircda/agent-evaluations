"""
Short script to verify the results of the agent work found in runs/
"""
import itertools, subprocess, shutil, filecmp, tempfile
from pathlib import Path
import numpy as np
from config import *

# open master results
#results = np.loadtxt("master_results.csv")
    
for model, effort, i in itertools.product(MODELS, EFFORTS, range(1, AGENTS + 1)):
    print(f"Checking {model} ({effort}) agent {i}")
    model_dir =  Path("runs") / f"{model}_{effort}_{i}" 
    result = model_dir / f"results.csv"

    # check agent results against master results
    #agent_results = np.loadtxt(result)
    #if (agent_results!=results).any():
    #    print("Discrepancy against master results")

    # check agent method reproduces agent results
    # by running method.py in a temporary directory
    # and comparing
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for f in ("method.py", "data.csv"):
            shutil.copy(model_dir / f, tmp)
        rerun = subprocess.run(["python3", "method.py"], cwd=tmp,
                               capture_output=True, text=True, timeout=120)
        regenerated = tmp / "results.csv"
        ok = regenerated.exists() and filecmp.cmp(regenerated, result, shallow=False)
        if not ok: # keep the evidence of a failure
            keep = model_dir / "verify_failed"
            shutil.copytree(tmp, keep)
            (keep / "stderr.txt").write_text(rerun.stderr)
            print(f"method.py does not reproduce results.csv for {model} {effort} {i}")
            print(f"Result of rerun saved to {keep}")
