# James Game Center — Visual & Asset Bible v1.0

## Jamesy The Hulk Racer | Storybook arcade / 2.5D

Prepared September 28, 2026. Direction approved; production specifications v1; individual artwork and runtime integration still subject to the gates below.

**Runtime status:** This package does not modify the deployed racer, player roster, sign-in flow, scores or Firebase rules.

## 01 / THE NORTH STAR — Storybook charm. Arcade clarity.

One familiar little hero, authored character art, a fast readable route and a sense of depth. The visual reboot must bring the playable game closer to the warmth of the original Jamesy reference.

### Approved direction

The owner has approved an art-bible-first process and a faux-3D / 2.5D direction. Five James costume families and three worlds are in scope. This bible defines version 1 of the production specification; individual costume sheets, animation frames and final UI artwork still need visual review.

### What 2.5D means here

Use a simple dimensional track for perspective, with illustrated or pre-rendered character and object images that face the camera. Separate scenery layers move at different rates. Soft ground shadows, careful scale and authored lighting create volume without rebuilding the child as a detailed real-time model.

### What this handoff does

It establishes the visual rules, five costume briefs, three world briefs, exact first-hero animation list, asset register, review tooling and implementation gates. It does not replace the running game or claim that final sprites already exist.

### Order of importance

Jamesy identity first; clear pickups and hazards second; stable animation third; atmosphere fourth; decorative effects last. Reduce scenery and effects before reducing control readability.

> Decision rule: a still image that looks impressive but fails at running speed is not finished game art.

## 02 / SOURCE OF TRUTH — Protect what already works.

This reboot changes presentation. It must not accidentally replace the account system, rename stored worlds or erase existing progress.

### Canonical names

Hub: James Game Center. Game: Jamesy The Hulk Racer. “Hulk-Racing” is a working shorthand only, not a new release title. New world display names in this bible are proposed labels; stored IDs and indices stay park / 0, cavern / 1 and volcano / 2. [R3]

### Preserved account behavior

The current repository uses the v1.3 email-and-nickname flow with Anonymous Authentication and Realtime Database. Sean is the sole initial Master; additional players are explicitly added by the master. Keep Hall of Fame and player cards. Do not reintroduce the obsolete Firestore / Google-sign-in plan. [R1, R2]

### Do not reset anything

Keep practice, registered records and queued uploads separate. Do not import family or SUJA accounts, create sample scores, seed extra players or change live Firebase rules for an art update. Private matching credentials stay outside public source and artwork. [R2]

### Version and review

Baseline racer: 47d8291…; baseline hub: 40a1f4b…. Full commit IDs are in sources.json. Preserve main while artwork and the isolated preview are reviewed. Re-check the latest application interfaces before integration; do not assume the snapshot never changes.

> No Firebase action is needed to review this art bible or run the asset tools.

## 03 / CHARACTER ANCHOR — Jamesy must stay Jamesy.

Use the supplied cartoon as the identity anchor, not as a photo, a sprite atlas or evidence that a production model exists.

Reference in the supplied PDF / package: `references/jamesy-character-reference.jpg`. Identity reference supplied in the conversation. Only screenshot borders were cropped. Not a gameplay sprite.

### Keep these identifiers

Swept orange-red hair; large blue eyes; warm fair skin; friendly child face; open eye mask; compact heroic stance. The white 4 is the chest emblem and the white J is the belt mark. Do not age him up or substitute a generic superhero.

### Proportion target

Aim for about 3.5 head-heights overall, with a large expressive head, short limbs, rounded boots and padded hands. This is a production target to align designs, not a measurement claim about every reference view.

### Lighting and material

Upper-left soft key light, broad highlights, gentle ambient shading. Use toy-like fabric, rubber and rounded armor, not skin pores or hard photoreal metal. Keep a subtle dark edge so the character separates from bright scenery.

> Camera views: front / three-quarter for menus; rear / rear-three-quarter for racing. “Faces the camera” describes the image plane, not a front-facing character pose.

