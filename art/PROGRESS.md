# Resume Jamesy art production — Jump 04

## Current stage

**Group 1 — Characters. Hulk Jamesy's jump and landing pose candidates are prepared for review.** The broader project has a playable original racer and Game Center foundation; the new 2.5D storybook presentation is still in art production and has not replaced the live renderer.

## New in this batch

- One original nine-pose rear-view source, preserved unchanged with its SHA-256 and generation provenance.
- Six jump and three landing drawing candidates; 512x640 RGBA masters and matching 256x320 copies, review atlas, source rectangles, provisional roots, contact board and an embedded-image reviewer.
- [Jump 04 reviewer](01-characters/hulk/jump-reviews/v01/review-export/review.html) and [review notes](01-characters/hulk/jump-reviews/v01/REVIEW.md). Starts paused; one-shot playback holds the last pose rather than treating landing as a continuous loop.
- Source order is unchanged. Pose 2 reads as early lift rather than grounded push-off. No simulated jump path, hidden interpolation, per-pose scale fitting or physics changes are added.
- 18 individual PNG checks, nine atlas comparisons, source verification, 11 synthetic unit tests and 15 executed local Chromium reviewer checks. Browser checks are separate from the art workflow and do not replace physical phone testing.

## Current selected Hulk sequence candidates

| Clip | Planned unique frames | Current selected candidates |
| --- | ---: | --- |
| Rear idle | 4 | Movement 03: 4 |
| Rear run | 8 | Run 02: 8 |
| Lean left | 4 | Movement 03: 4 |
| Lean right | 4 | Movement 03: 4 |
| Jump | 6 | Jump 04: 6 |
| Land | 3 | Jump 04: 3 |
| Smash | 8 | Earlier contact study only; sequence next |
| Thunderclap | 6 | Next action batch |
| Power-up | 6 | Pending |
| Bump | 3 | Pending |
| Victory | 8 | Pending |
| Menu idle | 4 | Pending |

**29 selected sequence-drawing candidates across six clips, out of 64 planned Hulk frames.** This is a candidate-count milestone, NOT a completion percentage or 29 production-approved frames. Six earlier pose studies are separate. Export resolutions, obsolete run versions and source-sheet copies do not increase this count.

## Assessment and unresolved work

The character identity, palette, rear-view vocabulary and reusable alpha/export pipeline are established. The largest remaining art risk is motion consistency: stride cadence, cape transitions, cross-sheet proportions, jump takeoff/contact timing, loop seams and final camera/ground alignment. Resolve these together before accepting the character package as production-ready.

The other four costumes have reference designs, not finished animation libraries. Item families, environment layers, matching interface artwork and effects are still later production groups. Do not generate another poster as a substitute for actual pose frames.

## Next exact sub-batch

**Rear-view Smash (8) and Thunderclap (6)**, with effects kept separate. Then power-up, bump, victory and menu idle. Keep outstanding run/bank/jump notes open for a unified character-motion review. Continue the remaining four character families before items, then environments, interface, effects and assembly.

## Whole-project checkpoint

See [PROJECT_STATUS.md](../production/art-bible-v1/PROJECT_STATUS.md). Main already contains the original three-world game and the hub/account/Player Card/Hall of Fame foundation. The new sprite presentation and matching hub graphics are not integrated. Live Firebase rule activation and physical Safari behavior have not been verified by the art tests.

## Protected boundary and storage

Preserve art bible v1.2, the permanent J-emblem five-costume reference, prior reviewed sources and the current v1.3 email/nickname Realtime Database design with Sean as sole initial Master. Costumes are not player accounts. No main deployment, live-renderer change, Firebase rule edit, roster import or score migration is part of this batch.

GitHub remains the artwork archive. Original sources, candidates and export copies have explicit statuses. No Google Drive migration or generated video is needed for this handoff. Confirm real saved bytes in the file inventory and successful archive job rather than counting generation prompts as assets.
