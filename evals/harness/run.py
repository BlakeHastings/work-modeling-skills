"""Run a skill's evals with and without the skill, following agentskills.io's eval guide.

Each run is a conversation: the agent under test gets the eval prompt, and a simulated user (the
owner persona in evals/personas/owner.md) answers whatever the agent asks, until the persona says
the work is done or the turn limit is hit. The same persona answers both configurations, so the
only variable is the skill.

Usage:
    python3 -I evals/harness/run.py user-stories --iteration 1 [--eval NAME] [--jobs 4]
"""

import argparse
import json
import shutil
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import EVALS, SKILLS, WORKSPACE, claude, read_json, structured, total_tokens, write_json  # noqa: E402

CONFIGS = ("with_skill", "without_skill")
AGENT_TOOLS = "Skill,Read,Glob,Grep"
# Most stories settle in two or three exchanges; five leaves room for a full grilling round.
MAX_TURNS = 5

AGENT_NOTE = (
    "You are talking to the user through a text relay. You cannot write files: put everything you "
    "produce in your reply. If you need the user, ask in your reply and they will answer."
)

PERSONA_SCHEMA = {
    "type": "object",
    "properties": {
        "done": {"type": "boolean"},
        "reply": {"type": "string"},
    },
    "required": ["done", "reply"],
}


def persona_turn(persona, eval_case, transcript, cwd):
    prompt = (
        f"{persona}\n\n## What you asked for\n\n{eval_case['prompt']}\n\n"
        f"## The conversation so far\n\n{render(transcript)}\n\n"
        "## Your move\n\nIf the assistant has delivered what you asked for and is not waiting on "
        "you, set done to true and reply with an empty string. Otherwise set done to false and write "
        "your reply to the assistant's latest message, in character."
    )
    result = claude(prompt, cwd, tools="", json_schema=PERSONA_SCHEMA, persist=False)
    return structured(result), result


def render(transcript):
    return "\n\n".join(f"**{who}:**\n{text}" for who, text in transcript)


def skills_invoked(session):
    """Names of skills the agent invoked, read from the session transcript Claude Code saved."""
    names = []
    for path in (Path.home() / ".claude" / "projects").glob(f"*/{session}.jsonl"):
        for line in path.read_text().splitlines():
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            content = entry.get("message", {}).get("content")
            if not isinstance(content, list):
                continue
            for block in content:
                if block.get("type") == "tool_use" and block.get("name") == "Skill":
                    names.append(block.get("input", {}).get("skill", "?"))
    return names


def prepare_workdir(eval_case, config, skill_name, root):
    work = Path(tempfile.mkdtemp(prefix=f"{eval_case['name']}-{config}-", dir=root))
    for rel in eval_case.get("files", []):
        src = SKILLS / skill_name / rel
        if src.is_dir():
            shutil.copytree(src, work, dirs_exist_ok=True)
        else:
            shutil.copy2(src, work / src.name)
    if config == "with_skill":
        shutil.copytree(SKILLS / skill_name, work / ".claude" / "skills" / skill_name,
                        ignore=shutil.ignore_patterns("evals"))
    return work


def run_one(skill_name, eval_case, config, run, iteration, persona, scratch_root):
    out = (WORKSPACE / skill_name / f"iteration-{iteration}" / f"eval-{eval_case['name']}" / config
           / f"run-{run}")
    out.mkdir(parents=True, exist_ok=True)
    work = prepare_workdir(eval_case, config, skill_name, scratch_root)
    transcript, tokens, started = [("User", eval_case["prompt"])], 0, time.monotonic()
    session, message, turns = None, eval_case["prompt"], 0
    while turns < MAX_TURNS:
        result = claude(message, work, tools=AGENT_TOOLS, resume=session,
                        append_system_prompt=AGENT_NOTE)
        session, turns = result["session_id"], turns + 1
        tokens += total_tokens(result)
        transcript.append(("Assistant", result.get("result", "")))
        verdict, _ = persona_turn(persona, eval_case, transcript, work)
        if verdict["done"] or not verdict["reply"].strip():
            break
        message = verdict["reply"]
        transcript.append(("User", message))
    duration_ms = int((time.monotonic() - started) * 1000)
    (out / "outputs").mkdir(exist_ok=True)
    (out / "outputs" / "transcript.md").write_text(render(transcript) + "\n")
    (out / "outputs" / "final.md").write_text(transcript[-1][1] if transcript[-1][0] == "Assistant"
                                              else transcript[-2][1])
    write_json(out / "timing.json", {"total_tokens": tokens, "duration_ms": duration_ms,
                                     "agent_turns": turns, "session_id": session,
                                     "skills_invoked": skills_invoked(session),
                                     "workdir": str(work)})
    return f"{eval_case['name']}/{config}/run-{run}: {turns} turn(s), {tokens} tokens, {duration_ms / 1000:.0f}s"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("skill")
    parser.add_argument("--iteration", type=int, required=True)
    parser.add_argument("--eval", action="append", help="run only these eval names")
    parser.add_argument("--config", choices=CONFIGS, action="append")
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--runs", type=int, help="runs per eval (default: runs_per_eval in evals.json)")
    parser.add_argument("--include-unvalidated", action="store_true",
                        help="also run cases the owner has not validated")
    args = parser.parse_args()

    spec = read_json(SKILLS / args.skill / "evals" / "evals.json")
    persona = (EVALS / "personas" / "owner.md").read_text()
    cases = [e for e in spec["evals"] if (not args.eval or e["name"] in args.eval)
             and (e.get("validated") or args.include_unvalidated)]
    runs = args.runs or spec.get("runs_per_eval", 1)
    configs = args.config or CONFIGS
    scratch_root = Path(tempfile.mkdtemp(prefix=f"wms-{args.skill}-"))
    print(f"fixtures under {scratch_root}")

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = [pool.submit(run_one, args.skill, c, cfg, r, args.iteration, persona, scratch_root)
                   for c in cases for cfg in configs for r in range(1, runs + 1)]
        failed = 0
        for f in as_completed(futures):
            try:
                print(f.result(), flush=True)
            except Exception as exc:  # one broken run should not sink the batch
                failed += 1
                print(f"FAILED: {exc}", flush=True)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