## 04 / FIVE COSTUMES — One child. Five silhouettes.

These are written design briefs, not five finished character models. Hair, face, eye color, age, scale, 4 shield and J buckle stay consistent across the roster.

| Costume family | Silhouette and identity | Release order |
| --- | --- | --- |
| Jamesy The Hulk | Broad padded gloves, rounded purple shoulder armor, a full purple cape with green lining. | Hulk-first slice |
| Jamesy Spider Style | A light, tapered silhouette, small gloves and agile boots; no cape. | Expansion after slice |
| Jamesy Captain Style | A friendly round shield held to one side, sturdy boots and a short shoulder mantle. | Expansion after slice |
| Jamesy Iron Style | Rounded child-sized armor with glowing wrists and compact boot thrusters; no enclosing helmet. | Expansion after slice |
| Jamesy Super Style | The longest cape, rounded boots and an open, uplifting pose. | Expansion after slice |

### Costume versus identity

Change costume materials, cape length, movement attitude and effect motifs. Do not change the child’s face or body scale to make the variants different. Use the same grounded hitbox for the first comparison pass.

### No silent mirroring

The 4 and J must never reverse. Left and right lean poses are separate drawings. A shield hand, belt pouch or asymmetrical hair sweep must remain consistent from view to view.

### Character-select rule

Show Hulk as the playable first hero. Other designs may appear as clearly labeled “In development” candidates only; they must not look selectable before animation and gameplay are ready.

> The working labels Spider Style, Captain Style, Iron Style and Super Style are costume families, not promises of finished abilities.

## 05 / HERO A — Jamesy The Hulk

The first production hero. Preserve the supplied green-and-purple costume, then make every action read from the racing camera.

### Costume lock proposal

Emerald eye mask and suit; purple forearms, shoulder pads and boots; purple diamond with a white 4; green utility belt with a white J. Keep the face and orange hair exposed.

### Performance

A confident, buoyant run. Strong steps without angry facial acting. Weight comes from anticipation, contact and recovery, not screen shake.

### The four moves

Mighty Leap gives a readable takeoff and soft landing. Jamesy Smash has a visible windup, forward contact and recover. Thunderclap gathers the hands before a thin expanding wave. Super Jamesy Rush adds a soft aura and short trailing accents without changing body size.

### Power language

Retain the current thresholds for the first visual slice: 10 begins a faint spark, 25 unlocks Smash, 65 adds Thunderclap and the magnet, and 100 triggers Super Jamesy. These are existing rules, not new balance decisions. [R3]

### Reject these variations

Adult bodybuilder proportions, torn clothing, angry rage face, green skin, enormous fists hiding the face.

### First proof, before a full sheet

Approve a front-three-quarter pose, a rear pose, a rear-left lean, a rear-right lean and a Smash contact pose. Compare all five together at the intended on-screen size. Only then expand to the 64-frame animation package.

> Hero dimensions, anchor, costume details and view angle must be approved together; fixing them after 64 frames multiplies rework.

## 06 / HEROES B + C — Agility and courage.

Expansion briefs keep the same Jamesy child and readable race controls. Specialized abilities are proposals for a later gameplay pass.

### Jamesy Spider Style — costume

Red open eye mask, red-and-blue suit with restrained web-like seams. Keep his orange hair and face visible. Use the same white 4 shield and J buckle; do not replace them with another hero logo.

### Motion and powers

Springy, precise and playful. Compact landings, tilted shoulders and curved motion trails. Proposed moves: Spider Leap, Web Dash, Web Burst, Spider Rush. Keep web trails thin and behind the character.

### Spider exclusions

An enclosing full-face mask, a different boy, copied franchise symbols, literal sticky webs that obscure the racing route.

### Jamesy Captain Style — costume

Royal-blue open eye mask and suit with red and warm-cream accents. White 4 on the chest and on his own circular shield; J buckle. Orange hair exposed, no full helmet.

### Motion and powers

