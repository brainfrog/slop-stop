# Russian patterns

Most Russian AI patterns are calques of an English draft: the model thinks in English and translates. Hence «является», participle tails, extra pronouns, and English word order.

Markers *(first sight)*, *(cluster)*, *(weak)*, and "Own threshold:" are defined in SKILL.md under "When a pattern counts". This file holds word-level patterns only; run-ups, closing morals, performed honesty, and chatbot lines in both languages are in structures.md. Every replacement below keeps the checks of core rule 2: if a replacement would change modality, scope, a role, a unit, or add an actor, keep the original wording.

## Empty intensifiers *(cluster)*

Cut: «действительно», «по-настоящему», «поистине», «буквально», «просто» (as emphasis), «по сути», «на самом деле», «безусловно», «несомненно», «крайне», «максимально», «кардинально», «принципиально».

Exception: keep the word when it carries degree, scope, or a term: «крайне редко», «принципиально невозможно», «максимально допустимый»; or when it marks an approximation («по сути, это прокси»: functionally, not formally; core rule 2); or when it contrasts with or confirms something stated nearby: «В доке написано 30 с, на самом деле таймаут 60 с», «тест действительно падает, как и описано в задаче». Keep adverbs that are terms: «асинхронно», «атомарно», «идемпотентно», «потокобезопасно», «лениво», «намеренно», «синхронно».

## AI vocabulary (calques) *(cluster)*

| Word | Instead |
|---|---|
| ключевой, важнейший, критически важный | Say what depends on it (from the source). If it ranks one thing among others («ключевой фактор задержки»), keep the rank in plain words («один из главных факторов»; see "Significance" in structures.md); if it only praises, delete the word. Keep technical uses («ключевое слово», «ключевое поле») |
| комплексный (as "comprehensive") | List what it covers (from the source); if the source claims full coverage, «полный»; otherwise delete the word |
| эффективный, оптимальный, надёжный, гибкий, масштабируемый (as praise) | Name the property the source gives: time, size, what failure it survives; otherwise delete the word. If the text already names the property, the word is a term and stays (core rule 4) |
| успешно (реализовал, внедрил) | Delete: the word carries no fact. Exception: keep it if the source contrasts it with a failure («со второй попытки успешно…») |
| обеспечивает | An action verb only if the source says the thing does it itself («хранит», «повторяет запрос»); otherwise keep «обеспечивает» |
| позволяет | The one who acts becomes the subject: «API позволяет клиентам загружать файлы» → «клиенты могут загружать файлы через API»; with no one named, «через API можно загружать файлы». Never «API может загружать файлы» or a direct action («позволяет делать X» is not «делает X»); if unsure, keep «позволяет» («даёт возможность» is the same pattern in longer words) |
| способствует | «помогает»; never a direct action («способствует снижению» is not «снижает») |
| на текущий момент | «сейчас»; never delete: it limits the claim in time |
| в рамках, на базе, посредством | «в», «на», «через», or restructure. Exception: «в рамках» meaning "within the limits of" stays («в рамках квоты» is not «в квоте») |
| данный, этот (on every repeat of a noun) | Repeat the noun or drop the pronoun |
| решение (about any code) | Name the thing the source names: сервис, библиотека, скрипт |
| функционал | «функции», «возможности», or drop the word: «добавлен функционал экспорта» → «добавлен экспорт» |
| бесшовный, прозрачный (as praise) | Say what the user does not have to do (from the source), or delete the word |
| экосистема, ландшафт | The specific area or list of systems from the source |
| уникальный (as praise), инновационный, прорывной | Say what is new (from the source), or delete the word. «Уникальный» as a constraint («уникальное поле», «уникальный ключ») is a term (core rule 4) |

## Back-translation test for calques *(cluster)*

Translate the phrase back to English. If you get a ready English idiom that a Russian speaker would not say, rewrite it.

| Calque | Instead |
|---|---|
| на ежедневной основе (on a daily basis) | каждый день |
| на регулярной основе | регулярно |
| адресовать проблему (address the issue) | заняться проблемой (not «исправить»: addressing is not fixing) |
| в терминах X (in terms of X) | по X, с точки зрения X |
| принять во внимание (take into account) | учесть |

## «Является» and relatives

