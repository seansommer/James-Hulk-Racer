# Resume Jamesy art production — Actions 05

## Current stage

**Group 1 — Characters. Hulk Jamesy's Smash and Thunderclap pose candidates are prepared for review.** The original racer and Game Center software foundation remain separate from this new 2.5D artwork. The art branch does not deploy or replace the live renderer.

## New in this batch

- Two original source sheets, eight rear Smash drawings and six rear-three-quarter Thunderclap drawings, preserved unchanged with hashes and generation provenance.
- Fourteen selected action poses at 512x640 and 256x320 RGBA, a review atlas, source/scale/root manifest, individual action contact boards and a combined board.
- [Actions 05 reviewer](01-characters/hulk/action-reviews/v01/review-export/review.html) and [review notes](01-characters/hulk/action-reviews/v01/REVIEW.md). Offline, initially paused, one-shot playback, final-pose hold, frame stepping, backgrounds, sizes and pose strip.
- Effects kept separate. Contact labels are review metadata, never game-damage or score events. Original source order retained; no hidden interpolation, mirrored bodies, per-pose fitting or physics changes.
- 28 individual PNG export checks, 14 atlas-region comparisons, two source checksums, 12 synthetic unit tests and 16 executed local Chromium viewer checks. Browser tests are separate from the archive workflow and are not physical-phone testing.

## Current selected Hulk sequence candidates

| Clip | Planned unique frames | Current selected candidates |
| --- | ---: | --- |
| Rear idle | 4 | Movement 03: 4 |
| Rear run | 8 | Run 02: 8 |
| Lean left | 4 | Movement 03: 4 |
| Lean right | 4 | Movement 03: 4 |
| Jump | 6 | Jump 04: 6 |
| Land | 3 | Jump 04: 3 |
| Smash | 8 | Actions 05: 8 |
| Thunderclap | 6 | Actions 05: 6 |
| Power-up | 6 | Next |
| Bump | 3 | Next |
| Victory | 8 | Pending |
| Menu idle | 4 | Pending |

**43 selected sequence-drawing candidates across eight clips, out of 64 planned Hulk frames.** This is not an overall completion percentage or a production-approved frame count. Six earlier pose studies are separate. Source copies, export resolutions, atlases and older run revisions do not increase the count.

## Open motion-polish notes

Keep run cadence, bank support transitions, cape continuity, cross-sheet proportions, jump takeoff/contact timing and loop seams open for unified review. For Actions 05 specifically: overhead-to-downswing spacing, foot-placement drift, impact cape lift, Thunderclap's wider-than-planned release, hand anatomy and transition into its three-quarter pose still need attention. File checks do not approve motion, final camera/ground registration or hitbox alignment.

## Next exact sub-batch

**Power-up (6) and bump reaction (3)**, without aura/impact effects baked into the body art. Then victory (8) and menu idle (4). Complete the selected Hulk library and unified motion review, then the four other costume families. Items, environments, interface artwork, effects and assembly follow the character group.

## Whole-project boundary

See [PROJECT_STATUS.md](../production/art-bible-v1/PROJECT_STATUS.md). The original three-world racer and hub/account/Player Card/Hall of Fame foundation are implemented. The authored sprite presentation and matching hub graphics are not integrated. Live Firebase activation and physical Safari behavior are not verified by the art tests.

Preserve art bible v1.2, the permanent J-emblem five-costume reference, earlier sources, and the v1.3 email/nickname Realtime Database design with Sean as the sole initial Master. Costumes are not accounts. No live-game source, Firebase rules, sign-in, roster, score migration or main deployment is changed by this batch.

GitHub remains the art archive. Verify actual saved bytes in the inventory and successful archival workflow, rather than treating queued generation tasks as delivered artwork. No Google Drive migration or generated video is part of this handoff.