Purposeful, balanced stride; a clear shield windup and a gentle recovery. Shield remains separate from the collision footprint. Proposed moves: Heroic Leap, Shield Bash, Shield Wave, Captain Rush. The shield can overlap his body, but cannot hide incoming objects.

### Captain exclusions

Shield over the face, copied shield insignia, combat realism, shield-sized collision boxes.

> First compare costumes with the same rules and hitboxes. If future abilities affect scoring, define fair ranked categories and a rules-version plan before release.

## 07 / HEROES D + E — Bright technology. Open skies.

Expansion designs should add personality without becoming a different game or a different child.

### Jamesy Iron Style — costume

Red-and-gold toy-like plating over a flexible undersuit; red eye mask; restrained cyan wrist and boot lights. White 4 chest shield and J belt remain readable.

### Motion and powers

Soft mechanical timing, quick hops and short boost trails. The run must still read as the same child. Proposed moves: Booster Hop, Repulsor Push, Pulse Wave, Booster Rush. Keep exhaust trails short and away from item silhouettes.

### Iron exclusions

Adult armored proportions, a sealed helmet, harsh gunfire, realistic weapons, overly tiny plating details.

### Jamesy Super Style — costume

Cobalt mask and suit; red boots and cape with a golden lining; gold diamond with a white 4, and white J buckle. Keep the common face, hair and body scale.

### Motion and powers

Floaty anticipation with decisive landings. Cape stays behind the child and below the HUD. Proposed moves: Super Leap, Wind Push, Sky Wave, Sky Rush. Flight-like actions stay tied to the grounded lane system until a separate movement design is approved.

### Super exclusions

An adult physique, copied chest insignia, a cape wider than the safe play corridor, damaging eye beams.

> Do not copy familiar franchise logos or interface artwork. Jamesy’s own 4 shield and J mark remain the unifying symbols.

## 08 / ANIMATION — A complete first-hero package.

64 unique frames across 12 states. Fast run reuses the run cycle at a higher playback rate; the intro reuses menu idle. These are planned drawings, not generated assets.

| State / view | Frames | Rate | Playback |
| --- | --- | --- | --- |
| Rear idle / rear | 4 | 6 fps | Loop |
| Run / rear | 8 | 12 fps | Loop |
| Lean left / rear left | 4 | 12 fps | Loop |
| Lean right / rear right | 4 | 12 fps | Loop |
| Jump / rear | 6 | 8 fps | One-shot |
| Land / rear | 3 | 12 fps | One-shot |
| Smash / rear | 8 | 12 fps | One-shot |
| Thunderclap / rear | 6 | 12 fps | One-shot |
| Power-up pose / rear | 6 | 12 fps | One-shot |
| Bump reaction / rear | 3 | 10 fps | One-shot |
| Victory / front three quarter | 8 | 10 fps | One-shot |
| Menu idle / front three quarter | 4 | 6 fps | Loop |

### Animation acceptance

No face drift, hair swapping, reversed emblems, changing limb lengths or moving ground pivots. Run contact frames must match the footfall timing. Test at normal and half speed on light, dark and checker backgrounds.

### Physics owns movement

Keep each pose anchored consistently inside its frame. The engine moves the entity for jumping and lane changes; do not bake that same world displacement into the sprite and apply it twice. Contact FX follow the gameplay event, not a new collision rule.

> Frame timing is a first-pass proposal. Retiming an animation must not silently change hit windows, cooldowns or score events.

## 09 / EFFECTS — Power without visual noise.

Glow should support Jamesy, not wash him out. Effects remain separate assets so their intensity can be changed without regenerating every hero frame.

| State | Visual treatment | Must stay clear |
| --- | --- | --- |
| Baseline | No aura; readable green silhouette and soft shadow. | Face, cape edge, ground contact |
| Spark / 10 | Sparse foot sparkles, faint rim. | Approaching treasure trail |
| Smash / 25 | Short dust puff and outward ground accent. | Obstacle edges and route |
| Charge / 65 | Soft green glow; thin secondary violet accents. | Pickups and center corridor |
| Super / 100 | Brighter controlled aura and brief trails, no size jump. | The same hitbox and controls |