A calque of "serves as / represents / functions as / has the ability to". Own threshold: two or more of these in one paragraph, counted together («является» and every form in the table below). Stricter than English "Copula avoidance" on purpose: there these verbs are ordinary English, here they are a translation artefact.

| Before | After |
|---|---|
| «Сервис является точкой входа» | «Сервис — точка входа» |
| «представляет собой ISO-образ» | «это ISO-образ» |
| «выступает в роли прокси» | «работает как прокси» |
| «служит для хранения сессий» | «используется для хранения сессий» |
| «имеет возможность» | «может» |

## Participle tails *(first sight)*

The Russian form of English "-ing riders": a participle clause bolted onto a plain fact for weight.

- «…, обеспечивая высокую доступность»
- «…, повышая производительность»
- «…, позволяя командам быстрее…»
- «…, что подчёркивает важность…» / «…, что свидетельствует о…»

Delete the tail. Exception: if it carries a real fact («…, поэтому повторный запуск безопасен»), make it a separate sentence or a clause with an explicit cause, keeping its modality and its actor: the one the tail lets act becomes the subject («…, позволяя cloud-init настраивать сеть» → «Благодаря этому cloud-init может настраивать сеть»).

## Verbal nouns and officialese *(first sight)*

Stricter than English "Filler phrases" on purpose: "in order to" and "in the event that" are ordinary English, while «в целях обеспечения», «в случае возникновения» stack verbal nouns, the mark of Russian officialese.

| Before | After |
|---|---|
| «Нами было принято решение» | «Мы решили» |
| «Осуществляется процесс внедрения» | «Идёт внедрение» |
| «Была проведена работа по оптимизации X» | «Занимались оптимизацией X» (the source claims the work, not its result; no actor, the source names none). «X оптимизировали» only when the source states the result |
| «произвести перезапуск», «производит проверку», «осуществляет проверку» | The verb itself: «перезапустить», «проверяет» |
| «в целях обеспечения X» | «чтобы обеспечить X» |
| «в случае возникновения ошибки» | «если возникнет ошибка», «при ошибке» (a general condition stays general) |

## Genitive chains

Own threshold: four or more nouns in a row in the genitive. Break with a verb or «который», keeping every noun:

| Before | After |
|---|---|
| «порядок формирования отчётов подразделений компании» | «порядок, в котором подразделения компании формируют отчёты» |
| «механизм обработки ошибок валидации запросов клиента» | «механизм, который обрабатывает ошибки валидации запросов клиента» |

Exception: a chain made of terms (`конфигурация сети гостевой ОС`) stays if shorter wording loses precision.

## Extra pronouns *(cluster)*

In Russian, ownership is usually clear from context. The model carries over English "my", "our", "your".

- «Мы улучшили *наш* сервис» → «Мы улучшили сервис»
- «Укажите *ваш* токен в *вашем* конфиге» → «Укажите токен в конфиге»
- «Функция возвращает *свой* результат» → «Функция возвращает результат»

## Word order

In Russian new information usually comes at the end of the sentence, known information at the start. English keeps subject-verb-object order and marks the new with articles. Translated text keeps the English order, so every sentence ends with something the reader already knows. Own threshold: a run of three or more such sentences.

- Bad (release notes for 2.3): «Новый формат логов появился в версии 2.3. Сжатие включено по умолчанию в новом формате. Флаг `--no-compress` нужен для отключения сжатия.»
- Good: «В версии 2.3 появился новый формат логов. В новом формате по умолчанию включено сжатие. Для отключения сжатия нужен флаг `--no-compress`.» (Only the order changed: every sentence now starts with what the reader knows and ends with the new part.)

## Corporate jargon *(cluster)*

| Avoid | Instead |
|---|---|
| Дипдайв, глубокое погружение | Разбор, анализ |
| Синкануться, засинкаться | Обсудить, договориться |
| Геймчейнджер, меняет правила игры | Say what changed (from the source) |
| Двигаясь вперёд | «Дальше», «в дальнейшем» |
| Закрыть вопрос | «Решить вопрос» |
| Прорабатывать | Проектировать, проверять, выяснять (the one the source means) |
| Создавать ценность, раскрыть потенциал | Say the result (from the source), or delete the phrase |

## Commit messages

Rules for the genre, not a pattern. Follow the repo convention (prefix, tense, language). No «Данный коммит…», «Успешно…», «Различные улучшения», «Небольшие правки». The body explains why, only when the subject does not.
