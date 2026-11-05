# Maintaining slop-stop

For whoever edits the skill. `SKILL.md` links neither here nor to `scripts/`, so neither is loaded when the skill runs.

## After every edit

```bash
cd ~/.claude/skills/slop-stop && python -I scripts/check.py
```

(`python3` wherever `python` is not Python 3. `test_check.sh` finds either and needs GNU sed, as `gsed` on macOS.)

It checks: the frontmatter `name` matches the directory and the Agent Skills format, the description is valid plain YAML (no `: `, no ` #`, no leading indicator such as `[` or `*`) within 1024 characters; every rule reference ("rule 7", "Core rule 3", "rules 1–5 and 8") points at an existing core rule; marker definitions do not leak out of `SKILL.md`; every pattern carries exactly one marker; every example has a "Changes" line; every named cross-reference (`see "X"`, `See "X" in file.md`, `under "X"`, `(file.md, Section, Item)`) points at an existing heading or bold label, in the named file when one is given, and in `(file.md, A, B)` B sits inside A, and in `(core rule N, Label)` the label is a bold label of that rule; every instruction to warn (warn, warns, warned, with a warning) in the references points at the Warnings list; no quoted phrase of two or more words is listed under two patterns (one-word quotes are skipped because they are mostly replacements, so check those by eye); every pair in `PAIRS` in `check.py` (a phrase and its translation, or two wordings of one construction) carries one and the same marker; no listed item reappears in its own pattern's "Exception:" unless it is in `REVIEWED_OVERLAPS`, and that set holds no stale entries; no claim word or hedge from core rule 2 that is in an example's "Before" vanishes from "After" without being quoted in its Changes or Change list (the word lists are read from `SKILL.md`); every example has an entry in `EXAMPLE_SIGNS` in `check.py` whose signs are in its "Before" and meet the markers (written check 7 below), and no entry is stale; `tests/cases.json` is well formed; every `*.md` named outside code exists, and every `"X" in file.md` names an existing section whatever verb precedes it ("see", "under", "follows"); every "Process, step N" exists; the two lists of core rule 2 hold as many Russian words as English ones; every pair in `ASYMMETRIC_PAIRS` really differs in marker and one of its patterns names the other to explain why; the skill directory holds no leftovers (`__pycache__`, `*.pyc`, editor backups); every field of `tests/cases.json` has the right type, and an embedded case has a context; the grep commands in `structures.md` still work (without grep on the machine this is a WARN, not a FAIL). Rule references, cross-references, marker definitions, and pairs match regardless of case, since any of them may open a sentence. Then do the written checks below; the script cannot judge meaning.

After changing `check.py` itself, run `bash scripts/test_check.sh`: it first requires `check.py` to pass on the untouched skill (a crashing checker would otherwise "catch" every mutation), then breaks a copy of the skill in each way the script is meant to catch and fails if any break goes unnoticed or is caught by a different check than the one named. Add a line there for every new check and every new branch of an old one, with the text of the FAIL message it must produce. Where a check could fail on valid text, add a `run_ok` line too: it applies a valid change and requires a pass (a `(MAINTAINING.md, …)` reference once would have failed as a missing file). Edit `check.py` in an editor, not through shell heredocs: escaping once turned a `\n` inside a regex into a real line break and broke the script.

## After every change to SKILL.md or the references

```bash
cd ~/.claude/skills/slop-stop && python -I scripts/eval.py
```

`check.py` sees the text; `eval.py` sees what the model does with it. It gives the whole skill to a fresh `claude -p` session as its system prompt, runs every case in `tests/cases.json`, and checks the answer by regular expressions and, where a regex cannot judge, by yes/no questions to a second session. A full run costs about $0.3–1 and prints the cost; `--case ID` runs one case. A call that returns no answer (a usage limit, the network) is an ERROR, not a FAIL, and the run exits with 2: rerun those cases, they say nothing about the skill. Before calling the skill finished, run `--runs 3`: a model answer varies, and a case must pass every time.

