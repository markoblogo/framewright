# Good Dog — сюжетная карта v1

**Current status,1November2026:** accepted v8; owner-reported YouTube publication. Production case closed. [Retrospective and next-film tests](good-dog-closeout.md). Earlier entries below are dated history; they do not reopen accepted decisions.

Рабочая адаптация исходного рассказа:178с,16:9, английская озвучка и тексты. Иллюстрации трилогии задают визуальный язык, не заменяют сюжет прочитанного рассказа. Город, один рассказчик и финальная рифма — решения адаптации, не цитаты из книг.

**Смысл:** человек считает себя дрессировщиком; цепочка вознаграждений превращает его в управляемого участника собачьей системы. Финал мрачный, без натуралистического насилия.

| Время | Ключевой кадр | Сюжетное изменение | Движение / материал |
|---|---|---|---|
|0–14с|K01 · Находка|Собака замечает свёрток, человек ставит миску. Обмен кажется добрым.|Dog sniffs; bowl makes one contact; dog raises eyes. PixVerse retained + next Flow shot.|
|14–30с|K02 · Кто кого ждёт|Еда уже на полу, но собака смотрит на человека; именно человек ждёт её решения.|Dog gaze to man; man leans forward; restrained pause, no talking dog. Flow image-to-video first; PixVerse next daily slot fallback.|
|30–48с|K03 · Маршрут|Собака выбирает дорогу и останавливает человека; он послушно следует.|Real forward travel, one stop and look back; match screen direction. Odyssey selected third-person + compatible World Labs/Marble passage.|
|48–66с|K04 · Система вознаграждения|Небольшой личный обмен превращается в повторяющийся распорядок.|Two different short actions, repeat match cut, clock advances; no drug contents. I2V provider comparison; local time/clock overlay.|
|66–82с|K05 · Масштаб|У дверей уже несколько людей со своими собаками: люди думают, что построили сеть.|Foreground turn and background travel in separate layers; avoid crowd morphing. Keyframe + short I2V; local layered fallback.|
|82–100с|K06 · Перехват управления|Без очередной награды люди стоят и ждут. Собака одним движением запускает выдачу.|Dog operates one large accessible lever; one packet enters tray, man reacts. Blender or PlayMCP controlled scene; Teardown mechanism candidate.|
|100–120с|K07 · Открытие|Тот же принцип виден внутри фабрики: собаки наблюдают, люди обслуживают линии.|Camera reveals connected conveyor path and switches from human eye level to dog eye level. PlayMCP candidate / existing Blender fallback; optional Teardown insert.|
|120–138с|K08 · Попытка отказаться|Герой отходит от очереди. Выдача останавливается, все смотрят на него; он возвращается.|Man one step away, tray closes; next shot his hand returns to station. Flow I2V split into short actions; precise local tray animation.|
|138–158с|K09 · Цена системы|За стеклом готовый корм и обозначение происхождения. Человек понимает, что людей считают ресурсом.|One tin moves under inspection lamp; readable label added locally, not generated. Blender/Three.js repeatable prop shot; StableGen texturing optional later.|
|158–178с|K10 · GOOD HUMAN|Возвращаемся к первому обмену: собака теперь у рычага, человек садится ждать. Роль хозяина перевёрнута.|Dog gaze, lever movement, human sits; subtle room action; fade only after reveal. Flow matching keyframe + local title/sound.|

## Как избежать слайд-шоу и несвязанных миров

Десять картинок — опорные состояния, а не десять неподвижных планов по18с.
Каждый блок состоит из2–4 коротких планов: действие, реакция, деталь, переход.
Итого ориентир25–35планов, преимущественно3–8с. Длительность уточняется после
первых склеек: не растягивать материал ради трёх минут. Генерировать по одному
связанному фрагменту, сохранять удачный и менять исполнителя при конкретном сбое.

Сначала K01→K02: уже понравившийся PixVerse и новый кадр ожидания/взгляда.
Для второго кадра проверять существующий Flow до расхода: модель, цена, доступ
по текущим250бонусам. Последний принятый кадр и описание объектов — референс
следующего. Повторно оживлять всю исходную картинку разными сервисами полезно
для сравнения, но это ещё не следующая сцена истории.