### Standard effects

Limit persistent glows; cap visible decorative particles at 32 initially. Avoid full-screen white flashes, repeated brightness pumping, heavy electricity and camera shake. A power cue must also be visible in the meter and ability icon.

### Gentle Effects

Remove decorative particles, shake and expanding rings; reduce aura intensity and parallax. Keep useful pickup confirmation, cooldown state and hazard information. Respect the reduced-motion preference when selecting the first-run default.

### Safety review

Design for no strobing in any mode, then inspect a capture of the combined effects. A gentle toggle does not excuse unsafe default flashing. Treat the WCAG flashing and interaction-motion guidance as review criteria, not a certification claim. [A1]

> No flashing invulnerability. Use a steady outline, soft tint or icon instead.

## 10 / WORLD 1 — Emerald Skyway

Warm, welcoming, adventurous. A sunlit park and friendly city skyline with bridges and water.

Reference in the supplied PDF / package: `references/emerald-concept.jpg`. Earlier AI concept: atmosphere and finish reference only. Its embedded HUD and numeric values are not the approved interface.

### Light and track

Golden upper-left key, soft teal fill; keep foreground brighter than distant skyline. Warm cream panels, emerald lane accents and restrained purple wall bands. Broad forward chevrons, not a dense flickering checkerboard.

### Separate scenery layers

Sky and soft clouds / Distant city silhouettes / Bridges and water / Tree clusters and lampposts / Track-side shrubs and banners / Sparse foreground leaves. These must be authored as separate images with suitable overlaps, not cut arbitrarily out of one flattened screenshot.

### Pickups and hazards

Collect: Green power gems, Golden stars. Dodge: Mossy stone blocks, Dark violet bumpers, Purple goo. A safe opening, then pickups, one hazard family at a time, jumping, Smash and the first full-power rush.

> Storage remains park / index 0. Existing display label: Emerald Park. New display name is proposed; no data migration.

## 11 / WORLD 2 — Crystal Cavern Run

Wonder, not fear. Luminous crystal architecture with clear blue-green passages.

Reference in the supplied PDF / package: `references/cavern-concept.jpg`. Earlier AI concept: atmosphere and finish reference only. Its embedded HUD and numeric values are not the approved interface.

### Light and track

Soft cool key from upper-left; cyan fill and violet rim. Pickups remain brighter than scenery. Desaturated teal floor with broad violet bands. Do not use tiny sparkle patterns across the full track.

### Separate scenery layers

Dark blue cave shell / Distant luminous arches / Waterfall and mist veil / Tall crystal columns / Small edge crystals / Occasional foreground mineral silhouette. These must be authored as separate images with suitable overlaps, not cut arbitrarily out of one flattened screenshot.

### Pickups and hazards

Collect: Blue crystal shards, Moon crystals. Dodge: Jagged blocker clusters, Violet bumpers, Purple goo. Familiar controls in a new setting, clearer alternating paths and more opportunities for timed Thunderclap.

> Storage remains cavern / index 1. Existing display label: Crystal Caverns. New display name is proposed; no data migration.

## 12 / WORLD 3 — Volcanic Jungle Dash

An exciting tropical finale, still friendly. Distant glowing lava, giant leaves and warm evening light.

Reference in the supplied PDF / package: `references/volcano-concept.jpg`. Earlier AI concept: atmosphere and finish reference only. Its embedded HUD and numeric values are not the approved interface.

### Light and track

Warm peach key, purple shadows and muted jungle greens. Lava stays a background accent. Muted warm stone panels with purple rails. Keep orange pickup silhouettes separate from orange lava.

### Separate scenery layers

Warm sky and distant vapor / Volcano silhouette / Waterfalls and distant bridges / Palms and jungle shelves / Large track-side foliage / Very sparse leaves and embers. These must be authored as separate images with suitable overlaps, not cut arbitrarily out of one flattened screenshot.

### Pickups and hazards

