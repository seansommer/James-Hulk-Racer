# Jamesy Art Bible v1.3 — Hulk-first gameplay slice

## Latest owner decision

> Start with just Jamesy the Hulk, test gameplay before doing the remaining characters, and move on to objects and environments.

This instruction supersedes the production order in v1.2 and older plans. **Do not finish all five costumes before testing the game.** Spider Jamesy, Captain Jamesy, Iron Jamesy and Super Jamesy are deferred, not deleted. Their established lineup references stay intact.

The immediate goal is **Hulk Jamesy + Emerald Skyway + a short playable, unranked test**. The other two environment kits are deferred until this first test answers the readability and control questions. The final three-world goal is not cancelled.

## What stays visually locked

Use the existing dimensional storybook / 2.5D presentation, orange-red hair, friendly child proportions, emerald-and-purple Hulk suit, purple cape with green lining, and upright white J chest/belt marks. No age numeral, new cape emblem or unrequested redesign. See [v1.2](ART_BIBLE_v1.2.md) for the retained material, camera and export standards. Only its conflicting scope/order requirements are superseded.

Product titles stay **James Game Center** and **Jamesy The Hulk Racer**. Emerald Skyway is the proposed visual name for existing world `park`, index `0`; it is not a new stored world.

## New order of work

1. Make the **five Emerald object designs together**: power gem, star, mossy rock, floating bumper, violet goo. Separate rewards from hazards by silhouette, material and motion, not hue alone.
2. Make a **small Emerald environment kit**: distant sky/city backdrop, treetop/parallax layer, tree/shrub props, track-facing gateway. Reuse the existing perspective half-pipe geometry/material as a test surface; a new track texture is optional, not a blocker.
3. Export cleaned object sprites and transparent scenery. Assemble an **isolated Hulk/park practice preview** using existing Hulk candidate frames, current input and simulation logic, a minimal HUD, and the existing sound controls.
4. Test readability, steering, jump timing, Smash/Clap response, collision alignment, frame pacing, portrait/landscape and Gentle Effects. Refine only the animations and art defects the test exposes.
5. After the Hulk slice is enjoyable and readable, decide whether to expand the two worlds or return to the four deferred costumes. Do not automatically restart those costumes.

Work in coherent art sub-batches within this reduced scope. An item still may be approved for a prototype without every spin/pulse frame existing. Never simulate a 3D rotation by turning a flat image edge-on; a gentle bob or authored frames are sufficient for the first test.

## Current Hulk art is a starting point, not a reason to delay testing

There are 64 selected first-pass drawings across twelve clips in the combined conversation set. The last verified repository snapshot has 56 exports; Victory 07's eight drawings are supplied locally and still await source archival. See its [SOURCE.json](../../art/01-characters/hulk/victory-reviews/v01/SOURCE.json) for the actual archive state. No number in this document asserts that the missing bytes are uploaded.

The unified review found menu/victory scale mismatch, a run-to-Thunderclap camera change, and hair/cape/support-foot differences. Keep those findings open. Fix a coherent clip-level registration or a targeted pose where needed; no independent per-frame fitting or broad regeneration solely to make the library look complete.

The preview may use explicitly marked candidate art and honest fallback presentation where a nonessential menu/victory source is unavailable. Missing archival of a victory pose does not block testing movement on a track. Shipping approval is still separate.

## Emerald object contract

| Existing kind | Visual design | Pose and anchor | First test |
| --- | --- | --- | --- |
| `gem` | Emerald beveled power crystal, clean symmetrical facets | Center pivot, floating | Collect; clear silhouette at distance |
| `special` | Thick rounded five-point golden star | Center pivot, floating | Bonus pickup, visibly different from gem |
| `rock` | Squat gray stone with a restrained moss cap; broad irregular base | Bottom-center ground contact | Avoid, jump or smash under existing rules |
| `orb` | Charcoal rounded bumper with muted violet band and warm warning accents | Center pivot, floating | Avoid; never disguised as a reward |
| `goo` | Low irregular violet puddle with a few rounded bubbles, not a shiny gem | Bottom-center ground contact | Avoid or jump under existing rules |

