# English phrase list

For English prose: READMEs, `AGENTS.md`, docs, commit messages, MR descriptions, review comments. For Russian text see `phrases-ru.md`.

Markers *(first sight)*, *(cluster)*, *(weak)*, and "Own threshold:" are defined in SKILL.md under "When a pattern counts". This file holds word-level patterns only; run-ups, closing morals, performed honesty, and chatbot lines in both languages are in structures.md. Every replacement below keeps the checks of core rule 2: if a replacement would change modality, scope, a role, a unit, or add an actor, keep the original wording.

## Empty intensifiers *(cluster)*

Cut: really, truly, genuinely, simply, just (as emphasis), literally, actually, fundamentally, inherently, deeply. An adverb that opens a sentence to announce its point is a run-up (see "Run-ups" in structures.md).

Exception: keep the word when it carries degree, scope, or a term: "just one retry" (only), "fundamentally incompatible", "inherently racy", "deeply nested", "genuinely random"; or when it contrasts with or confirms something stated nearby: "the docs say 30 s; the timeout is actually 60 s". Keep technical adverbs: asynchronously, atomically, idempotently, lazily, eagerly, deliberately, synchronously.

## Overused AI words *(cluster)*

| Word | Instead |
|---|---|
| delve into | look at, cover |
| leverage, utilize | use |
| robust, seamless, scalable (as praise) | the property the source gives (retries on X, handles N req/s); otherwise delete the word. If the text already names the property, the word is a term and stays (core rule 4) |
| crucial, pivotal, vital, key (figurative adjective) | say what depends on it (from the source). If it ranks one thing among others ("a key factor in latency"), keep the rank in plain words ("a major factor"; see "Significance" in structures.md); if it only praises, delete the word. Keep technical uses (primary key, API key, key-value) |
| comprehensive | say what it covers (from the source); if the source claims full coverage, "full"; otherwise delete the word |
| enhance, streamline | say what got faster or simpler (from the source); otherwise "improve" for enhance, "simplify" for streamline |
| showcase, highlight, underscore (verbs) | show, point out; keep what is shown ("the report highlights three risks" → "the report points out three risks") |
| foster | help, encourage; never a direct action or a permission ("the shared cache fosters reuse" → "the shared cache encourages reuse", not "lets reuse" or "reuses") |
| empower, enable (as filler) | let, allow, or make the one who acts the subject with "can"; keep the modality and the actor: "the API enables clients to upload files" → "clients can upload files through the API", not "the API can upload files" |
| landscape, ecosystem, tapestry | the systems the source names |
| intricate | "complex" when it claims complexity ("intricate locking scheme"); otherwise delete the word |
| meticulous | delete the word |
| gate/gated (figurative) | limit, require, depend on; keep for real feature gates |

## Copula avoidance *(cluster)*

| Before | After |
|---|---|
| serves as the entry point | is the entry point |
| acts as / functions as a fallback | is a fallback (a role); for a kind of component, "works as" (core rule 2, Roles) |
| boasts / features 3 replicas | has 3 replicas |
| represents a shift | is a change |
| has the ability to | can |

A role stays a role: "serves as a foundation for X" becomes "is a foundation for X", not "does X".

## -ing riders *(first sight)*

A participle clause bolted on to sound thorough: "…, ensuring reliability", "…, enabling teams to…", "…, highlighting the importance of…". Cut it. Exception: if it carries a real fact, make it its own sentence, keeping its modality ("enabling X" → "this lets X happen", not "X happens").

## Filler phrases *(cluster)*

| Before | After |
|---|---|
| in order to | to |
| due to the fact that | because |
| at this point in time | now |
| in the event that | if |
| moving forward | from now on (it limits the claim in time) |
| at the end of the day | cut |
| as mentioned earlier | cut or restructure |

## Dashes

The English dash rule; for Russian see structures.md. When the text is the skill's own (written from scratch, or generated as a step of another task), use no em dashes or en dashes as dashes: use a period, comma, colon, or parentheses. When the text is someone else's, in any mode, keep the author's dashes below the threshold. Own threshold: three or more connecting dashes in one paragraph; reduce them there and vary the replacement. Dashes in code, paths, URLs, and numeric ranges (`1–10`) are never counted.

## Commit messages

Rules for the genre, not a pattern. Follow the repo convention (`feat(scope): …`, ticket prefix). Imperative mood in the subject. No "This commit…", no "Successfully…", no "Various improvements". The body explains why, only when the subject doesn't.
