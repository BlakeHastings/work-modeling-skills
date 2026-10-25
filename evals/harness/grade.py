"""Grade every run in an iteration and write grading.json in the agentskills.io format.

Assertions with a `script` key are checked in code (checks.py); the rest go to a model grader that
must quote evidence for every PASS.

Usage:
    python3 -I evals/harness/grade.py user-stories --iteration 1 [--jobs 4]
"""

import argparse
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from checks import CHECKS  # noqa: E402
from common import SKILLS, WORKSPACE, claude, read_json, structured, write_json  # noqa: E402

GRADER_SCHEMA = {
    "type": "object",
    "properties": {
        "assertion_results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "passed": {"type": "boolean"},
                    "evidence": {"type": "string"},
                },
                "required": ["text", "passed", "evidence"],
            },
        },
    },
    "required": ["assertion_results"],
}

GRADER_PROMPT = """You are grading one run of an AI assistant against a list of assertions.

Rules:
- Grade each assertion PASS or FAIL from the conversation below, nothing else.
- Require concrete evidence for a PASS: quote or point to the specific text. Do not give the
  benefit of the doubt. A heading with no real substance under it is a FAIL.
- Judge what the assistant produced, not what it said it would do.
- Return one result per assertion, in the same order, with the assertion text copied exactly.

## Assertions

{assertions}

## Conversation

{transcript}
"""


def grade_run(run_dir, assertions, scratch):
    transcript = (run_dir / "outputs" / "transcript.md").read_text()
    final = (run_dir / "outputs" / "final.md").read_text()
    timing = read_json(run_dir / "timing.json")
    results = {}
    model_items = []
    for i, a in enumerate(assertions):
        if isinstance(a, dict) and a.get("script"):
            passed, evidence = CHECKS[a["script"]](final, transcript, timing)
            results[i] = {"text": a["text"], "passed": passed, "evidence": evidence}
        else:
            model_items.append((i, a["text"] if isinstance(a, dict) else a))
    if model_items:
        listed = "\n".join(f"{n + 1}. {text}" for n, (_, text) in enumerate(model_items))
        out = structured(claude(GRADER_PROMPT.format(assertions=listed, transcript=transcript),
                                scratch, tools="", json_schema=GRADER_SCHEMA, persist=False))
        graded = out["assertion_results"]
        for n, (i, text) in enumerate(model_items):
            r = graded[n] if n < len(graded) else {"passed": False, "evidence": "grader returned no result"}
            results[i] = {"text": text, "passed": bool(r["passed"]), "evidence": r["evidence"]}
    ordered = [results[i] for i in range(len(assertions))]
    passed = sum(r["passed"] for r in ordered)
    write_json(run_dir / "grading.json", {
        "assertion_results": ordered,
        "summary": {"passed": passed, "failed": len(ordered) - passed, "total": len(ordered),
                    "pass_rate": round(passed / len(ordered), 4) if ordered else 0.0},
    })
    return f"{run_dir.parent.parent.name}/{run_dir.parent.name}/{run_dir.name}: {passed}/{len(ordered)}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("skill")
    parser.add_argument("--iteration", type=int, required=True)
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()

    spec = read_json(SKILLS / args.skill / "evals" / "evals.json")
    by_name = {e["name"]: e for e in spec["evals"]}
    root = WORKSPACE / args.skill / f"iteration-{args.iteration}"
    scratch = tempfile.mkdtemp(prefix="wms-grade-")
    jobs = []
    for eval_dir in sorted(root.glob("eval-*")):
        case = by_name.get(eval_dir.name.removeprefix("eval-"))
        if not case:
            continue
        for run_dir in sorted(p for p in eval_dir.glob("*/run-*") if (p / "timing.json").exists()):
            jobs.append((run_dir, case.get("assertions", [])))
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for line in pool.map(lambda j: grade_run(j[0], j[1], scratch), jobs):
            print(line, flush=True)


if __name__ == "__main__":
    main()
