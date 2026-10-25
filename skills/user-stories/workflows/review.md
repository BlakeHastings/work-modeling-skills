# Review workflow

For critiquing one story or rewriting a batch.

## One story

1. Gather context as in SKILL.md: fetch the story from its tracker if it lives there, plus its epic
   and linked items, so the review judges what is actually recorded.
2. Route it ("Is it really a story?" in SKILL.md). If it is a sub-task, enabler, spike, or epic, say
   so first: the rest of the review depends on it.
3. Run every check in `references/checks.md`.
4. Report findings ordered by impact. Each finding gets the concrete rewrite, not just the name of the
   smell.
5. Offer the full rewritten story. If it is already fine, say so plainly.

## A batch or backlog

1. Review each story as above, but fix what is unambiguous without asking.
2. Collect everything that needs the user's judgement into **one** numbered list of questions, each
   with a recommended answer, rather than asking story by story.
3. Report: what you rewrote, what you re-routed (story to sub-task, story to epic, and so on), and the
   question list.
4. Look across the batch as well as within it: duplicated stories, stories that lean on each other,
   and missing actors who appear in one story but have no stories of their own.
