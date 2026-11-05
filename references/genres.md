# Technical text genres

Identify the genre before editing. The same rule helps a README and hurts a spec. Where a genre moves content elsewhere (history out of a README, diagnosis out of a reply), the cut follows core rule 3.

| Genre | Tone | Main thing | Notes |
|---|---|---|---|
| ADR | Neutral, precise | Context → decision → consequences | History and rejected options belong here: that is the genre. Every rejected option needs its reason |
| Spec, task plan | Dry, reference | Completeness, verifiability | Lists and tables keep every item (core rule 8). Rhythm does not matter. Code references stay as they are |
| README, docs | Direct, skimmable | How it is now, not how it changed | Change history moves to the changelog or MR (see below). The first paragraph answers "what is this and why" |
| Code comment | Minimal | Why, not what | Do not retell the code. Edit history belongs in git, not in the comment |
| Commit | Terse | What changed and why | See "Commit messages" in the phrase file for the text's language |
| MR description | Businesslike | What, why, how to verify | Change history is fine. Do not retell the diff |
| Changelog, release notes | Terse, factual | What the user or operator sees change | History is the genre. When writing one, one item per visible change. When editing, keep every item; flag items with no visible effect the same way core rule 3 reports cuts |
| Agent instructions (`AGENTS.md`, `CLAUDE.md`, `SKILL.md`) | Imperative, explicit | Rules an agent can follow and check | Imperative mood, deliberate repetition of key rules, bold labels on list items, and "Important:" markers are the norm here, not patterns. Still cut run-ups, inflation, and chat leftovers |
| Review or chat reply | Conversational, short | Decision first; a short acknowledgement may precede it | See "Wrong reader" below. Shorthand (`db`, `env`, `config`) is fine |
| Reply to the user in a terminal (only when a project instruction requires the skill) | Direct | Result first, then details | See "Chatbot lines" in structures.md |

## Reference text

Port tables, flag lists, field lists, build steps are reference text. They need neither rhythm nor voice. Check them only for junk: run-ups, intensifiers, chat leftovers.

## Neutrality

In docs, specs, and ADRs a neutral, plain tone is the human one. Do not add opinions, jokes, or first person to make the text "livelier". If the source has an opinion, keep it.

## Describe the current state

Outside changelogs, ADRs, MR descriptions, and migration guides, the text must read without knowing the last commit.

- Source: «Эта функция добавлена вместо прежнего перебора всех элементов, который давал O(n²); теперь она ищет по хеш-таблице за O(1).»
- Result: «Функция ищет по хеш-таблице за O(1).»
- Change list: cut the history (the function replaced iteration over all elements, which was O(n²)) and «теперь», which only contrasted with it; put the history in the changelog or MR description.

## Wrong reader

In a reply to a question or review, start with the decision; a short acknowledgement («Да, вы правы») may come before it. Keep what affects whether the reader agrees: the argument they lack and a link they need to act. Cut context they already have. Diagnosis and proof that the plan works belong in the ticket or document; cutting them here follows core rule 3.