Collect: Amber sunstones, Golden suns. Dodge: Lava-cracked boulders, Warm-core bumpers, Purple goo. Combine familiar moves. Difficulty comes from readable decisions, not hidden hazards or flashing scenery.

> Storage remains volcano / index 2. Existing display label: Volcano Jungle. New display name is proposed; no data migration.

## 13 / OBJECT LANGUAGE — Read the object before its color.

Every collectible should look inviting. Every obstacle should be distinct at a glance, even against a world with a similar palette.

| Asset family | Shape and finish | Gameplay reading |
| --- | --- | --- |
| Common treasure | Faceted, compact, bright center and soft edge. | Small floating pickup; one consistent size. |
| Special treasure | Star, crescent or sun with a wider silhouette. | Higher-value pickup; not an obstacle ring. |
| Rock / blocker | Heavy asymmetric base, visible ground contact. | Grounded hazard; never floats like a gem. |
| Bumper | Dark rounded body, large colored core. | Hover height visually matches the jump requirement. |
| Goo | Low, wide, irregular puddle with thick border. | Floor hazard, not a glowing treasure pool. |

### Fair silhouettes

Collision uses the existing gameplay footprint, not transparent margins or glow. A large shadow cannot become a larger hitbox. Test object overlap at every lane and on the curved walls.

### Layer discipline

The halo lives below or behind the pickup. Atmospheric particles stay behind the danger layer. Foreground plants never hide the next decision point. Decorative shapes must not impersonate a pickup.

### Approval at distance

Review each object at its far, middle and near sizes; then inspect grayscale and low-effects modes. Keep an accessible name for each ability or item counter in the interface.

> Start with two treasure types and three hazards in Emerald Skyway; reuse the same interaction language in the other worlds.

## 14 / CAMERA + DEPTH — Keep the track. Author the character.

The first technical experiment should reuse the existing track and movement rules, while replacing only their visual presentation.

### Renderer decision

Retain the current Three.js stack for the isolated slice. Keep a simple curved track mesh; introduce camera-facing art for hero, pickups and hazards. Do not add another renderer or rewrite authentication to achieve a different visual style. The Sprite primitive is camera-facing and does not cast a real shadow, so ground shadows need a separate decal. [T1]

### Framing targets

Start with a stable rear chase view. Keep the vanishing point around the upper third and the character around the lower-middle, with an unobstructed route ahead. Author rear sprite views for a roughly 12-degree downward camera; validate this angle in the composition proof before mass production.

### Avoid billboard failures

Do not orbit the camera around a single rear drawing. Limit banking and use authored left/right view poses rather than tilting a flat child into the ground. Keep shadow scaling separate from the character, especially during jumps.

### Order and lighting

Render broad scenery first, then track and contact decals, then grounded objects and hero, then small effects, then HTML controls. Resolve translucent overlap explicitly. Authored sprites already contain lighting: do not tint them with a second full 3D lighting setup.

### Parallax and cleanup

Use modest movement differences among far, middle and near layers. Load only the selected hero and world; dispose of old textures and materials on world changes rather than accumulating them. Three.js requires explicit GPU-resource cleanup. [T3]

> The first slice is a visual adapter, not a balance update. Preserve movement timing, collision math, score events and account boundaries.

## 15 / HUD + INPUT — The road belongs to Jamesy.

Information at the edges. Controls within reach. No large floating word banners across the character or the next obstacles.

### Landscape layout

Top corners: Pause and one quiet world/progress indicator. Bottom left: score and combo above left/right steering. Bottom right: power and treasure count above Jump / Smash / Clap. Keep the center corridor empty. Use short labels on action buttons rather than unexplained icons alone.

### Portrait layout

A compact top row holds score, treasures and Pause. The power meter sits just below; the bottom row holds steering and actions. Do not force the landscape arrangement into a narrow screen. This is an intentional responsive exception to bottom-corner counters.

### Touch and legibility