The default run hands the model every reference at once, which tests the rules under ideal conditions. Claude Code loads only `SKILL.md`, and the model decides whether to open the rest. `--realistic` reproduces that: the model gets `SKILL.md` and a Read tool, and a case fails when it skips any file that Process, step 1 requires. Run it before calling the skill finished, and after any change to `SKILL.md` itself. When it was added, the skill as of 4.13.0 skipped the references in 6 runs out of 6 and edited from memory; a mere list of files in Process did not make the model open them, an explicit "every time, even for one sentence, even when the text looks clean" did (12 runs out of 12). So a rule that lives in a reference is only as good as the instruction that makes the model read it.

Every accepted review finding that can show in the skill's behaviour becomes a case, so the same defect cannot return unnoticed:

- One case, one behaviour: the input that used to go wrong and what must happen to it. Write in "origin" which review and finding it comes from.
- Prefer regex checks (`text_contains`, `text_not_contains`, `notes_contains`, `unchanged`); they do not vary. Use `judge` only for what a regex cannot see, and phrase each question so that the right answer is "yes".
- Show that the case can fail: run it with `--skill-dir` against a copy that still has the defect (the backup, or a copy with the fix reverted). A case that has never failed proves nothing. When this was set up, three cases failed on the pre-review backup of 2026-10-09 and passed on the fixed skill.
- A case that fails sometimes on a correct skill is a badly phrased case or a real ambiguity in the rule; fix one of the two, never delete the case to make the run green.

A finding that lives only in the text (two rules that contradict each other, an example that breaks its own threshold) does not always show in behaviour; it goes to `check.py` if it can be detected mechanically, and to the written checks below if it cannot.

## Where each rule lives

Every rule has one home. Other files refer to it by name and never restate it. When a rule changes, change only its home.

| Rule | Home |
|---|---|
| What may be invented, lost, cut, and the meaning checks (core rules 1–3) | `SKILL.md`, Core rules |
| Markers *(first sight)*, *(cluster)*, *(weak)*, "Own threshold:", and that genre overrides them | `SKILL.md`, When a pattern counts |
| Markers decide whether a sentence is edited; rule 3 decides what leaves it | `SKILL.md`, When a pattern counts |
| Which dash rule applies to a sentence | `SKILL.md`, When a pattern counts |
| Russian dash rule | `references/structures.md`, Dash as a universal connector, Russian |
| English dash rule, including the skill's own text vs someone else's | `references/phrases-en.md`, Dashes |
| A pattern's threshold or exception | that pattern's section, phrased "Own threshold:" or "Exception:" |
| Genre norms, including what a genre moves elsewhere and fixed section order | `references/genres.md` |
| Warnings to the author, and content cuts in embedded mode, and where they go in each mode | `SKILL.md`, Output modes, Warnings |
| Commit message rules | "Commit messages" in each phrase file |
| Which references to read, in every mode | `SKILL.md`, Process, step 1 |
| Which core rules trigger an edit on their own (6 and 7 do not) | `SKILL.md`, When a pattern counts |
| When several words may be merged into one term | `SKILL.md`, Core rules, rule 5 |
| Staging and leftovers in both languages (run-ups, closing morals, performed honesty, chatbot lines) | `references/structures.md`; the phrase files hold word-level patterns only |
| Whether a deleted closing sentence leaves a trace (repeat: no; own evaluation: yes) | `references/structures.md`, Closing morals and dramatic fragments |

## Every pattern has exactly one marker

A pattern carries exactly one of: *(first sight)*, *(cluster)*, *(weak)* in its heading, or "Own threshold:" in its text. The script enforces this. Choose by what a single occurrence means:

- a single occurrence is already wrong (a grammar error, a chatbot line, a run-up): *(first sight)*;
- a single occurrence is normal human writing (one «ключевой», one "robust"): *(cluster)*;
- it is a hint only, never a reason to edit: *(weak)*;
- the count that matters is not "one" or "about three in a paragraph" (per sentence, per text, per document): "Own threshold:".

## Every Before → After pair keeps meaning

This applies to `examples.md` and equally to every replacement table row and every Bad/Good line in the references. Most past review findings were table rows that quietly broke core rule 2. Do these checks in writing, not by eye:

1. List every fact, claim, hedge, modal word, cause, role, unit, time limit, actor, and attribution in "Before" (plus "Source" if given).
2. For every one, find it in "After" unchanged in meaning, or under "Change list". Padding (core rule 3) is the only thing that may vanish without a trace.
3. For every fact in "After", find it in "Before" or "Source". If it is not there, add it to the source or remove it from the result.
4. For a replacement row, try it on a sentence where the word carries meaning («крайне редко», «на текущий момент поддерживается только X»), on a sentence with an object or a second participant («API позволяет клиентам загружать файлы»), and on a sentence where X names a kind of thing rather than a role ("acts as a load balancer"). If the row breaks any of them, narrow the row or add an exception. Check the tense too: a general condition must not turn into a past event. Check the aspect: work must not turn into a result («была проведена работа по оптимизации X» once became «X был оптимизирован»). Check the degree: a rank that compares one thing with others stays ("plays a key role in" once became "affects", losing "one of the main causes"); only an intensity with no comparison is padding. A worked example inside a row must use a replacement from that row's own "Instead" column ("highlights" once became "names" while the column offered "show, point out").
4a. The same applies to every listed word or phrase that a pattern deletes, and to every item of a *(first sight)* list: try it in a sentence where it does work (contrast or confirmation: «на самом деле таймаут 60 с»; a plain clause: "When the queue is full…") and in a genre where it is normal (instructions: «Шаг 1: соберите образ»; a task plan; docs: "Here is an example:", which once sat in the chatbot list as a bare "Here is a…"). If it breaks, narrow the item to the form that only a chatbot or a draft produces, or add an exception. Try every evaluative adjective as a term too: «надёжная доставка» with acknowledgements, «уникальное поле», "horizontally scalable". If it has a technical sense, mark it "(as praise)" (core rule 4 keeps the backed sense), and never use it as the sample of padding in a rule or an example without saying why it is praise there («надёжную» once stood bare as the padding sample in core rule 3 and example 1).
5. Read "After" against the skill itself: no negative tail, no closing moral, no dramatic dash, no word repeated in neighbouring clauses (terms excepted, core rule 5), no ambiguous pronoun. A repeat stays when every substitute is vaguer: example 6 once swapped «оставить обходной путь» for «оставить как есть», which can read as "change nothing". A pattern kept under its own "Exception:" is fine; say so in "Changes".
6. In `examples.md` use the format Before / After / Changes, plus Change list when content is cut, plus Source when the result draws on a diff, code, or ticket.
7. "Before" and every "Bad:" line must meet the marker of every pattern they illustrate: a *(cluster)* edit needs about three signs in one paragraph, an "Own threshold:" edit needs that threshold. A lone *(cluster)* sign is normal writing, and an example that edits it teaches the opposite of the marker (E4 once edited a lone "The data tells us…" sentence; example 5 once edited bold labels as a *(cluster)* pattern with no other sign; the "Word order" Bad line once had two sentences under a threshold of three). When the count is not obvious, name the signs in "Changes". For `examples.md` the script counts: list each new example's signs in `EXAMPLE_SIGNS` in `check.py`; for Bad lines in the references the count stays a written check. A Bad/Good pair changes only what its pattern names, so the fix cannot be credited to another pattern (the same "Word order" pair was mostly fixed by dropping «Данный»).

## Before adding a rule