Сохранять сторону оси, положения миски/свёртка, одежду, шерсть и масштаб.
Odyssey и World Labs/Marble использовать как обозначенные самостоятельные
планы пути, без обещания общей точной географии. Лес уместен только как реальный
участок маршрута/поиска; не вставлять его ради наличия. Сначала просмотреть уже
созданные миры. Не допускать статичного ожидания, обратной походки, рывка камеры
или объяснения неслучившегося действия одной озвучкой.

## Роль уже использованного и нового инструментария

| Задача | Основной маршрут / резерв | Проверяемое новое |
|---|---|---|
|Ключевые изображения, герой и следующий ракурс|Встроенная генерация с референсами; существующие иллюстрации не изменять|Сохранение паспорта через несколько картинок, а не только похожий стиль|
|Живые действия K01–K06/K08/K10|PixVerse + Flow по имеющимся бонусам; Raphael внутренний сравнительный тест; Dreamina/Vidu/Kling/SeaArt/Vidnoz после проверки конкретной бесплатной операции|Разделить сдвиг камеры, анатомию, контакт и фактическую длину файла; права отдельно|
|Движение по миру K03/K05|Сохранённые Odyssey и World Labs/Marble; новый мир только при нехватке|Монтаж независимых миров без ложной непрерывности; стабильная камера|
|Механизмы и фабрика K06–K09|PlayMCP после проверки текущего доступа/стоимости, либо локальный Blender/Three.js; Spline при реальном преимуществе|Teardown: связанный привод→рычаг→выдача; StableGen: текстуры одного реквизита при подходящем сервере|
|Сборка, звук, контроль|FFmpeg/существующий монтажный маршрут, локальная EN-озвучка, авторские шумы/музыка, DJV по пригодности|Ритм поворота управления, совпадение контактов со звуком, сохранение точных версий и замечаний|

OpenAI Sora исключена из текущего плана после проверки официального закрытия.
Google AI Studio/API не получает автоматически лимит Google AI Plus; Flow —
отдельно проверенный интерфейс. Платные маршруты не запускаются без бюджета.

## Озвучка и переходы

Английский черновик по каждому повороту и промпты всех картинок:[story-map-v1.json](../../examples/good-dog-pilot/story-map-v1.json).
Сначала тёплый человеческий рассказ и миска/шаги; затем ритмический повтор,
пауза при остановке выдачи, механический пульс фабрики, тесный почти бесшумный
финал. Надпись GOOD HUMAN. добавлять при монтаже, не запекать в картинку.
Происхождение корма показать через локально оформленную этикетку и реакцию,
без крови и анатомических подробностей. Это законченная сатирическая развязка,
не открытый финал и не счастливая история о спасении.

## Следующий исполняемый шаг

Картинка K02 создана по сохранённому герою/декорации и удержана в журнале; приёмка пока не получена. Далее сверка объектов и оси →
короткий Flow I2V при подтверждённой стоимости → склейка с K01 → просмотр.
Далее K03/K04, а не параллельная генерация всех сцен. Новые инструменты остаются
кандидатами, пока не пройден их узкий тест. Публикация и финальная приёмка отдельно.


[Teardown/StableGen assessment](../research/teardown-stablegen-2026-10-31.md) · [Previous trials](good-dog-preproduction.md). Working proposal; not final narrative/canon or whole-film acceptance.


## Серия опорных кадров готова31October2026

K01/K02 переиспользованы; K03–K10 созданы отдельными reference-guided изображениями. Все10 файлов1672×941 проверены на открытие, сохранены по номерам с хешами и EN-промптами движения в частном производстве. Картинки ещё не приняты как канон и не доказывают движение. Выражения и реквизит сверяются в соседних видеокадрах.

