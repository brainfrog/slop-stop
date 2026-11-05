# Structural patterns

Shared by Russian and English. Markers *(first sight)*, *(cluster)*, *(weak)*, and "Own threshold:" are defined in SKILL.md under "When a pattern counts". Cutting content (not padding) follows core rule 3; every replacement keeps the checks of core rule 2.

## A. Staging instead of stating

### "Not X but Y" *(first sight)*

| Pattern | Example |
|---|---|
| «Не X, а Y» / «Не просто X, а Y» | «Это не просто кэш, а слой согласованности» |
| Contrast split across sentences | «Это не значит, что X. Это значит, что Y.» |
| «Проблема не в X. Проблема в Y.» | Template reframing |
| Negative tail | «Опции берутся из выбранного элемента, без угадывания» |
| Negative listing | «Не X. Не Y. А Z.» |
| English forms | "It's not X. It's Y.", "not just X, but Y", "X, not Y" as a tail |

The negative half names something nobody claimed and only adds weight to the positive half. State Y directly. Exception: keep the contrast when it corrects a misconception the reader likely holds, or when both halves carry information: «Лимит считается на проект, а не на пользователя» is fine if that is a common mistake.

### Closing morals and dramatic fragments *(first sight)*

- A one-line paragraph that repeats the previous one: «Так кэш и снижает нагрузку.»
- The same closer under every section.
- A sentence after an example that explains what was just shown: «Это наглядно показывает, как кэш снижает нагрузку.»
- A run of fragments: «Скорость. Надёжность. Простота.» / «Это работает. Всегда. Без исключений.»
- «Точка.» / «Вот и всё.» as a separate sentence.
- Summary openers: «Подводя итог», «Таким образом, можно сделать вывод», «В заключение», «Время покажет»; "In summary", "In conclusion", "Ultimately", "Overall", "All in all", "Time will tell".
- English: "That's the real win.", "Full stop.", "Let that sink in."

Cut without a trace only what repeats. A closing sentence that adds an evaluation of its own («в этом его главная ценность», «это кардинально изменило ситуацию») is a significance claim: cut it under core rule 3 (see "Significance"). Exception: keep it if it adds a new fact or consequence; "overall" meaning "in total" and "ultimately" meaning "at the end of a chain" ("ultimately, the request reaches the database") are claim words (core rule 2). Merge fragments into one sentence. End on the last concrete fact.

### Fake depth *(first sight)*

«По своей сути», «на самом деле всё упирается в», «настоящий вопрос в том», «X — это язык Y», «X становится ловушкой», «данные — новая нефть». An ordinary thought dressed as a hidden truth or an aphorism. Replace with the plain claim. Same for "insider" run-ups: «вот чего никто не замечает», «мало кто знает, но». English: "At its core", "The real question is", "What really matters is".

### Run-ups *(first sight)*

A sentence or an opener that announces a point instead of making it. Delete it whole, do not soften it, and start with the point. A casual tone does not cure it: «короче, сейчас расскажу» is still a run-up. Test: delete the opener and reread the sentence. If it lost nothing, the opener was a run-up. Exception: if it lost a warning, a cause, or a change of topic, the opener does work and stays: «Необходимо учитывать, что лимит считается на проект» (without it the caveat reads as a plain fact), «Дело в том, что кэш не сбрасывается» (the cause), «Что касается миграций, они идут отдельно» (the topic shift), "Note that the limit is per project". «Сразу предупрежу, тут есть нюанс» is a run-up: it announces the warning and gives it later.

- Russian: «Давайте разберёмся», «Давайте посмотрим», «Рассмотрим подробнее», «Разберём по пунктам», «Вот что нужно знать», «Стоит отметить, что», «Важно отметить», «Следует подчеркнуть», «Суть в том, что», «Правда в том, что», «Интересно, что», «Примечательно, что», «Если коротко» and «Короче говоря» before something already short, «В современном мире», «В наше время», «В эпоху цифровизации», «Смотрите,».
- English: "Here's the thing:", "Here's what you need to know", "Let's dive in", "Let's break this down", "Let's take a look at", "It's worth noting that", "It's important to note that", "Importantly,", "Crucially,", "Interestingly,", "Notably,", "The truth is", "The reality is", "In today's [X]", "In a world where", "In this section, we'll…", "As we'll see…", "Without further ado", and a pseudo-cleft opener ("What this means is…", "What happens is…"). An ordinary clause starting with when, where, or if is not one.
- «Как известно,», «Общеизвестно, что», "As is well known,", "As we all know,": the author states X as a fact; delete the opener and keep X as a fact.