- Check it against core rules 1–3 using the checks above. Any instruction that says "say", "name", or "delete" must work when the source lacks the detail (rule 1) and when the text is content rather than padding (rule 3).
- Give it exactly one marker.
- Compare the pattern's list with its own "Exception:". An item whose usual meaning the exception protects does not belong in the list («Таким образом» usually means "therefore", so it left the connective list; «Необходимо учитывать» usually introduces a caveat, so it left the run-up list). An item that is usually empty and only sometimes protected stays, with the exception naming the rare case («максимально» / «максимально допустимый»). The script cannot tell these apart, because the difference is how often each meaning occurs, so it fails on every overlap until you decide and add the item to `REVIEWED_OVERLAPS` (or take it out of the list). "Importantly," once stood in the run-up list and as a kept example in the run-up exception, while «Важно отметить» was deleted.
- If it ranks one rule over others ("outranks", "overrides"), name exactly which rules it outranks. "The sample outranks the style rules" once let a writing sample override core rule 8, which is about completeness, not style.
- Check the genre table: does some genre treat this pattern as normal?
- Read every core rule literally against the new rule and against each other: does one forbid what another prescribes? Past clashes: a too-broad "false agency" flagged "сервис повторяет запрос", which rule 7 asks for; rule 4 ("terms untouchable") forbade the unification rule 5 asks for; rule 8 ("never merge items") forbade turning a bold-label list into a sentence; rule 8 ("no pattern is a reason to drop an item") forbade the cut of an item with no fact behind it that rule 3 allows. Fix the clash with an explicit exception in the rule that is too broad.
- Put a phrase and its translation in the same pattern («если честно» and "To be honest" both under "Performed honesty and precision"). Word-level patterns live in two phrase files, so there the pair goes into the matching pattern of each file, and both patterns carry the same marker. Before adding a phrase, search the other language's files for its translation, including as a single word inside a list ("interestingly" once sat among intensifiers while «Интересно, что» was a run-up). Add the pair to `PAIRS` in `check.py`: the script cannot translate, but it keeps listed pairs in step. The same holds inside one language: one construction in two wordings belongs in one pattern («произвести перезапуск» was *(first sight)* while «осуществляет проверку» was *(cluster)*). Markers may differ only when the pattern's own text says why, naming the other pattern in quotes, as «Является» does against English "Copula avoidance"; then add the pair to `ASYMMETRIC_PAIRS` in `check.py` ("in order to" against «в целях обеспечения» once differed with no word of explanation).
- If the pattern deletes a whole sentence or a predicate, say whether it leaves a trace: only what repeats, or a word attached to a fact, may vanish; a sentence or a predicate with a claim of its own, even an evaluation, follows core rule 3 («является ключевым компонентом системы» once vanished as padding in an example while "Significance" required a trace). Check every example and Bad/Good line that deletes the same kind of text.
- Each quoted example must show exactly the case its bullet names: an example of a "repeat" must be a pure repeat, not a repeat plus an evaluation («В этом и есть главный выигрыш» once illustrated a repeat while carrying a claim).
- An instruction that limits output ("only the final text", "without comment", "do not rewrite") must leave room for Warnings in every mode: "return it unchanged without comment" once hid an unfilled placeholder in embedded mode, and diagnosis mode once had nowhere to put warnings.
- A condition that limits a rule lives in the rule itself or in a reference that Process, step 1 makes the model read, never only in `examples.md`, which the model may skip: "merge words only when the source shows they name one object" once lived only in example 8, and the model merged an instance, a VM, and an «экземпляр» in 3 runs out of 3. Fixing an example is therefore never enough on its own: «корректно» kept only in example 1 was still dropped in 1 realistic run out of 3 until core rule 2 listed it. Confirm every fix with `--realistic`, where `examples.md` is optional.
- A core rule with no marker must say whether it triggers an edit on its own. Rules 6 and 7 once did not, and the model rewrote a correct passive («запрос обрабатывается воркером») in 2 runs out of 2.
- A fallback replacement must not be a pattern itself: «позволяет» once fell back to «даёт возможность», the same officialese in longer words; when unsure, the fallback is the original word.
- Put it in one place and add it to the table above if it is a new kind of rule.
- Run the script.

## Which review findings to accept

Every review by a model finds something; a review never comes back empty. Accept a finding when it shows one of these:

1. A Before → After pair anywhere breaks core rules 1–3 (invents, loses, distorts, or silently cuts).
2. Two places give the model instructions it cannot follow at once.
3. Something breaks loading or triggering (frontmatter, description).
4. A rule makes the model damage correct text (false positives on real technical prose).

Decline findings that are taste ("this example could be stronger"), that ask for more coverage of rare patterns, or that would restate a rule in a second place.

When a finding is real, fix the class, not the instance: run the written checks over every table and example for the same defect, and if the defect can be detected mechanically, add it to `scripts/check.py` and confirm the script fails on a copy that contains the defect. If it can show in behaviour, add a case to `tests/cases.json` (see "After every change to SKILL.md or the references").

Stop when two independent reviews in a row bring nothing that meets the four criteria above. Then freeze the skill: change it only when it goes wrong on a real text, and turn that text into a case first.
