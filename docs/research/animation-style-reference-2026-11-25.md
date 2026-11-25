# Animation art direction — 26 looks and reusable motion rules

25 November 2026. Research intake from the owner-supplied bilingual PDF **26 стилей анимации — промпты EN / RU**, 29 pages, attributed in the document to «Силиконовый мешок». The printed source uses one underwater mini-submarine reference and a two-stage image-and-motion recipe (p.2), with a style page for each look (pp.4–29). The original source and SHA-256 receipt are retained privately in the studio's `records/reference-intake-2026-11-25/`; no reference images or complete prompt text copied into Git. This is a reading and visual review of illustrated examples, not evidence that 26 videos were generated or that a provider supports them. Rights to the PDF's illustrations and archive assets are not established; use our own new material for trials.

## Transferable method

Separate **composition and continuity**, **look**, and **movement** before generating anything. The source has a fixed object and view, then a per-look still description and matching motion description. The first image can be strong while the sequence fails: its surface may crawl, an object may deform, or the camera may move while the intended action never happens.

For Framewright, choose a single owned reference and write four independent blocks (an original studio template, not copied prompts):

- **SHOT LOCK:** subject identity and important parts, silhouette, anchor position, intended aspect, view direction, relative scale, environment and allowed framing changes. Name what must stay visible; no automatic crop from a portrait reference. Default landscape 16:9 for Radar.
- **LOOK:** material or medium, palette roles and contrast, line/edge treatment, texture location and lighting, intended photographic/illustrative realism. Use generic visual language; do not reproduce a proprietary character, interface, branded toy or recognisable game's assets.
- **MOTION:** start → action → end, duration and cadence; distinguish camera, rigid subject movement, local animated detail and depth layers. Specify which elements must remain fixed and which are allowed to vary. Choose movement appropriate to the medium rather than merely adding a pan.
- **CHECK:** no geometry/identity drift, stable texture anchors, no unwanted text, no occlusion of key details, temporal continuity and readability on a reduced frame. Mark the first-frame decision separately from motion and owner approval.

## Taxonomy and practical uses

The style names are reference vocabulary (English/Russian). Motion and production opportunities below are our own synthesis of the pages, not full prompts. Some entries (exploded view, magazine layout, collage) are treatments/structures rather than distinct animation algorithms. Stop-motion-like output is not proof of physically photographed stop motion.