Target 52 CSS-pixel tap areas with 8-pixel gaps, counters of at least 20 CSS pixels and settings text of at least 16. Honor safe-area insets plus a 12-pixel margin. Test 390 x 844 portrait and 844 x 390 landscape, with toolbars expanded and collapsed. [A2]

### Feedback hierarchy

Pickups animate their counter and use a sound cue. Ability unlocks highlight one icon. At most one short edge notification appears; consolidate rapid pickups instead of queueing a wall of words. Show full explanations in training, pause or results.

### Interaction states

Every button needs idle, focused, pressed, disabled and cooldown states. Keyboard focus is visible. Preserve simultaneous steering and jumping, keyboard controls and automatic pause when the page loses focus.

> UI sizes are proposed targets. Verify contrast at runtime: 4.5:1 for ordinary text, 3:1 for qualifying large text and relevant controls. Do not rely on color alone. [A1]

## 16 / MENUS + THE HUB — One visual family, not one giant image.

Reuse color, spacing, border treatments and hero artwork across the racer, James Game Center, Hall of Fame and player cards.

### Title screen

Separate a clean character/environment image from the editable game logo and real HTML menu buttons. Main actions: Play, Character Select, Level Select, Settings, Hall of Fame, Player Cards and Back to James Game Center. Keep Play visually dominant.

### Character and world selection

Use consistent portrait framing, a clear selected border and one short ability description. All existing worlds remain accessible. Future characters clearly say “In development” and do not trigger a broken route.

### Hall of Fame

Keep six current categories: Most Points, Most Adventures, Most Worlds Completed, Highest Average, Highest Single Run and Longest Clean Streak. Keep Little Hero and Superhero separate, equal-rank ties, empty-state honesty and clickable player cards. Do not award Sean fabricated scores just to fill a podium. [R4]

### Player cards and Master

Show nickname, Master / Player badge, game-specific records, medals and best runs. Sean remains the only initial Master account. Candidate costume portraits are not user accounts. Show no email, private sign-in data or technical identifiers on cards. Preserve the current master-only process for adding players. [R2]

### Icons and share art

Create 1024-square icon masters, then check 512, 192 and 180 exports. Keep the hero face and 4 badge readable without tiny title text. Share artwork is 1200 x 630 with safe title margins. Do not bake a current score or rank into shared art.

> Opening menus or browsing this art package must never seed players, score receipts or production database writes.

## 17 / EXPORT CONTRACT — Frames that can actually ship.

An attractive lineup is not a sprite sheet. A production asset needs stable geometry, clean transparency, predictable metadata and an explicit approval state.

| Property | First-pass contract |
| --- | --- |
| Authoring frame | 512 x 640 RGBA PNG; identical canvas for every hero pose. |
| Runtime frame | 256 x 320; scale all frames uniformly from the authoring canvas. |
| Ground anchor | Top-left normalized (0.5, 0.9); runtime pixel (128, 288). |
| Atlas | 2048 x 2048 maximum; no rotation, no per-frame trim. |
| Padding | 4 pixels each side, including 2 pixels of edge extrusion. |
| Metadata | Unique ID, animation/view, frame rectangle, page and anchor. |
| State | planned → candidate → approved → production_ready. |

### Alpha and edge checks

True alpha is required for characters and objects. A painted checkerboard or a flattened contact sheet is not transparency. Inspect outlines on black, white and checker backgrounds for halos. Keep a small transparent border and exclude large baked glows.

### Naming and separation

Use stable lowercase IDs such as hero.hulk.run; files use hulk_run_rear_000.png. Keep source art, normalized frames, atlases and generated previews in separate folders. Item and effect atlases do not share the hero’s fixed-frame contract.

### Pipeline included

tools/pack_atlas.py validates and packs same-size RGBA hero frames. review/index.html lets a reviewer load its atlas JSON and pages, scrub animations and inspect the anchor. The tool tests use temporary synthetic fixtures, not finished game art.

> The provided packer handles this first hero contract only. It is not an automatic character animator or a guarantee that anatomy is consistent.

## 18 / PERFORMANCE — Budget the pixels, not just the files.

