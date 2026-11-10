"""
Short script to launch an agent to summarise the results of the agent work found in runs/
"""
import subprocess
from pathlib import Path

summary_prompt = f"""Please look inside the subdirectory runs/.
There you will find a set of directories containing agent-generated methods to perform the task explained in AGENTS.md.
....
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
