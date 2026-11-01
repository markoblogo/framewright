# REL-B — повторный продакшн и осмысленное продолжение

1 ноября 2026. Автор принял дополнение текущего REL-B: журнал творческих решений
и проверку продолжения после паузы. Основной порядок сохраняется:
**повторный ролик → измерения → разбор результата**. Это протокол, не результат
проведённого нового продакшна или независимой проверки.

**Текущий итог, 1 ноября:** обе версии приняты; восстановление после паузы и
ограниченный повтор R05 проверены. Производственных доказательств достаточно для
предложения предрелизной подготовки. [Оценка и оставшиеся проверки](../rel-b-readiness-2026-11-01.md).
Датированные pending-состояния ниже сохранены как история, не текущие поручения.

## Основа и границы

Принятая база — [One Artist, Two Cities](two-cities-reuse.md): 33,208 с,
горизонтальный и вертикальный варианты. Повтор использует подходящий сохранённый
шаблон и разрешённые материалы; новый сюжет/монтаж фиксируется до сборки.
Принятие старого фильма не распространяется на новый. Историческое активное время
неизвестно; ускорение и экономия пока не доказаны. Pocket OS остаётся на паузе,
SSI работает отдельно. Новые платные пробы и публикация сюда не входят.

## Журнал творческих решений

Использовать существующие `project.py observe --kind decision --topic …`,
`asset` и `retain`; отдельную систему решений не строить. Заполненный документ
ниже сохранять как материал проекта. Значимые зависимости на источники и версии
указывать явно: журнал не выводит их из вложенных ссылок автоматически.

Одна запись на реальный выбор; отвергнутые варианты сохранять. Не придумывать
альтернативы задним числом, чтобы создать видимость выбора.

| Поле | Что записывать |
| --- | --- |
| ID, сцена / участок, версия | Стабильный ID решения, назначение сцены и конкретные материалы |
| Автор предложения и основание | Автор / агент / внешний источник; ссылка или точная формулировка запроса |
| Варианты | Реально рассмотренные варианты, различия и ограничения; если был один, так и написать |
| Выбор и причина | Что выбрано, какую смысловую или визуальную задачу это решает |
| Что сохранить | Например, голос, последовательность действий, темп, фактура, утверждённый текст |
| Упрощение | Что убрано ради бюджета/времени и почему замысел остаётся понятным |
| Изменение после проверки | Дефект → требуемая правка → версия результата; технический QA отдельно от вкусовой правки |
| Решение по версии | proposed / accepted / rejected / deferred; кто проверил и что действительно принято |

Решение автора о рамках REL-B можно записать accepted с `owner_report`.
Новый творческий выбор агента сохранять proposed до соответствующего согласования;
техническая исправность не превращает его автоматически в авторское принятие.

## Проверка продолжения после паузы

Провести на настоящем промежуточном состоянии повторного фильма, после появления
первых результатов и решений. Не создавать рендер только ради проверки паузы.

1. Сохранить `brief` проекта, версии/хеши, журнал решений, измерения и текущий
   статус проверки. Зафиксировать, что принято, что только предложено и что мешает
   следующему действию. Связать нужные исходники через существующий журнал.
2. Оставить короткий checkpoint: замысел; что защищено от изменений; ближайшее
   допустимое действие и его условия; явные ожидания; вопросы только при нехватке
   данных. Старые ожидания не удалять: отметить их исторический статус.
3. В новой сессии без пересказа чата сначала прочитать инструкции и выполнить
   `project.py brief PROJECT.json`. Записать выбранное действие и его обоснование
   **до** запуска инструмента; отдельно записать фактическое действие/результат.
4. Сопоставить с checkpoint. Проверить сохранение замысла, версий и ограничений,
   отсутствие лишней перегенерации, корректное различение текущих блокировок и
   истории. При реальном пробеле остановить зависимое действие и назвать пробел.
