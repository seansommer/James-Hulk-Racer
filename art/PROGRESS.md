# Resume Jamesy art production — Unified Review 08

## Latest owner direction

Continue character artwork in groups and use the built-in image generator when new images are needed. Reuse suitable existing art. The owner likes Victory 07's visual direction. No new image-generation or Runway call was made in Unified Review 08.

## Current stage

**Group 1 — Characters. The complete 64-drawing Hulk first pass has been assembled locally into a twelve-clip consistency review.** Existing movement, actions, states and victory were compared at a shared canvas size and ground guide. These are selected candidates, not final animation or a deployed renderer.

See [Unified Review 08](01-characters/hulk/unified-review/v01/README.md) and its [specific findings](01-characters/hulk/unified-review/v01/REVIEW.md). The new utilities preserve existing PNG pixels and make size/camera differences visible rather than hiding them with per-frame fits.

## Archive boundary — important

The GitHub checkout still contains the earlier **56 selected drawings**. The eight Victory 07 drawings and their original source are supplied in the conversation review package but await the previously described direct source upload. See [SOURCE.json](01-characters/hulk/victory-reviews/v01/SOURCE.json). A pending source is not an archived source.

The GitHub-generated unified viewer uses only files actually present: 56 now, 64 once the victory source is archived and exports rebuilt. It shows an explicit missing clip instead of fabricated artwork. The separate conversation package contains all 64 for review now.

## Selected Hulk drawing schedule

Rear idle 4; run 8; left bank 4; right bank 4; jump 6; land 3; Smash 8; Thunderclap 6; power-up 6; bump 3; victory 8; menu idle 4. Total: 64 candidates across twelve clips. Duplicate resolutions, older revisions, atlases and review composites do not add unique frames.

## What the combined pass found

1. Menu idle is visibly smaller than victory at the same canvas scale: first-frame visible heights are 213 and 243 pixels using alpha >=16. Reconcile landmarks rather than fitting every drawing separately.
2. Thunderclap's rear-three-quarter camera does not match the straight-rear run. Plan an intentional turn-in/turn-out or a camera-matched redraw.
3. Rear idle, run and banks need a common hair/shoulder/cape landmark pass and connected support-foot timing.

The existing jump, Smash, power-up, bump, matte and loop-seam review notes remain open. The victory visual direction is accepted for continuing; neither file checks nor positive feedback automatically validates runtime motion.

## Verification

The full local review checks 64 real 256x320 RGBA images and byte-identical copies. Ten Node checks executed the viewer's timing/control code using a minimal DOM stub. This does not test browser rendering or mobile layout. Managed Chromium blocked file navigation before any browser assertions; no policy was disabled. Contact boards were inspected separately. Physical iPhone Safari remains unverified.

## Next exact character work

Reconcile the menu-to-victory size and the rear/action handoffs, then start Spider Jamesy's identity/pose proof using the established five-costume lineup and the same permanent J. Continue the remaining character families before items, environments, interface artwork, effects and assembly.

## Protected boundary

No live-game source, Firebase rules, account setup, roster, saved score, Player Card or Hall of Fame data is changed. Keep the v1.3 email/nickname Realtime Database design with Sean as sole initial Master. Costumes are not accounts. The art branch does not deploy main, and no Google Drive move is needed for this review.