Use one modestly elevated front-three-quarter camera, soft upper-left light and rounded toy-like volume. Render each object in isolation. No hero, labels, poster decoration, scenery, baked ground shadow, pickup aura or impact debris on the source sheet. Retain original pixels and record any later masking.

The first sheet has **five static designs**, not five approved animation clips. Isolated export targets are up to 512-square source canvases and 256-square runtime sprites, preserving aspect ratio. These dimensions are packaging targets, not a claim of native detail. Store the chosen visible bounds, pivot and projected collision footprint separately; alpha bounds must never silently define hitboxes.

## Emerald environment contract

Sunlit city park with a gentle blue sky, softened distant skyline, warm ivory stone, green tree canopies and violet accent details. Match the objects' and character's lighting and finish.

**Backdrop:** no character, coins, gems, obstacles, HUD or foreground track painted into it. It must work behind a moving dimensional track rather than depict a second fixed road with incompatible perspective.

**Parallax canopy:** a separate transparent treetop band; do not crop a whole scenic painting and call the crop a reconstructed background layer.

**Near props:** isolated tree and shrub sprites; positions remain outside playable lanes. Dense foliage must not obscure the next obstacle.

**Gateway:** isolated warm-stone park arch with open center and no written sign. It is decorative in the first test. Supports stay outside the collision route; do not confuse a decoration with an interactable hazard.

A composed scene can demonstrate mood, but it is not proof that isolated production layers exist. The manifest must distinguish backdrop, transparent layer, prop and composition study.

## Minimal playable test

Hulk only; `park` / 0 only; Little Hero first. A short representative section can precede a full-world run. Auto-run, left/right steering, jump, treasure collection, visible power, Smash and Thunderclap remain the core loop. Use the existing grounded shadows and restrained procedural effects for early feedback instead of waiting for a full effects-art library.

Reuse current responsive controls, keyboard equivalents, pause/resume and independent sound/music sliders. Keep gameplay center clear. No new main menu illustration, four-character selector or completed Hall of Fame decoration is required before testing.

In the preview, keep the existing score/collision rules when possible; mark any deliberate balance experiment. **No preview run may be submitted to ranked records.** Use an isolated practice adapter without account/score writes. Retain the production interfaces separately for later regression testing.

## Acceptance questions

- At near, middle and far sizes, can a player distinguish gem, star, rock, bumper and goo?
- Can the player see the next decision before the object reaches Jamesy?
- Do the displayed contact points and the unchanged simulation agree?
- Are steering plus jump responsive together, and do Smash/Clap respond without an animation lock?
- Are the cape, scenery and effects clear of the route and controls?
- Are prototype animation transitions acceptable at running speed, and which actually need correction?
- Do portrait/landscape controls fit and does the selected quality mode hold stable frame pacing on a real iPhone?

Passing a file validator does not answer these questions. Physical playtesting, not completion of every art group, is the next meaningful milestone.

## Protected systems and storage

Keep v1.3 email/nickname Realtime Database account behavior, `jamesV1`, Sean as the sole initial Master, existing Player Cards, Hall of Fame, per-mode records and queued production receipts unchanged. No migrations, sample accounts, score resets, credential changes or live deployment are part of this scope update.

Use built-in image generation for new art, reuse suitable sources and keep GitHub as the preferred archive. No Runway generation or transfer. A local source is `pending_direct_upload` until its exact bytes exist in GitHub. Do not publish base64 text pretending it is an image or relabel documentation as a completed upload. Continue the existing direct-source archive pattern when an exact source is available.

The current v1.2 PDF remains a historical snapshot for its production order. This Markdown addendum is the authoritative scope change; the PDF has not been silently re-exported.
