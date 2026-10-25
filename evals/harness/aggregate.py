"""Aggregate an iteration's grading and timing into benchmark.json and a readable benchmark.md.

Each eval runs several times per config, so every assertion gets a pass rate per config. Assertions
are then grouped the way the agentskills.io guide suggests: where the skill adds value, where it
regresses, and which assertions say nothing about the skill because they pass (or fail) everywhere.

Usage:
    python3 -I evals/harness/aggregate.py user-stories --iteration 1
"""

import argparse
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import WORKSPACE, read_json, write_json  # noqa: E402


def stats(values):
    if not values:
        return {"mean": 0.0, "stddev": 0.0}
    return {"mean": round(statistics.mean(values), 4),
            "stddev": round(statistics.stdev(values), 4) if len(values) > 1 else 0.0}


def rate(bools):
    return sum(bools) / len(bools) if bools else 0.0


def classify(w, wo):
    if w == 1 and wo == 1:
        return "Always passes (not discriminating)"
    if w == 0 and wo == 0:
        return "Always fails (check the assertion or the case)"
    if w > wo:
        return "Skill adds value"
    if w < wo:
        return "Skill regresses"
    return "No difference (mixed in both)"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("skill")
    parser.add_argument("--iteration", type=int, required=True)
    args = parser.parse_args()
    root = WORKSPACE / args.skill / f"iteration-{args.iteration}"

    per_config, per_eval, per_assertion = {}, {}, {}
    for run_dir in sorted(root.glob("eval-*/*/run-*")):
        if not (run_dir / "grading.json").exists():
            continue
        eval_name, cfg = run_dir.parent.parent.name, run_dir.parent.name
        grading, timing = read_json(run_dir / "grading.json"), read_json(run_dir / "timing.json")
        c = per_config.setdefault(cfg, {"pass_rate": [], "time_seconds": [], "tokens": []})
        c["pass_rate"].append(grading["summary"]["pass_rate"])
        c["time_seconds"].append(timing["duration_ms"] / 1000)
        c["tokens"].append(timing["total_tokens"])
        e = per_eval.setdefault((eval_name, cfg), {"pass_rate": [], "turns": [], "tokens": []})
        e["pass_rate"].append(grading["summary"]["pass_rate"])
        e["turns"].append(timing.get("agent_turns", 0))
        e["tokens"].append(timing["total_tokens"])
        for r in grading["assertion_results"]:
            per_assertion.setdefault((eval_name, r["text"]), {}).setdefault(cfg, []).append(r["passed"])

    summary = {cfg: {k: stats(v) for k, v in m.items()} for cfg, m in per_config.items()}
    if "with_skill" in summary and "without_skill" in summary:
        summary["delta"] = {k: round(summary["with_skill"][k]["mean"] - summary["without_skill"][k]["mean"], 4)
                            for k in ("pass_rate", "time_seconds", "tokens")}
    assertions = []
    for (name, text), res in per_assertion.items():
        w, wo = rate(res.get("with_skill", [])), rate(res.get("without_skill", []))
        assertions.append({"eval": name, "text": text, "with_skill": round(w, 4),
                           "without_skill": round(wo, 4), "group": classify(w, wo)})
    write_json(root / "benchmark.json", {"run_summary": summary, "assertions": assertions})

    lines = [f"# {args.skill}: iteration {args.iteration}", "",
             "| Eval | Config | Runs | Pass rate (mean ± sd) | Turns (mean) | Tokens (mean) |",
             "|---|---|---|---|---|---|"]
    for (name, cfg), m in sorted(per_eval.items()):
        pr = stats(m["pass_rate"])
        lines.append(f"| {name} | {cfg} | {len(m['pass_rate'])} | {pr['mean']:.2f} ± {pr['stddev']:.2f} | "
                     f"{statistics.mean(m['turns']):.1f} | {statistics.mean(m['tokens']):.0f} |")
    order = ["Skill adds value", "Skill regresses", "No difference (mixed in both)",
             "Always fails (check the assertion or the case)", "Always passes (not discriminating)"]
    for group in order:
        items = [a for a in assertions if a["group"] == group]
        lines += ["", f"## {group}", ""]
        lines += [f"- {a['eval']}: {a['text']} (with {a['with_skill']:.2f}, without {a['without_skill']:.2f})"
                  for a in items] or ["- none"]
    if "delta" in summary:
        d = summary["delta"]
        lines += ["", "## Delta (with minus without)", "",
                  f"pass rate {d['pass_rate']:+.2f}, seconds {d['time_seconds']:+.0f}, tokens {d['tokens']:+.0f}"]
    (root / "benchmark.md").write_text("\n".join(lines) + "\n")
    print((root / "benchmark.md").read_text())


if __name__ == "__main__":
    main()