Кандидаты анимации: K03 — реальная проходка/Odyssey; K04 — жест I2V плюс локальные часы; K05 — ограниченный I2V или независимые слои; K06 — точный рычаг/выдача Blender/Three.js/Teardown/PlayMCP; K07 — управляемая камера/конвейер; K08 — короткий поворот человека, отдельная заслонка; K09 —3Dбанка/лента/свет и точная этикетка; K10 — небольшой взгляд/дыхание, титр и затемнение в монтаже. Это план распределения, не отчёт об испытании этих инструментов.

## First keyframe animation trials — 31 October 2026

Owner accepted the ten-image series and authorised proceeding. K02 produced one actual4s1280×72024fps clip in Google Flow using Omni1.1Flash, first-frame input and UI quote7 existing-plan credits. No new purchase; actual account debit not independently reconciled. Original retained; generated audio excluded from the film candidate. Sampled frames show head/gaze/posture change; owner motion acceptance remains pending.

K06: original Three.js r186/MIT procedural mechanism rendered96frames, with three identical reseeks. Its schematic style/limb failed the operator visual fit check, so it is retained as technical/negative evidence. An illustrated2.5D fallback preserves the approved K06 characters and machine, moves a single packet and deforms the attached paw/paddle region; original procedural foley added. It is not physical simulation or a qualified final insert. Outlet reconstruction, packet contact, temporal edges and listening still require review. No Teardown/PlayMCP deployment or new dependencies.

## Route, exchange and motivated style inserts — 31 October 2026

Owner accepted the2.5sdeep-tray dispenser after correcting occlusion: packet disappears behind the front wall; bottom-impact cue retained. This is2.5D illustration animation, not physical simulation.

K03/K04 each produced an actual4s720p24fps first-frame clip in Flow/Omni1.1Flash, quoted7existing-plan credits per job. Original files and AAC retained; film candidates silent. K03 sampled forward travel/head turn and K04 sampled hand/packet contact; full motion approval pending. Existing Odyssey79–82srunning plate also retained as comparison; its native16fps and differing style/human absence remain limits.