**Run-ups at paragraph level.** Read only the first sentences of the paragraphs in a row. If they form a table of contents, the text is built from announcements. Start each paragraph with its point.

### Performed honesty and precision *(first sight)*

«Стоит уточнить», «здесь важно быть точным», «если честно», «Честно?», «скажем прямо», «одна оговорка сразу», «есть одна конкретная причина», «это нужно проговорить»; "To be precise", "To be honest", "Let me be clear", "it's worth being careful here", "the honest answer is", "one caveat up front", "in one specific way", "it bears repeating", "credit where it's due". The author announces precision instead of being precise. Delete the announcement, keep what follows, including any claim the announcement itself made. If nothing follows, delete the sentence.

- Bad: «Прогоны отличаются в одном конкретном аспекте. Во втором окно контекста больше.»
- Good: «Прогоны отличаются только окном контекста: во втором оно больше.» («В одном аспекте» is a claim, "no other differences", so «только» keeps it.)

### Arguing with an absent opponent *(first sight)*

«Можно было бы подумать, что…», «Это не столько про X», «Я не говорю, что…», «Напрашивается решение… но», «Кто-то скажет…». The text answers an objection or rejects an option that appears nowhere else. Delete the defence; any claim inside it stays. Exception: real alternatives in ADRs and design docs stay.

### Options instead of an answer *(first sight)*

«Существует несколько подходов к…», «Это зависит от многих факторов», «С одной стороны… с другой стороны». Give the answer first. If a list follows, the list is the answer: open with it. If the source states no position, do not invent one; drop the empty symmetry and keep the facts. Exception: «Во-первых… во-вторых…» is fine.

## B. Rhythm by rule

### Triads

Ideas arrive in threes to sound complete even when there are two parts. Own threshold: any group of three whose items do not each carry a separate idea; merge those. This applies to groups inside prose; items of a list, table, or instruction stay (core rule 8).

### Identical blocks

Sections of equal length, the lists of every section all three items long, a summary line under every section. Own threshold: judged per document, the same shape in most sections. This pattern never shortens a single list (core rule 8). Shuffle test: swap the second and fourth paragraphs; if nothing breaks, it is a stack of interchangeable blocks, not an argument. Let each section be as long as its content. Delete closing summaries that only repeat.

### Connective pile-up

«Кроме того», «Более того», «Помимо этого»; "Additionally", "Moreover", "Furthermore". Own threshold: more than one such opener in a paragraph. Delete the extra additive connectives ("in addition") and let sentence order carry the logic, or start a new paragraph. Exception: a connective that states a cause, a consequence, or a contrast («таким образом» meaning "therefore", «в свою очередь» meaning "in turn, as a result") stays: deleting it loses causality (core rule 2).

### Repeated openings *(weak)*

Several sentences in a row start with the same subject («Сервис… Сервис… Сервис…»). Merge them or start with the action. Do not fix this by swapping the term for a synonym (core rule 5).

### Dash as a universal connector, Russian

The Russian dash rule; for English see phrases-en.md. Own threshold: three or more connecting dashes in one paragraph; one or two are normal. Replace the extra ones with a period, comma, colon, or parentheses, and vary the choice: a colon in every other sentence is the same pattern. The grammatical dash (between subject and predicate, in elliptical sentences) is not counted and stays.

### Stacked hedges

«Это, возможно, потенциально может привести к…», "could potentially perhaps". Own threshold: three or more softeners in one sentence; one or two is ordinary caution. Remove duplicate softeners and keep one if the uncertainty is real. Qualifiers that set scope, precision, or time («в некоторых случаях», «при включённом X», «обычно», «около», «пока») are not softeners: they stay (core rule 2).

### Self-question, self-answer

«Зачем это нужно? Чтобы не терять задачи при рестарте.», «Результат? Задержка упала вдвое.», "Why does this matter?", "The result? …". Own threshold: more than one per text. State it: «Это нужно, чтобы не терять задачи при рестарте.» Exception: an FAQ, where questions are the genre.

