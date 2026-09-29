# Unified Hulk consistency findings

This is an inspected first-pass review of existing drawings, not production sign-off. The reviewer deliberately uses original export scale and pivot rather than independently fitting each silhouette.

## 1. Front menu → victory: reconcile size and proportions

The first menu-idle drawing is visibly smaller than the first victory drawing on the same 256x320 canvas. Using alpha >=16 as the visible-silhouette threshold, the existing menu frame spans y=76 through 288 (213 pixels); the first victory frame spans y=46 through 288 (243 pixels). Their lower extents agree while their upper extents differ by 30 pixels. These are silhouette bounds, not anatomical height measurements.

Both are relaxed front-facing stances, so this is worth correcting before direct texture swaps. Retain the owner's liked victory direction. Compare face, hair, shoulder, waist and boot landmarks before choosing a single clip-level registration or a targeted redraw. Do not scale every frame independently; that can hide breathing and introduce new foot drift.

## 2. Run → Thunderclap: plan the camera handoff

Run is straight rear; Thunderclap is rear-three-quarter to expose the hands. The side-by-side view makes the orientation change obvious. Retain the clap sequence as a candidate, but either add an intentional turn-in/turn-out drawing or re-author the action to the gameplay camera. Do not describe an immediate texture switch as seamless. A cosmetic transition must not delay input, grant a second hit or write another score receipt.

## 3. Rear idle / run / banks: refine the connected motion

Hair outline and shoulder/cape proportions differ between sheets. Idle has a fuller hair silhouette; running and banking change the cape's sweep and apparent body size. Some change is expected from body tilt, but it needs a landmark review at the same camera and canvas scale.

Keep the existing left/right banks separately drawn. Review their support-foot transitions and the run's last-to-first seam. Do not mirror hair or emblems, or duplicate a contact pose merely to fill a frame count.

## Additional checks before assembly

- Jump and landing: takeoff/contact and recovery-to-run, with physics owning world height.
- Smash: overhead-to-downswing spacing, two-fist contact, planted feet and cape lift.
- Power-up: changing foot spacing and shoulders; aura stays separate from body artwork.
- Bump: stabilizing step and open-glove anatomy.
- Front clips: victory frame 4 → 5, menu frame 4 → 1, face/eye continuity and cape return.
- Alpha: check pale fringes and enclosed arm/cape gaps against dark and checker backgrounds; a valid alpha channel is not final matte approval.

## What the review does not change

All 64 chosen PNGs in the conversation set preserve the exact previous pixels. No new pose, interpolation, hitbox, score formula or database write is introduced. The original 64-drawing schedule is represented, not finished animation. Review utilities and duplicate export sizes do not count as additional drawings.

## Next character work

Carry out the front-scale and camera-handoff corrections while keeping the established face, orange hair, permanent J and palette. Spider Jamesy's first identity/turnaround proof is the next costume family; it must use the approved five-costume lineup, not a recolored cape-bearing Hulk. Items remain after the character group.