At owner request, added local subjective inserts:2sluminance false-colour with animated scent points, and alternate128×45ASCII version from the same cropped Odyssey47–49splate. These are artistic perception, not thermal measurement or biological canine-vision claims. No robot was added to the story.3.5smonochrome comic cutout uses a supplied book panel and canonical PictiqSVG sequence move_feet→rel_here→punct_question, with original nonverbal synthetic creature cues. Reference:[Pictiq](https://github.com/markoblogo/pictiq). No pronunciation system or new sentence translation claimed.

Two18sstyle assemblies alternate ordinary picture, comic communication and sensory perception before route/exchange/dispenser. They are review candidates, not a complete film or proven continuous geography. No new dependencies, paid API purchases or publication; creative/listening checks pending.

## Rounded Pictiq and factory-process insert — 31 October 2026

Owner accepted the three natural canine barks and selected ASCII picture. Pictiq tiles revised to transparent rounded exteriors with thin white contours; interior canonical glyphs preserved. All corner alpha values checked zero; selected montage AAC stream copied exactly, including barks and tray impact. New contour picture awaits owner review.

Two actual4s720pFlow/Omni1.1Flash clips extend the story: other dog/human pairs repeat the exchange, then the main dog observes human factory workers. UI quote7existing-plan credits each, no purchase; actual debit un-reconciled. Original AAC retained but visual trial candidates silent.

At owner request, inserted a separate6soriginalThree.js reward-cycle diagram: moving tokens, FIND/REWARD/REPEAT nodes, then dog-paw CONTROL linked to reward. This intentionally differs from the canonical world and explains the fictional process. [Reusable original scene](../../examples/good-dog-pilot/reward-cycle/README.md). Three reseeks matched;v1 label crowding corrected in v2. Not physics or behavioral-model validation. Network→diagram→factory14sreview remains pending creative assessment and later narration/score.

## Conveyor/diagram revision and pixel-effects intake —31October2026

Owner requested factory→diagram→factory, glossier presentation and continuous
mechanism sound. New10s candidate uses2s cropped factory,6s polished Three.js
diagram and2s wide factory. Clearcoat/metal materials, local procedural studio
lighting and rounded geometry preserve the abstract explanation.144-frame diagram
render had no page errors and three identical reseeks. Assembly decodes; listening
and creative acceptance remain pending.

A single10s window of Kinoton’s [Industrial Conveyor Belt](https://freesound.org/people/Kinoton/sounds/519027/)
(CC0 file page; HQ MP3 preview) continues across both cuts, with a -25LUFS target
and short boundary fades. Raw media and source/profile records stay private; no
raw-stock redistribution. Full-film narration and final ducking remain future work.

[PixelFX/Codex recipe](../research/pixelfx-codex-2026-10-31.md), PIXELFX-01,
records an optional motivated reward accent or ASCII transition. Research only,
not used in the new factory candidate. Preserve canonical Pictiq and accepted
barks. No copied upstream skill/code or new global dependency added.

## Accepted fragments and ASCII terminal sound —31October2026

Owner accepted the reviewed fragments (rounded Pictiq and factory/glossy-diagram
link); requested one audio addition to the ASCII view. New18s style-linkv4 copies
the accepted picture stream exactly and adds a locally authored2s retro terminal
cue at5.5–7.5s: soft square bleeps, scanning tone and brief data chatter. No film
samples, external service or new dependency. Accepted barks/tray impact preserved
in the source mix; pre-encode PCM outside the window is identical. AAC is
re-encoded, so output audio byte identity is not claimed. Full decode and picture
stream hash pass. New sound awaits listening acceptance; full film remains open.

Owner subsequently accepted the ASCII retro cue ("звук ок"). Listening gate for
this revision is closed. Next priority: remaining dependency/reveal beats and
a complete story draft with English narration; defer new tool trials until the
whole-film edit exposes a concrete need. No full-film acceptance inferred.

## First complete story draft —31October2026

Owner authorised finishing the remaining story and a full English-voice draft,
deferring new experiments. A107s draft now connects all ten turns: discovery,
waiting, route, routine, network, dispenser control, factory, failed refusal,
non-graphic pet-food reveal and GOOD HUMAN payoff. This is an adaptation of the
original short story; trilogy manuscripts have not been read.

K08/K10: two new4s720p first-frame clips via the already-used Flow Omni1.1Flash
route. Each UI quote7existing-plan credits, no purchase; actual debit not
reconciled. Source AAC retained privately and excluded from the film. K09: local
Three.js tin/conveyor close-up with an authored readable HUMAN ORIGIN label.
First label angle was wrong; a corrected second render is retained. Existing
accepted mechanism, comic/Pictiq, natural barks, ASCII terminal cue and glossy
factory link are reused. No PixelFX or other new tool trial was started.

Narration: offline Supertonic-3 M1 from retained weights,10English passages.
Original sparse score changes from a warmer minor pulse to a low dissonant drone;
conveyor recordings and accepted contact sounds remain distinct event cues.
All jobs were sequential on this Mac. Full-film listening/creative acceptance is
pending; source-fragment acceptance does not transfer automatically.

The assembly includes camera moves over retained keyframes as bridging detail
shots. These are not newly animated character actions. The continuous world and
character identity are not broadly qualified. Internal review removed an adjacent
repeat of the waiting shot and cropped baked controls from the Odyssey excerpt.
No public upload, publication kit, commit or release was performed in this pass.

Final internal draft of this pass:v3,107.042s,1280×72024fps. Full decode and
all constituent frame-count checks pass; shot contact sheet/EDL/provenance retained
privately in the journal. The narration now says the man still called himself the
owner, rather than claiming a visible leash. Local links/structural checks are
separate from creative/listening acceptance, both pending for the complete film.

### Whole-film revision after owner feedback — 31 October 2026

The owner rejected v3 as a complete film: weak/unreadable titles, excessive
stills, duplicate clocks, low/crowded diagram, incompatible tin/roller motion,
abrupt payoff and upbeat narrator. Earlier accepted fragments remain accepted;
their acceptance did not qualify the complete edit.

Local corrections retain the original wall-clock rim and animate its one face,
use distressed Rockwell/Baskerville title cards, recolour/recentre the schematic,
and fix the roller axis/contact geometry. Tin travel and roller surface velocity
share one speed; there is no claimed physics simulation. A new minor/industrial
score and retained continuous conveyor recording support the revised narration.

Three additional 8s Flow Omni 1.1 Flash shots (waiting, courtyard, final
lever/packet/reaction) replace long still holds. UI quote:12 existing-plan credits
each; no purchase, actual debits not reconciled. Original audio is retained
privately and excluded. Motion strips were inspected; full creative acceptance
remains pending. No new tool experiment was added to the film.

Voice comparison: macOS Grandpa rejected for quality; lowered Supertonic M1
rejected as too cheerful. The owner explicitly accepted the tired Eleven v4
Spuds Oxley–Grandpa sample, with sparse sighs/exhales. Full narration was generated
and downloaded,130.586s; local Whisper timing is mismatch screening, not acoustic
acceptance. The final line makes the reversal explicit: the human was trained.
The observed ElevenLabs account is Free; publication rights remain a separate
unresolved gate. These renders are internal review material, not a cleared
publication package. No paid plan or API charge was authorised or used.

Private artifacts: `film-revision-02/` retains provider receipts, rejected probe
history, original source files, shot edit list, audio and render checks. Full
revised-film owner listening/creative acceptance must be recorded separately.

Revised review candidate:v7,133.000s,1280×720. All33shot extents match,
3192picture frames and full decode pass; local browser resolves the133s file.
Only9.083s use camera moves over still-image detail shots. Reused footage with
alternate close crops and three new8s motion shots replace the long holds.
The owner has not yet accepted the whole revised film or soundtrack.

Export regression retained: two cuts initially lost one frame; a subsequent
filter-based re-export produced only70.583s of picture against133s audio. That
v6 is explicitly rejected. Corrected shot extents and a copy-based assembly
restore the full picture; v7 has a separate QA receipt. This is evidence for
checking picture extent independently of container/audio duration after assembly.
No release, push, upload or commercial voice clearance was performed.

### Owner corrections — 1 November 2026

v8 preserves133s and the accepted voice delivery. Opening and ending subtitles
now sit inside the same opaque dark title plaque. Two remaining camera-only
stills,4.5–6.5s and36–38.292s, are replaced with existing animated exchange/walk
footage. Sampled frame differences confirm movement; they do not prove natural
motion. The accepted deep-tray impact is reused with its transient near124.125s,
aligned to the final dispenser packet landing. No fresh generation or spend.
Full decode,3192picture frames and all33shot extent checks pass. Title/motion
contact sheet and cut/audio sources retained. Whole-film owner listening/creative
acceptance and the existing ElevenLabs publication-rights gate remain separate.

### Accepted v8 and YouTube preparation — 1 November 2026

Owner accepted v8 and requested the publication package. The retained video is
unchanged (SHA2566326ada5174a971272b4e988a7a4c4d374071de24d92fefd19099e4090dfc1db).
Local package contains the video, a new text-bearing thumbnail derived from K10,
English title/description/tags, English SRT timing from retained ASR, metadata,
rights note and file hashes. Thumbnail generated with built-in image generation;
character/style reference retained, then formatted to1280×720JPEG and checked at
320px. No new paid provider subscription or public upload.

Official ElevenLabs publication FAQ checked again on1November2026: free-plan
output is noncommercial only and requires elevenlabs.io or11.ai in the title.
The prepared title includes11.ai. Commercial release remains blocked for the
current free-plan narration; later payment alone does not license old output.
Owner creative/listening acceptance and public/commercial permission remain
separate. Subtitles are prepared from ASR; no independent full subtitle listening
claim. The thumbnail itself has not yet received separate owner acceptance.
https://elevenlabs.io/docs/help-center/legal/can-i-publish-the-content-i-generate-on-the-platform

### Owner-reported YouTube publication — 1 November 2026

Good Dog: https://youtu.be/WxEa5q_PPOk (video ID: WxEa5q_PPOk).
Owner supplied the publication URL after accepting v8 and receiving its package.
Linked to the retained accepted v8 in the project journal. Uploaded file identity,
visibility, monetization, attribution and current provider-rights compliance were
not independently checked; publication does not resolve the separate voice gate.