### Treadmill *(first sight)*

A section restates one idea in different words. Ask what each paragraph adds to the previous one. "Nothing, but louder": merge and keep the clearest version.

The same happens across sections: one argument given in full twice, or one option or default described in several places. In an ADR this is typically "Decision" and "Alternatives" both explaining why an option was rejected. Keep the full argument in one place, where the reader looks for it first. Elsewhere leave the conclusion and a reference («отвергнут из-за дефекта Joliet, см. „Решение“»). Exception: a short recap that adds a new fact is not a repeat; agent instructions may repeat key rules on purpose (genres.md).

## C. Inflation

### Significance *(cluster)*

«Играет ключевую роль», «знаменует переход», «закладывает основу для», «важный шаг в развитии», «открывает новые возможности», «выйти на новый уровень»; "plays a key role", "marks a shift", "paves the way for", "opens the door to".

Test: remove the significance and see what is left of its predicate. If a fact is left, the significance was padding: keep the fact, drop the significance (core rule 3). «X играет роль в Y» leaves the fact «X влияет на Y», or what the source says X does there. A rank on a fact is part of the fact, not significance: in «X играет ключевую роль в Y» the fact is that X affects Y, and «ключевую» compares X with the other causes of Y, so the rank stays in plain words: «X — один из главных факторов Y», "X is a major factor in Y" (not «главный», "the main factor", unless the source says there is no other). An intensity with no comparison («значительно», "significantly") is padding. If nothing is left, or only a rank on what the reader already knows, the significance was the predicate's whole content: a claim of its own, even when the sentence also states facts. «Модуль является ключевым компонентом системы и обеспечивает X» leaves «модуль — компонент системы»: that a module is part of its system says nothing, so ranking it is pure evaluation, and «является ключевым компонентом системы» is a claim. Same for whole sentences: «Это важный шаг к…», «Последствия значительны»; "This is a major step forward", "The implications are significant", "The stakes are high", "The future looks bright". Name the specific thing if the source gives it; otherwise cut the claim under core rule 3. A participle rider is not a predicate: see "-ing riders" in phrases-en.md and "Participle tails" in phrases-ru.md.

### Vague relation *(cluster)*

«Связан с», «в связи с», «в контексте»; "associated with", "related to". Name the relation if the source gives it: «вызывается из», «хранит», «заменяет». Otherwise keep it vague.

### False agency *(cluster)*

An inanimate thing perceives, speaks, wants, demands, or decides: «данные говорят», «логи подсказывают», «архитектура требует», «рынок вознаграждает», «решение возникло». Keep the source of the claim without the human verb: «по данным мониторинга…», «в логах видно, что…»; name the actor if the source does. Do not invent an actor, and do not drop the source. Exception: a system doing its function is not this pattern: «сервис повторяет запрос», «кэш хранит ответы», «таймаут обрывает запрос».

### Anonymous authority *(cluster)*

«Эксперты считают», «по отраслевым данным», «принято считать», «специалисты рекомендуют»; "experts say", "it is widely believed". The author attributes X to someone else. (An opener that presents X as common knowledge is different: the author states X as a fact; see "Run-ups".) Name the source if the text gives it. Otherwise keep the claim attributed, as an opinion and not a fact («считается, что X»), and warn that the source is unnamed (SKILL.md, Output modes, Warnings). Never turn it into a bare statement of fact (core rule 2). A missing citation by itself is not a pattern.

### Ranges without a scale *(cluster)*

«От небольших проектов до крупных кластеров», «от новичков до профи». Decoration without a scale. Name the actual scope if the source gives it; otherwise cut it under core rule 3.

## D. Formatting by rule

### Bold as decoration

Bold in every paragraph, a bold label with a colon on every list item. Own threshold: bold in most paragraphs of a text, or bold labels on most items of a list; one bold fact or one labelled item is normal. Remove it. If the labels carry no information, turn the list into a sentence. Bold, if any, goes on a specific fact: a number, a name, a deadline. Exception: agent instructions (genres.md).

- Bad: «- **Производительность:** производительность улучшена. - **Надёжность:** надёжность повышена.»
- Good: the same facts in one sentence.

### Decorative headings *(first sight)*

