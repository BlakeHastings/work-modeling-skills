# Draft-and-confirm workflow

The default. The request, the conversation, or what the available tools can find already gives the
actor, the need, and the purpose, or makes them clearly inferable. Write first, then check with the
user in one round.

```
Progress:
- [ ] 1. Gather what is already known
- [ ] 2. Route the item and draft the story
- [ ] 3. Run the checks
- [ ] 4. Present with assumptions and questions
```

## 1. Gather

Follow "Gather context before asking" in SKILL.md: check the tracker for an existing or duplicate
story, read anything the user referred to, and pull the actor, need, purpose, rules, and constraints
from the request, the conversation, and whatever the available tools reach. If a matching story
already exists, propose updating it instead of drafting a new one. Do not ask for anything you can
find.

## 2. Route and draft

Apply "Is it really a story?" from SKILL.md. Draft in the template from `references/anatomy.md`.
Implementation detail the user gave goes in Context, not in the statement or criteria.

## 3. Check

Run every check in `references/checks.md` and fix what fails. If something only the user can resolve
fails, keep it as an Open question rather than guessing.

## 4. Present

Show the story, then underneath:
- **Assumptions**: what you inferred that they did not say. Keep it to the ones that matter.
- **Questions**: only those whose answer would change the story, numbered, each with your recommended
  answer, worded so "yes" accepts it.

One round. Apply their answers and show the final version. If they say it is fine as is, it is done.
