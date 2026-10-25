"""Shared helpers for the eval harness: paths, running `claude -p`, and JSON IO.

Every model call goes through the local `claude` CLI so evals run on the owner's Claude login. Runs
use `--setting-sources project` so the owner's global skills, plugins, and CLAUDE.md never leak in:
the only skill a run can see is the one copied into its fixture's `.claude/skills/`.
"""

import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SKILLS = REPO / "skills"
EVALS = REPO / "evals"
WORKSPACE = REPO / "workspace"

# One run can take several minutes when the agent explores a fixture, so the ceiling is generous.
CLAUDE_TIMEOUT_SECONDS = 900


def read_json(path):
    return json.loads(Path(path).read_text())


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def claude(prompt, cwd, *, tools, resume=None, system_prompt=None, append_system_prompt=None,
           json_schema=None, persist=True):
    """Run one headless `claude -p` turn and return its parsed JSON result."""
    cmd = ["claude", "-p", "--output-format", "json", "--setting-sources", "project",
           "--permission-mode", "dontAsk", "--tools", tools]
    if resume:
        cmd += ["--resume", resume]
    if system_prompt:
        cmd += ["--system-prompt", system_prompt]
    if append_system_prompt:
        cmd += ["--append-system-prompt", append_system_prompt]
    if json_schema:
        cmd += ["--json-schema", json.dumps(json_schema)]
    if not persist:
        cmd += ["--no-session-persistence"]
    proc = subprocess.run(cmd, input=prompt, cwd=cwd, capture_output=True, text=True,
                          timeout=CLAUDE_TIMEOUT_SECONDS)
    if proc.returncode != 0 and not proc.stdout.strip():
        raise RuntimeError(f"claude exited {proc.returncode}: {proc.stderr.strip()[:500]}")
    result = json.loads(proc.stdout)
    if result.get("is_error"):
        raise RuntimeError(f"claude reported an error: {str(result.get('result'))[:500]}")
    return result


def structured(result):
    """The structured output of a `--json-schema` run, whichever field the CLI put it in."""
    if isinstance(result.get("structured_output"), dict):
        return result["structured_output"]
    text = result.get("result", "").strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(text)


def total_tokens(result):
    usage = result.get("usage", {})
    return sum(usage.get(k, 0) for k in ("input_tokens", "output_tokens",
                                         "cache_creation_input_tokens", "cache_read_input_tokens"))
