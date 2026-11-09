"""
Short script to launch an agent to summarise the results of the agent reports found in runs/
"""
import subprocess
from pathlib import Path

summary_prompt = f"In the directory runs/ you will find a set of directories containing agent-generated answers to an examination paper, which you can inspect in the current directory as exam.tex. Mark each paper according to the file solutions.tex in the current directory and record the results in a table format, saved as summary.tex. Also update summary.csv with a final column, header 'grade', with the score for each agent."
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
