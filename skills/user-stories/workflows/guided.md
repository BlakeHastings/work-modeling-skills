# Guided workflow: brain dump, then grill

For a user who has an idea in their head but not a story. Do not walk them through the template field
by field; that makes them do the structuring and gets thin answers. Get everything out first, then
do the structuring yourself and challenge what does not hold up.

```
Progress:
- [ ] 1. Ask for the brain dump
- [ ] 2. Look up what you can yourself
- [ ] 3. Break the dump into stories
- [ ] 4. Grill in rounds until nothing is assumed
- [ ] 5. Draft the story and run the checks
- [ ] 6. Confirm with the user
```

## 1. Ask for the brain dump

One short message: ask them to dump everything they know or are thinking about, as raw as it is.
Who it is for, what bugs them today, what they imagine, constraints, half-formed worries. Say that
mess is fine and that you will do the organising. Do not ask structured questions yet.

## 2. Look up what you can yourself

Facts are your job, not the user's. Follow "Gather context before asking" in SKILL.md against
everything the dump touches: search the tracker for an existing or duplicate story, fetch any ticket
or decision they mentioned and compare it with what they said, and use every source the available
tools reach (tracker, docs, code, memory) for archetypes, related stories, and current behaviour.
Never ask the user something you could have found. Open the first grilling round with a short note of
what you found, so they can correct it.

## 3. Break the dump into stories

A brain dump is raw material, not a request for one story, so do not play it back as a single story
or argue about its size. Break it down straight away: list the stories you see in it, one line each,
with any that already exist, and recommend which to work through first. Grill one at a time from
there. If the dump only holds one story, grill it as it is.

## 4. Grill in rounds

Treat the story as a tree of decisions: actor, need, purpose, then the rules, then the examples and
edge cases under each rule. A decision is ready to ask about once the decisions it depends on are
settled.

Each round, ask every question that is ready now, numbered, each with your recommended answer, worded
so that "yes" accepts the recommendation:

```
Q1. Actor: You described two kinds of people. Is this story for the multi-machine user only, with
the single-machine case as its own story?
→ Recommended: yes. The single-machine user gets little from a central copy, so their story is
weaker and should be weighed separately.

Q2. Purpose: ...
```

Then wait. Their answers settle some decisions and unlock others; ask the next round. Do not ask a
question in the same round as one it depends on.

Challenge, do not just collect. Push on:
- a purpose that restates the need ("so that they're backed up")
- a need that names a mechanism
- two needs hiding in one ("and")
- rules that contradict each other, or an example that breaks a stated rule
- scope that sounds like an epic
- anything that is really a sub-task, enabler, or spike

The grilling is done when no branch is left open and nothing is being silently assumed. If the user
wants to stop early, stop: anything unresolved becomes an Open question.

## 5. Draft and check

Write the story in the template from `references/anatomy.md`. Run every check in
`references/checks.md` and fix what fails. If the dump produced more than one story, say so and draft
each.

## 6. Confirm

Show the story. Point out the one or two places most likely to be wrong, each as a question with your
recommended answer. Revise on their answer.