These are initial acceptance targets, not measured results. A 2.5D approach still needs profiling: large atlases and layered transparency can be expensive.

| Resource / behavior | Target to test |
| --- | --- |
| Menu transfer | At most 4 MiB compressed, no five-hero preload. |
| First-world additional transfer | At most 8 MiB; load the selected hero and world. |
| Resident texture budget | At most 80 MiB estimated in the active slice. |
| Hero atlas residency | At most two 2048-square RGBA pages at once. |
| Visible objects / particles | 80 billboards; 32 decorative particles; 0 in Gentle. |
| Frame rate | Prefer 60 fps; maintain at least 30 on target device. |
| Pixel ratio | Start with a 1.5 cap; lower quality before clarity. |

### Texture memory example

One 2048 x 2048 RGBA8 page is 16 MiB before mipmaps, about 21.3 MiB with a full mip chain. Two such pages are about 42.7 MiB. This is a dimension-based estimate; a smaller PNG download does not make the decoded texture equally small. [T2]

### Test on real hardware

Measure Safari on the owner’s iPhone in portrait and landscape, after several minutes of play and after repeated world changes. Record frame pacing, memory symptoms, temperature / throttling observations and touch response. A desktop screenshot is not a device performance test.

### Fallback order

Reduce decorative particles, background layers, pixel ratio and distant props first. Do not remove safe controls, shrink the hero beyond readability or change physics to disguise rendering problems.

> Texture sizes and draw limits can be revised only with a documented measurement; do not silently preload the entire five-hero roster.

## 19 / PRODUCTION GATES — One finished slice before five rosters.

Advance in small reviewable steps. Each gate has a concrete deliverable, a named reviewer role and a clear exit condition.

| Gate | Deliverable / exit condition |
| --- | --- |
| G0 · Direction | This bible, source register and asset IDs. Direction accepted; v1 specifications available for review. |
| G1 · Character | Five-costume lineup + Hulk front/rear/lean/contact proof. Sean approves identity and silhouette; art reviewer checks continuity. |
| G2 · Animation | Hulk 8-frame run proof, then 64-state-frame package. No ground jitter, flipped marks or opaque halos. |
| G3 · Composition | One Emerald composition with real layer separations, object families and responsive HUD. Route stays readable. |
| G4 · Playable slice | Hulk + Emerald in an isolated preview; controls, powers, finish and records regression tests pass. |
| G5 · Expansion | Remaining two worlds, then four heroes. Each new hero passes the same animation and fairness gates. |
| G6 · Release | Owner visual acceptance, real-device checks, account regressions and a rollback commit. Only then change main. |

### Ready now

Written hero/world briefs, frame schedule, asset registry, authoring prompts, export tools, tests and an atlas review page. These are production scaffolding, not a completed game reboot.

### Next production batch

Generate the five-costume lineup as a candidate; resolve identity drift. Produce Hulk’s view/pose proof, then the eight-frame rear run. Do not generate all 320 planned hero frames before this proof is accepted.

> No estimate is a delivery promise. Further generation, cleanup, rigging and device testing occur as explicit work, not unattended background activity.

## 20 / ACCEPTANCE — Review the whole experience.

Use the checklist in ACCEPTANCE.md before moving an asset or a build to the next status. Passing a script is only one part of acceptance.

### Visual gate

Same face and orange hair across frames; consistent 4 / J orientation; fixed ground anchor; plausible limbs; no boundary clipping; clean alpha; clear silhouettes at 48, 96 and intended display size. Review one full moving sequence, not just the best pose.

### Gameplay gate

Jump, Smash, Thunderclap and burst stay timed correctly. Lane positions and shadow contacts agree. Pausing freezes both animation and simulation. The result screen records a run once. A visual effect must not become a collision object.

### Account gate

Test using demo fixtures only: correct Master matching, rejected incorrect details, no extra Master, no automatic signup, no fabricated rankings, preserved mode filters and ties, retry-safe receipts, no practice-score leakage. Never use a real private credential in a screenshot or CI log. [R2, R4]

