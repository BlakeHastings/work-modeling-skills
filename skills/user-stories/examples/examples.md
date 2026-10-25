# Examples

## Contents
- A full story: "Back up my sessions"
- Before and after: four items from a real backlog
- Routing examples: story, sub-task, enabler, spike, or epic

## A full story

~~~markdown
# Back up my sessions

**As** a multi-machine user, **I want** to run a CLI command that backs up every agent session on
this machine to my registry, **so that** my full history is in one place no matter which machine I
worked on.

**Epic:** My sessions are kept in one place

## Acceptance criteria

```gherkin
Rule: Every session on the machine is backed up

  Example: First backup on a machine
    Given I am signed in to my registry
    And this machine has 14 Claude Code sessions that have never been backed up
    When I back up my sessions from the CLI
    Then all 14 sessions are in my registry
    And I am told how many sessions and how much data were backed up

Rule: A session already backed up is never uploaded twice

  Example: Backing up again with nothing new
    Given every session on this machine is already backed up
    When I back up my sessions from the CLI
    Then nothing is uploaded
    And I am told everything is already up to date

  Example: A session grew since the last backup
    Given a session was backed up at 400 KB
    And I have since continued it to 650 KB
    When I back up my sessions from the CLI
    Then only the new 250 KB is uploaded
    And the registry holds one copy of that session, 650 KB long

Rule: Backing up needs me to be signed in

  Example: Not signed in
    Given I am not signed in to a registry
    When I back up my sessions from the CLI
    Then nothing is uploaded
    And I am told how to sign in
```

## Context
- Suggested command: `protostar sync`.
- The CLI tracks progress per file locally; the registry deduplicates independently, so a lost local
  record never creates duplicates.
- Subagent transcripts are covered by a separate story.

## Out of scope
- Backing up automatically while I work (story: Sessions back up as I work).
- Codex sessions (story: Back up my Codex sessions).

**Estimate:** 8. Three rules, a new upload contract, local progress tracking, and server-side dedupe.
~~~

## Before and after: a real backlog

These were written before the method existed. Each shows a different failure.

**1.** Before:
> As a developer, I run `protostar sync` and every Claude Code session on this machine is backed up to
> my registry, so Claude Code's cleanup can't delete my history.

Problems: not in statement form; the exact command is in the need; the purpose is narrower than the
real reason (one central copy across machines, not just surviving cleanup). "Developer" is fine here,
since protostar is a developer tool, but a more specific archetype says more.

After: the full story above.

**2.** Before:
> Know what's backed up on this machine: `protostar sessions status` shows synced vs pending, using
> only local file information.

Problems: no actor, need, or purpose; a command name; an implementation constraint ("only local file
information") in the story itself.

After:
> **As** a multi-machine user, **I want** to see which sessions on this machine are not backed up yet,
> **so that** I know whether it is safe to wipe or leave this machine.

The "local information only" constraint moves to Context.

**3.** Before:
> Fixes reach me without upgrading: when session parsing improves, my existing sessions are re-processed.

This one is close. It names a real, user-visible outcome. Needs an actor and statement form:

> **As** any protostar user, **I want** improvements in how sessions are read to apply to sessions I
> have already backed up, **so that** my history gets better without me upgrading or re-uploading
> anything.

**4.** Before (listed as a story):
> Envelope contract v1; raw blob storage decision; append endpoint with dedupe rules.

Routing: not a story. No actor can observe it. It is the technical work of "Back up my sessions",
so it stays inside that story. The storage decision is a real unknown: if it cannot be settled in a
conversation, it is a **spike** whose artifact is an ADR comparing the options against the measured
session sizes.

## Routing examples

| Item | Route | Why |
|---|---|---|
| "Set up CI for the registry" | Enabler, if no story can absorb it | Cross-cutting, not user-visible; must name the stories it blocks |
| "Add the sessions table" | Part of the first story that stores sessions | A technical layer, not a story |
| "Upload and parse in parallel" | Sub-tasks of one story | Separate parallel work inside a story |
| "Figure out how Codex stores sessions" | Spike | Output is knowledge; artifact is a format write-up with samples |
| "Sessions, skills, and config follow me to a new machine" | Epic | Several distinct outcomes |
