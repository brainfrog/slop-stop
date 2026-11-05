# Before/after examples

Every example follows core rules 1–3: the result contains only facts from the source, passes every check of core rule 2, and every content cut appears under "Change list". Padding is removed without a trace.

## 1. Inflation and a participle tail (docs)

**Before:**
> Данный модуль является ключевым компонентом системы и обеспечивает надёжную доставку метаданных гостевой ОС, позволяя cloud-init корректно настраивать сеть и SSH-ключи.

**After:**
> Модуль обеспечивает доставку метаданных гостевой ОС. Благодаря этому cloud-init может корректно настраивать сеть и SSH-ключи.

**Changes:** padding removed: «данный», «надёжную». «Корректно» stays: «может корректно настраивать» says that without the module the setup goes wrong, «может настраивать» that there is no setup at all; these are different claims (core rule 2). «Надёжную» is praise here: nothing in the text backs it (no acknowledgements, retries, or delivery guarantee); with them it would be a term and stay (core rule 4). «Обеспечивает» stays: the source does not say the module delivers the metadata itself, so «доставляет» would change its role. The participle tail «позволяя…» carries a fact, so it became a sentence; «позволяя» keeps its modality as «может», and the cause stays as «благодаря этому».

**Change list:** cut «является ключевым компонентом системы»: without «ключевым» the predicate says nothing, so its only content was an evaluation (structures.md, Significance). If the source says what depends on the module, name that instead.

## 2. Officialese without invented metrics

**Before:**
> Нами была проведена масштабная работа по оптимизации механизма захвата кадров, в результате чего было достигнуто значительное снижение задержки.

**After:**
> Мы оптимизировали механизм захвата кадров и за счёт этого снизили задержку.

**Changes:** passive to active with the named actor («Нами» → «Мы», core rule 7), verbal nouns to verbs; padding removed: «масштабная», «значительное». «В результате чего» states a cause, so the result keeps it («за счёт этого»). «Оптимизировали» claims a result, not just work; the source gives one (lower latency), so the claim is not new. The source has no numbers and no details of the optimisation, so neither does the result; if the author or the code gives them, use them.

## 3. Only the run-up goes

**Before:**
> Важно отметить, что после выхода версии 2.4 количество ошибок таймаута, как правило, снижается примерно на 30%.

**Bad after:**
> Версия 2.4 снизила ошибки таймаута на 30%.

**After:**
> После выхода версии 2.4 количество ошибок таймаута, как правило, снижается примерно на 30%.

**Changes:** the run-up «Важно отметить, что» removed, nothing else; without it the sentence loses no warning, cause, or topic shift (the Run-ups test). The bad version dropped «как правило» and «примерно» and turned "after" into "because of".

## 4. Describing a change instead of the state (README)

**Before:**
> Ранее сервис опрашивал гипервизор каждые 10 секунд, что создавало лишнюю нагрузку. Теперь он подписан на события гипервизора, и это кардинально изменило ситуацию.

**After:**
> Сервис подписан на события гипервизора.

**Changes:** a README describes the system as it is.

**Change list:** cut the history (polling every 10 seconds, the extra load it caused), the judgement «кардинально изменило ситуацию», and «теперь», which only contrasted the present with that history; the history belongs in the changelog or MR description.

## 5. Bold labels and an item with no fact (MR description)

**Before:**
> - **Производительность:** значительно улучшена производительность за счёт кэширования.
> - **Надёжность:** повышена надёжность благодаря повторным попыткам.
> - **Удобство:** улучшен пользовательский опыт.

**After (chat mode):**
> Кэширование улучшило производительность, а повторные попытки повысили надёжность.

**Changes:** the labels repeated the item text. Both causes stay, now as subjects, each with its own verb from the source («улучшена» → «улучшило», «повышена» → «повысили»); padding «значительно» removed. The source says nothing about what is cached or when retries happen, so neither does the result.

**Change list:** cut «улучшен пользовательский опыт»: no fact behind it. Check with the author whether a real change stood behind it.

In embedded mode the text is the same, and the cut goes to the calling task with the warnings instead of a change list (core rule 3).

## 6. Wrong reader (review reply)

**Before:**
> Да, вы правы, это обходит проблему, а не исправляет её. Корень в том, что при переносе дочернего объекта к новому родителю обновляется `parent_id`, но не `pipeline_id`. Я проверил на QA: из 123 переносов неверных строк сейчас 6. Поскольку код общий, правильнее вынести исправление в отдельную задачу, а здесь оставить обходной путь.