Emojis and arrows in headings and list items, `---` between every section, Capitalised Every Word, a heading written for effect instead of naming the content, a period at the end of a heading. Exception: the repository's own convention (English Title Case, a house style for rules), and arrows in tables, data-flow notation, and changelogs (`A → B`).

### Heading repeated by the first sentence *(first sight)*

«## Производительность / Производительность важна. / Когда нагрузка растёт, …»: delete the second line when it only restates the heading. Here it also claims importance, so the cut follows core rule 3 (see "Significance").

## E. Chat and draft leftovers

### Chatbot lines *(first sight)*

«Отличный вопрос!», «Конечно! Вот вариант:», «Надеюсь, это поможет», «Дайте знать, если…», «Хотите, я…?»; "Great question!", "Certainly! Here is…", "I hope this helps", "Let me know if…", "Would you like me to…". Remove the wrapper, keep the content. Exception: in a reply to the user a next step is fine if it is specific and non-obvious; a plain "Here is an example:" or «Вот пример:» that introduces content in a document is not a wrapper.

### Thinking out loud *(first sight)*

«Давайте подумаем», «Шаг 1: разберёмся, что тут спрашивают», «Сначала я посмотрю…, затем…», «Теперь, когда мы установили». The writer narrates how they are producing the text. Remove the scaffolding, keep the conclusion. Exception: steps or a plan the text is meant to give stay: «Шаг 1: соберите образ», «Сначала соберу образ, затем обновлю манифест» in a task plan.

### Knowledge-limit disclaimers *(first sight)*

«На момент обучения», «по доступной информации», «подробности не раскрываются» followed by a guess. Say what the source lacks. The guess is invented content (core rule 1): remove it with a warning (SKILL.md, Output modes, Warnings).

### Technical junk *(first sight)*

- Unfilled placeholders: `[Название]`, `[вставить дату]`, `XX%`, `TODO: описание`. Do not fill them; warn the author (SKILL.md, Output modes, Warnings).
- Chatbot citation tokens: `citeturn0search0`, `contentReference[oaicite:0]`, `[cite: 8]`, `oai_citation`, stray `</think>`.
- `utm_source=chatgpt.com` and the like in URLs.
- Invisible characters: U+200B, U+200D, U+2060, U+00AD, U+FEFF. Non-breaking spaces (U+00A0) are not junk: Russian typography uses them before dashes and between numbers and units.
- Mixed Cyrillic and Latin inside a word (`сеrvice`, `Пpoкcи`). The grep below also matches slang with Russian endings («PRом», «Kubernetesе»); check every hit by hand.

Inside code, commands, or identifiers do not fix any of these: core rule 4 keeps code as it is, and a stray character there is a bug the author must see, so warn instead (SKILL.md, Output modes, Warnings).

Quick check for the last two. Requires GNU grep with a UTF-8 locale (prefix `LC_ALL=C.UTF-8` if `grep -P` complains about the locale); BSD grep on macOS has no `-P`.

```bash
grep -nP '[\x{200B}\x{200D}\x{2060}\x{00AD}\x{FEFF}]' FILE
grep -nP '\p{Cyrillic}\p{Latin}|\p{Latin}\p{Cyrillic}' FILE
```

## F. Consistency and grammar

Shared by Russian and English; the examples are Russian.

### One notation per number *(first sight)*

The same quantity in one notation throughout: not «1,5 млн», «1 500 000», and «полтора миллиона» in one text; not «МБ» and «Мбайт» for the same unit. Different units are not notations: «МБ» and MiB may mean different sizes, so never unify them (core rules 2 and 4). Warn instead of editing only when the text itself shows a mix-up, such as one quantity given in both units with different numbers (SKILL.md, Output modes, Warnings).

### Mixed «ты» and «вы» *(first sight)*

Do not switch between «ты» and «вы» within one text. Impersonal forms («нужно указать», «указывается») mix freely with either and are not this pattern.

### Dangling participle *(first sight)*

The participle refers to someone other than the subject: «Получив ответ, задача переходит в статус done» (Having received the response, the task moves to done): the task did not receive anything. Rebuild: «Когда приходит ответ, задача переходит в статус done».

## English only

These rules depend on English grammar and do not apply to Russian:

- dashes: see phrases-en.md;
- *(weak)* the hyphen in compound adjectives after the noun: "the report is high quality", not "high-quality".
