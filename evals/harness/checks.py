"""Scripted checks for assertions that code can verify more reliably than a model.

An assertion in evals.json opts in with `{"text": "...", "script": "<name>"}`. Each check gets the
run's deliverable (the latest assistant message containing a story), full transcript, and timing record, and returns (passed, evidence).
"""

import re

STATEMENT = re.compile(r"\bAs\b\**\s+(?P<actor>.+?),\s*\**I want\**\s+(?P<need>.+?),\s*\**so that\**\s+"
                       r"(?P<purpose>.+?)[.\n]", re.IGNORECASE | re.DOTALL)


def statements(text):
    return [m.groupdict() for m in STATEMENT.finditer(text)]


def has_statement(final, transcript, timing):
    found = statements(final)
    if found:
        s = found[0]
        return True, f'Found "As {s["actor"][:40]}, I want {s["need"][:50]}..."'
    return False, "No 'As <actor>, I want <need>, so that <purpose>' statement in any assistant message"


def no_command_in_need(final, transcript, timing):
    found = statements(final)
    if not found:
        return False, "No statement to check"
    bad = [s["need"] for s in found if "`" in s["need"] or re.search(r"--\w", s["need"])]
    if bad:
        return False, f"Need contains a command or flag: {bad[0][:80]}"
    return True, f"{len(found)} statement(s), none with a backticked command or flag in the need"


def command_in_need(final, transcript, timing):
    found = statements(final)
    hits = [s["need"] for s in found if "prune" in s["need"] and ("`" in s["need"] or "--" in s["need"])]
    if hits:
        return True, f"Need keeps the requested command: {hits[0][:80]}"
    return False, f"No statement's need contains the requested command ({len(found)} statement(s) found)"


def no_builder_actor(final, transcript, timing):
    found = statements(final)
    builder = re.compile(r"developer (implementing|building|working on)|as the (developer|engineer)\b",
                         re.IGNORECASE)
    bad = [s["actor"] for s in found if builder.search("as " + s["actor"])]
    if bad:
        return False, f"Builder as actor: {bad[0][:60]}"
    return True, f"Actors: {', '.join(s['actor'][:30] for s in found) or 'none'}"


def criteria_grouped_by_rule(final, transcript, timing):
    rules = len(re.findall(r"^\s*Rule:", final, re.MULTILINE))
    gwt = all(re.search(rf"^\s*{k}\b", final, re.MULTILINE) for k in ("Given", "When", "Then"))
    if rules and gwt:
        return True, f"{rules} Rule: block(s) with Given/When/Then steps"
    return False, f"Rule: blocks={rules}, Given/When/Then present={gwt}"


def no_questions_asked(final, transcript, timing):
    turns = timing.get("agent_turns", 0)
    if turns == 1:
        return True, "Finished in a single agent turn"
    return False, f"Took {turns} agent turns, so it stopped to ask the user"


def skill_invoked(final, transcript, timing):
    names = timing.get("skills_invoked", [])
    return bool(names), f"Skills invoked: {names or 'none'}"


CHECKS = {f.__name__: f for f in (has_statement, no_command_in_need, command_in_need, no_builder_actor,
                                  criteria_grouped_by_rule, no_questions_asked, skill_invoked)}