5. Сохранить наблюдение и результат проверки. Если была только проверка отдельным
   процессом, назвать её именно так: она не доказывает независимое агентное
   продолжение. План проверки и заранее написанный правильный ответ — не её прохождение.

**Критерий:** верный следующий шаг с объяснением творческой причины, сохранение
утверждённых элементов и отсутствие неразрешённых действий. Найденных файлов
недостаточно. Любой существенный провал сохранить и исправить; REL-B не закрывать
по одному среднему баллу. Авторский просмотр/прослушивание остаются отдельными.

## Измерения и итог

В существующем журнале хранить фактические интервалы активной работы, настройки,
рендера/ожидания, восстановления контекста и накладных расходов ведения проекта.
Перекрывающиеся интервалы не суммировать дважды. Время чата не равно активному
труду автора; не измеренное — unknown. Указать источник каждого замера.

Для восстановления: старт новой сессии → первое корректное действие; число
повторных вопросов, ответы на которые уже были сохранены; лишние действия и
причины. Для переиспользования: конкретные материалы/оформление/рецепты сохранены,
изменены или созданы заново. Сам факт повторного использования не доказывает экономию.

Итог REL-B связывает новый ролик и альтернативный формат, проверки границ шаблона,
одну ограниченную правку с защищёнными свойствами, наблюдение продолжения,
измерения и уместный повтор R05. Неуспешные пробы сохраняются. Не требуется
проходить всю очередь инструментов. Базовое время неизвестно — ограниченный вывод
без процента экономии. См. [RV01](../post-release-validation.md#rv01-второй-выпуск-точечная-правка-и-продолжение-в-новой-сессии).

## Отдельная небольшая задача DOC-ENTRY-01

После разбора REL-B привести входы в документацию к трём путям: начать / продолжить /
исправить. Сверху — текущее состояние, подробная история — по ссылкам. Сохранить
доказательства и не переписывать датированные факты как текущие. Завершение:
рабочие ссылки и проверка новым читателем, который находит актуальный следующий
шаг без чтения всей истории. Это RV02/M6, не новый интерфейс, не обязательный
рефакторинг перед фильмом и не самостоятельный повод для релиза.


## Current repeat — Beyond the Letters (1 November)

Owner selected the proposed concept. New36s English film,16:9 and9:16, uses nine
retained art-media files, the original score and unchanged FFmpeg/Pillow assembler.
New text, shot order, measured phrase placement and fresh offline M1 speech create
a detail-to-architecture essay. Five voice phrases fit their windows without
speed-up. Both864-frame exports decode; eighteen caption-layout checks fit.
Nine horizontal samples were inspected; whole-film owner picture/listening
acceptance remains pending, as does separate portrait crop review.

Actual QA correction: v1 AAC measured-1.06dBTP against the recipe's-1.2target.
Lowered the complete mix0.6dB and encoded new v2 files, preserving all encoded
video packets exactly. Both v2 outputs measure-18.38LUFS /-1.67dBTP and decode.
This is an audio QA correction, not an owner creative request. Originals retained.
Scripted stage timings/source pins and correction receipts are retained privately;
active human labour and baseline effort remain unknown. No savings claim.

The intermediate checkpoint now says to review v2 and preserve approved intent,
not rerender the accepted baseline or regenerate speech. The independent
meaningful-continuation check and R05 repeat are still pending. Merely writing this
checkpoint does not complete either. REL-B is not ready to release.


Owner subsequently viewed Beyond the Letters and accepted it as a successful test,
explicitly declining YouTube publication. Horizontal v2 is selected as the accepted
local final with picture/listening owner-report receipts. This statement does not
establish separate portrait review, independent continuation or R05 completion.

### Current reconciliation and continuation preparation

Reopened the current journal after owner acceptance and compared both v2 MP4 hashes
with correction receipts: both match. Saved a new current brief, reconciliation and
continuation-v4 checkpoint privately. The v3 checkpoint's pending-horizontal review
and local-only SSI statements are historical, not current instructions. Horizontal
v2 remains accepted, with no YouTube publication planned; portrait owner review,
actual production template-boundary cases, independent continuation and R05 remain
open. Scripted assembly timings (24.639s / 22.583s) and correction timings
(8.416s / 7.528s) are separate stages, not full production/human labour savings.
No new render, voice, publication, independent-agent pass or release inferred.

Latest owner direction: SSI is preparing one internal revised-template test; guide
embedding is in progress. Await owner reports instead of producing duplicate work.
Future guide automation and channel learning are staged in the roadmap, beginning
with TikTok and dual-format planning for the next selected book animation.

### Bounded template controls and independent continuation — 1 November

Frozen a one-scene opening-caption contract from the accepted horizontal v2 using
existing templates.py. Reused unchanged production-reuse renderer for six actual
3s controls: short/maximum text and absent optional **voice**, in16:9 and9:16.
Required artwork remains present; absence of voice becomes locally generated
silence while the original instrumental remains. No new voice/model/service.
Both required-artwork omission and over-limit headline are rejected. Render/decode
and inspected mid-shot geometry pass in this scope. Long headline96chars plus
subtitle64chars fits the panel but **3s is not a reading-time pass**. A duration/text
limit policy and separate editorial review remain necessary; no whole-template or
narration-replacement qualification. Unknown new-use rights remain internal-only.
Original accepted masters were not changed. Private packets, plans, six MP4s,
contact sheet and review-and-negative-controls.json retain the evidence.

With direct owner permission, a fresh agent without chat history independently
read instructions/project, ran brief/blockers, hashed both v2 files and recovered
the narrative, selected horizontal version and explicit no-YouTube decision. It
correctly chose review of existing controls/portrait instead of regeneration.
It exposed obsolete preparation prose and distinguished prepared packets from
later actual renders; the current summary was refreshed with continuation-v5.
The real project evolved as controls completed; this is a bounded read-only
continuation pass, not frozen whole-route execution or general agent reliability.
Recorded pause-continuation done with retained independent report. Portrait owner
acceptance, design/long-copy timing, R05 repeat and result review remain open.
REL-B has not reached its release gate. Current-session source pins still match.

### Long-copy timing rule and portrait preparation

Added an opt-in English-copy preflight to the existing production-reuse recipe.
It combines title/subtitle word and nonspace-character budgets, minimum hold and
transition time, rounds to frames and rejects invalid duration. The render guard
fails before output/media access when enabled. It never automatically retimes an
accepted plan; revised narration/music/source ranges require separate checking.
CLI regressions cover long/short copy, unbroken text, invalid timing and guard order;
existing label tests remain green. This is an authored heuristic, not a reader study.

The exact long-copy controls move from3s to9.75s in new16:9/9:16 plans; both render
and full decode pass. No newly generated voice: explicit silence replaces old
speech in these stress samples, original score retained. Old3s controls and accepted
masters remain. Preflight of the accepted film flags one4s caption against4.4167s;
retain as advisory disagreement, not retrospective rejection or automatic editing.

Portrait v2: inspected one encoded midshot frame for each of9scenes; captions and
subject framing are retained in inspected samples, without observed clipping.
AAC packet hashes match the owner-accepted horizontal film. This does not establish
full temporal/subjective acceptance. A dedicated36s portrait review page is open and
owner picture/listening decision has been requested; keep pending until answered.

### Portrait owner acceptance — 1 November

Owner explicitly answered “Принимаю вертикальную версию” to the request to view
all36s with sound and assess framing, copy, pacing and audio. Exact portrait v2
now has owner-reported creative/listening acceptance; its review wait is closed.
Both aspect variants of Beyond the Letters are accepted internal tests, with no
publication planned. Horizontal selected final is unchanged; portrait acceptance
does not replace it or confer publication permission. R05 repeat and final REL-B
result/gate assessment remain open; template design/control approvals are separate.