### Mobile and comfort gate

Check safe areas, toolbars, two-finger steering/jumping, accessible labels, readable focus, no scrolling overflow, no flashing, Gentle Effects, mute and audio start after a user gesture. Test the final composition on the device, not only resized browser windows.

### Release gate

Approved art is present, checksums recorded, production manifest contains no candidate paths, all references are labeled, main still has a rollback point, and actual screenshots are distinguished from concept illustrations.

> Reject an asset for a single critical defect even when the rest of the page looks polished.

## 21 / REFERENCES + HANDOFF — A reusable source of truth.

Creative rules in this document are project decisions and proposed targets. Technical and current-system claims are tied to the sources below.

### User-provided visual evidence

The original Jamesy cartoon is the identity anchor. The three earlier AI-generated racing illustrations are mood references, not layers, alpha sprites or validated gameplay screenshots. Their old HUD is intentionally not carried forward.

### Current application snapshot

R1: racer README. R2: v1.3 player setup. R3: current game logic. R4: current Hall of Fame model. All are pinned to racer commit 47d8291eadd9c0848dee38dc508b67f3129b6d11; hub snapshot is 40a1f4b2355e8e920ecd8a53cdc115cb47c75b49.

### Technical references

T1: Three.js Sprite documentation. T2: Three.js Textures manual. T3: Three.js Cleanup manual. A1: W3C WCAG 2.2. A2: MDN CSS env / safe-area documentation. Retrieved September 28, 2026. Full addresses are in sources.json and the editable Markdown edition.

### Handoff map

ART_BIBLE.md mirrors the editorial specification. heroes.json, worlds.json, animations.json and tokens.json are machine-readable briefs. assets.json is the status register. PRODUCTION_PLAN.md sequences work. PROMPTS.md contains reusable authoring instructions. ACCEPTANCE.md defines the gates. tools/ and review/ prepare the next sprite pass.

### Approval record

Direction: accepted in the conversation. Written v1 details: proposed production baseline. New five-costume illustration: candidate when generated. Final hero animation, world layer sets, title art and new gameplay renderer: not yet approved or shipped.

> Keep this document versioned. A later change to identity, timing, storage or the score model needs an explicit decision entry, not an unrecorded edit.

## Source register

The full downloadable production kit contains the JSON briefs, asset register, tools, local reviewer and reference images mentioned below. The GitHub document review may contain only the editorial bible, production plan and frame contract until that toolkit is imported.

- [R1] Current racer README, preserved baseline: https://github.com/seansommer/James-Hulk-Racer/blob/47d8291eadd9c0848dee38dc508b67f3129b6d11/README.md
- [R2] Current player setup (v1.3): email / nickname, Realtime Database: https://github.com/seansommer/James-Hulk-Racer/blob/47d8291eadd9c0848dee38dc508b67f3129b6d11/docs/PLAYER_CENTER.md
- [R3] Existing game rules and stable world IDs: https://github.com/seansommer/James-Hulk-Racer/blob/47d8291eadd9c0848dee38dc508b67f3129b6d11/src/game/logic.js
- [R4] Existing Hall of Fame categories and score model: https://github.com/seansommer/James-Hulk-Racer/blob/47d8291eadd9c0848dee38dc508b67f3129b6d11/src/shared/center-model.js
- [T1] Three.js: camera-facing sprites and manual shadow requirement: https://threejs.org/docs/pages/Sprite.html
- [T2] Three.js: texture memory and image dimensions: https://threejs.org/manual/pages/textures.html
- [T3] Three.js: explicit resource disposal: https://threejs.org/manual/pages/cleanup.html
- [A1] W3C WCAG 2.2: contrast, motion and flashing criteria: https://www.w3.org/TR/wcag/
- [A2] MDN: safe-area environment variables: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/env

- [R5] James Game Center baseline commit: https://github.com/seansommer/James-Game-Center/commit/40a1f4b2355e8e920ecd8a53cdc115cb47c75b49
