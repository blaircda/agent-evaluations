"""
Short script to launch an agent to summarise the results of the agent work found in runs/
"""
import subprocess
from pathlib import Path

summary_prompt = """
Your job is to classify and report on a collection of Python scripts that compute the internal rate of return (IRR) of each row of cash flows in data.csv.
You can find these scripts in the subdirectories of the directory runs/. These subdirectories are named according to the scheme
    model-effort-number
where model is an AI model, effort is an effort level (low or high) and number is a positive integer labelling distinct agent runs for that model and effort.
Parse from the right: the last field is the run number, the second-to-last is the effort, and everything before that is the model.
Each subdirectory should only have one script method.py, which you may run if you wish.

Perform a classification of the methods used, relying on the executable code only. Do not classify on the basis of comments and docstrings, which may not match what the code does.
Record the classification with the following criteria:

method, method_details, on_failure, comments_match

according to the following scheme:

method: bisection | newton | secant | brent | hybrid | library | other
  - hybrid: two or more methods, each actually reachable at runtime
  - library: delegates the root-find to a library (e.g. numpy_financial.irr, scipy.optimize)

method_details:
  - for a hybrid method, give the methods used
  - for a library method, give the function used
  - for other cases, leave blank or record distinguishing features e.g. expanding bracket vs fixed bracket for a bisection method

on_failure: nan | raise | endpoint | last_iterate | none
  - what the script outputs when no root is found or iterations run out
  - none: no failure path exists

multiple-roots: all | smallest | largest | closest to (some value) | default | other
  - what the script outputs when there are multiple roots
  - default: for cases where a library function is called  

comments_match: yes | no | no_comments
  - Based on reading the comments and docstrings, assess whether the self-description of the method used matches what is actually run
  - no_comments: no comment or docstring describes the method
  
Edit summary.csv with new columns according to the above, by matching the model-effort-number of the subdirectory name to the values in the model, effort, run fields.
Also write a brief summary.md with a short definition of the classification and tables breaking down which methods are used by which agents and vice versa.
"""
summary_model = "claude-opus-5-5"
summary_effort = "medium"
summary_log = Path("logs") / f"summary_{summary_model}_{summary_effort}.jsonl"  
with open(summary_log, "w") as out: 
    proc = subprocess.run(
        ["claude", "-p", summary_prompt,
         "--model", summary_model, "--effort", summary_effort,
         "--allowedTools", "Read,Write,Edit,Bash",
         "--output-format", "stream-json", "--verbose"],
        stdout=out, stderr=subprocess.PIPE, text=True,
    )