| # / PDF page | Style | Motion or look control | Framewright use / proposed route |
|---|---|---|---|
| 01 / 4 | Neon sketch / Неоновый скетч | Stable luminous contours, traveling highlight, layered depth | Futuristic HUD or signal insert; SVG/Canvas, glow and parallax |
| 02 / 5 | Comic book / Комикс | Ink silhouette, print dots, rhythmic pose change and anchored graphic marks | Humour, narrative transitions; original ink artwork + layered motion |
| 03 / 6 | Brick-built stop motion / Конструктор | Discrete poses, rigid aligned blocks and incremental mechanical rotation | Product assembly or playful short; generic brick geometry, no branded assets |
| 04 / 7 | Pixel art / Пиксель-арт | Whole-pixel positions, limited palette, sprite steps and no filtered scaling | Retro interface or fictional world; Canvas/sprite sheets; preserve existing RUN//SIGNAL canon |
| 05 / 8 | Chalk on blackboard / Мел на доске | Gradual stroke reveal, restrained chalk variation, stable diagram | Lesson, calculation; SVG strokes and board texture |
| 06 / 9 | Early-2000s low-poly game graphics / Ретро-3D | Faceted forms, distance fog, short camera follow, discrete HUD values | Original game-world or simulation; Three.js/Blender, no specific game asset recreation |
| 07 / 10 | Flat vector / Плоский вектор | Bold shape hierarchy, limited palette, layered parallax | Technical or business explainer; OpenMotion/SVG/GiveMotion |
| 08 / 11 | Continuous line drawing / Рисунок одной линией | Unbroken path, travelling emphasis, anchored contour | Minimal explainer or brand transition; SVG path animation |
| 09 / 12 | Cinematic CGI / Киношная CGI-анимация | Camera arc, reflections follow geometry and light sweep, local action | Technical product hero; Blender/Three.js, or separately tested generator |
| 10 / 13 | Exploded 3D view / 3D-разбор | Fixed camera, parts move along assembly axes, attached callouts, reversible assembly | Hardware, mechanical explanations; editable 3D scene, not random generative geometry |
| 11 / 14 | Paper cutout / Бумажная перекладка | Distinct layers, stepped hinges, clean cut edge | Editorial metaphor, timeline; original textures + 2D layer animation |
| 12 / 15 | Cardboard diorama / Картонная диорама | Foreground occlusion and parallax, rigid miniature, stepped details | Toy-like process visual, geography; staged 3D or layered original assets |
| 13 / 16 | Needle-felted wool / Валяная шерсть | Fibres travel with the surface; gentle stepped posing | Warm whimsical creative short; material-specific image-to-video test |
| 14 / 17 | Plasticine stop motion / Пластилиновый стоп-моушен | Uneven but intentional cadence, stable dents, rigid character parts | Playful narrative or product vignette; stop-motion recipe or one image-to-video test |
| 15 / 18 | Sumi-e ink wash / Японская тушь | Local ink bloom against a stable paper plane and silhouette | Evocative reflective transition; brush reveal/masks or controlled generation |
| 16 / 19 | Ukiyo-e woodblock / Ксилография укиё-э | Contained printed shapes, wood-grain anchoring, layered flow | Landscape/travel illustrative insert; original print design and parallax |
| 17 / 20 | Watercolor / Акварель | Slow wash bloom around stationary material texture; contour remains readable | Atmosphere and travel or historical vignette; layered still with selective motion |
| 18 / 21 | Linocut / Линогравюра | Cut marks stay with object; paper grain fixed; restrained pose changes | High-contrast news illustration or graphic essay; own carved-print look + layers |
| 19 / 22 | Archival photo collage / Коллаж из архивных фото | Separate cutouts and uneven edges anchored to planes; parallax | News, historical and research explainers; only rights-cleared actual photos/footage, distinguish illustration from evidence |
| 20 / 23 | Vintage magazine page / Винтажная журнальная полоса | Print grid and page held stable, selective picture animation/push-in | Editorial research/video essay opener; own typography, layout and images |
| 21 / 24 | Two-ink risograph / Двухцветная ризография | Two ink roles, controlled overlap and intentional temporary misregistration | Distinct bold editorial visual family with strong palette rotation; compositing/SVG |
| 22 / 25 | Gouache and colored pencil / Гуашь и цветные карандаши | Matte shapes stay steady; limited variation in hatch lines | Educational story or authored illustrated film; layered art + discrete animation |
| 23 / 26 | Scandinavian folk painting / Скандинавская народная роспись | Ornaments remain attached to subject, repeating rhythmic motif | Decorative creative or seasonal vignette; original motifs, vector layers |
| 24 / 27 | Cyanotype / Цианотипия | Fixed paper boundary, contact-print silhouette and controlled tonal change | Archival/science metaphor; 2D colour treatment, clearly illustrative |
| 25 / 28 | Stained glass / Витраж | Glass geometry/lead seams locked, backlight moves across panes | Intro or emotional transition; masked lighting in original artwork |
| 26 / 29 | Blue-and-white porcelain / Сине-белый фарфор | Glaze highlights respond to camera orbit, surface motifs remain attached | Product or crafted material showcase; original staged 3D or bounded image-to-video |

## First experiments (not yet executed)

**STYLE-ROTATION-01** (M3/M4, existing Radar visual-rotation practice): one owned neutral subject with 3–5s landscape action and matching framing. Compare the present baseline with three materially different directions as independent candidates: magazine/collage (19/20), two-ink risograph (21), and tactile diorama/cutout (11/12). Each has a different purpose and medium. Produce a small native-size/contact-sheet still first, then animate the same named action at matching duration. Keep colour treatment, motion cadence, actual camera/stage constraints and tool/version/source in the existing brief. Use authorized photographs where relevant; a moving graphic is not a substitute for real documentary evidence. Compare immediate readability, visual variety, motion completion, texture stability and ease of one localized correction; no forced single winner across distinct briefs. Owner sees only final matched probes. Do not run all 26 or generate any paid assets by default.

**Reuse path, not a new standalone production:** for a selected technical film, use 07/08/10 when geometry and process explanation matter (SVG, editable 3D); for a creative film, trial 13/14 or 25/26 if the style supports story and material. For retro fiction, keep established RUN//SIGNAL identity intact rather than restyling a series on the basis of a reference intake. Consider 2D/3D deterministic routes first when the visual behavior can be represented directly; try generators only for an actual need and test first-frame-to-motion fidelity. Verify generated typography/diagrams; prefer separately typeset shot labels.

This is a reusable reference, not an owner mandate to make every future video one of these styles or change approved masters. [Existing visual standards](../video-taste.md) remain the policy; this is a selectable vocabulary for art direction.