**After:**
> Да, вы правы, это обходит проблему, а не исправляет её. Код общий, поэтому правильнее вынести исправление в отдельную задачу, а здесь оставить обходной путь.

**Changes:** the author's agreement stays word for word; the contrast in it stays because both halves carry information (its Exception). The decision now follows a short acknowledgement instead of closing a long reply (genres.md, Wrong reader). «Правильнее» still governs both halves: the opinion does not become a promise («вынесу») or a decision («оставим»). «Поскольку код общий» keeps its own claim. «Оставить обходной путь» stays, though «обходит» stands nearby: «оставить как есть» would read as "change nothing", and a precise repeat beats a vague substitute.

**Change list:** cut the diagnosis (`parent_id` is updated, `pipeline_id` is not) and the QA numbers (6 wrong rows out of 123 moves). They prove the bug, not the decision; put them in the new task.

## 7. Empty contrast and a closing moral

**Before:**
> Это не просто таймаут, а настоящая защита от зависших запросов. Именно в этом его главная ценность.

**After:**
> Таймаут — защита от зависших запросов.

**Changes:** nobody claimed it was "just a timeout", so the negative half only added weight; padding «настоящая» removed. The role stays a role («защита», not «защищает»). Compare E2, where the contrast stays.

**Change list:** cut «Именно в этом его главная ценность»: it adds an evaluation of its own, not a fact (structures.md, Closing morals and dramatic fragments).

## 8. One term, one word

**Before:**
> Инстанс переводится в `stopped_offloaded`. После этого у виртуальной машины нет домена, а у экземпляра остаются только тома.

**Source (the code):** all three words name the same `Instance` object.

**After:**
> Инстанс переводится в `stopped_offloaded`. После этого у инстанса нет домена и остаются только тома.

**Changes:** three names for one object made the reader wonder whether there are three. Without the source line, merging them would be a guess; then ask (core rule 5).

## 9. Technical register: do not cut for rhythm

**Before:**
> Для запуска выполните четыре шага: соберите образ, загрузите его в реестр, обновите тег в манифесте и примените манифест.

**After:** unchanged.

**Changes:** none. Four steps, all needed (core rule 8).

---

## English

### E1. Inflation and copula avoidance (README)

**Before:**
> This service serves as a robust, scalable foundation for VM lifecycle management, seamlessly integrating with the control plane and ensuring reliable operation.

**After:**
> The service is a foundation for VM lifecycle management and integrates with the control plane.

**Changes:** "serves as" became "is"; the role stays a role ("a foundation for", not "manages") and keeps its own noun and article. Padding removed: "robust", "scalable", "seamlessly", "ensuring reliable operation"; the text backs none of them with a property, so they praise (core rule 4). If the source or code says what the service does or how it integrates, name it.

### E2. Throat-clearing and a justified contrast

**Before:**
> Here's the thing: the bottleneck isn't the database. It's the connection pool. Let that sink in.

**After:**
> The bottleneck is the connection pool, not the database.

**Changes:** run-up and closing moral removed. The contrast stays because it corrects what the reader likely suspects.

### E3. Commit message

**Before:**
> This commit successfully implements various improvements to the shelve offload functionality, ensuring robust handling of edge cases.

**Source (the diff, its ticket, and the repo log):** the shelve offload save failed when the task state was one of two states missing from the expected list; the diff adds them to the list in the node service. The repo uses Conventional Commits with the service as the scope.

**After:**
> fix(node): accept two more task states when saving a shelve offload

**Changes:** every word of the subject comes from the source, including the format (the repo's convention) and the type: `fix` because the save failed. A diff that only widens a list does not tell `fix` from `feat`; then ask. With no source at all, ask instead of guessing.

### E4. False agency

**Before:**
> The data tells us that costs rose after the migration. Egress plays a key role in this growth, and the billing logs say most of the egress comes from the new replication job.

**After:**
> According to the data, costs rose after the migration. Egress is a major factor in this growth, and the billing logs show that most of the egress comes from the new replication job.

**Changes:** three *(cluster)* signs meet in one paragraph: two cases of false agency and a significance phrase. The data and the logs no longer "tell" and "say", but each claim keeps its source; no actor is invented. "Plays a key role in" loses the staging and keeps its fact and its rank: "is a major factor in", not just "affects" (structures.md, Significance).
