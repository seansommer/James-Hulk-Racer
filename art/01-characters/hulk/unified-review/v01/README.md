# Hulk Jamesy — Unified Review 08

## Owner feedback and scope

The owner said **“Looks good let’s continue”** after the Victory 07 review. Record this as acceptance of the victory visual direction, not blanket approval of all animation, matte edges, timing or game integration.

This pass brings the twelve existing Hulk clips together. No new character image, pose interpolation, individual-pose fit, mirrored sprite, video generation or image-service call is part of this pass. The selected PNGs remain unchanged.

## Available drawings versus GitHub archive

The complete conversation review contains **64 selected drawings in twelve clips**: the 56 existing GitHub exports plus the eight Victory 07 exports supplied in the conversation. At the start of Review 08, the victory source was still pending direct GitHub upload. See [Victory source status](../../victory-reviews/v01/SOURCE.json).

The GitHub-generated viewer counts only actual files in the checkout. Until Victory 07 is uploaded, it shows **56 available / 64 planned** and an explicit missing-victory panel. It does not generate replacements, copy a run into the empty clip or call a planned asset archived. After the exact source upload, the existing Victory 07 workflow also rebuilds this review.

- [Review page](review.html): open from a downloaded checkout; GitHub's source page is not a running app.
- [Manifest](manifest.json): exact selected frame references, per-frame hashes and source manifests.
- [All-clip overview](Hulk-Jamesy-All-Clips.jpg) and [all-drawing board](Hulk-Jamesy-All-Drawings.jpg): generated from available exports, not concept illustrations.
- [Review findings](REVIEW.md): issues and correction priorities.

The conversation package additionally supplies a self-contained HTML with all 64 PNGs embedded, an assembled animated WebP review, and the victory supplement. That package is not evidence that the pending source has been uploaded.

## Review behavior

Shared 256x320 canvases and documented ground pivot (0.5, 0.9). Controls include play/pause/reset, individual stepping, half/quarter speed, small display sizes, light/dark/checker backgrounds, previous-frame ghost and paired transition checks. One-shots stop at their final pose; movement and idle clips loop. Starts paused. No requests to game accounts or Firebase are implemented; a restrictive content policy prevents network connections.

No silhouette auto-fit is used. The ground guide is a registration aid, not a measurement proving that both feet are planted. Action frame rate here is review timing, not a new gameplay schedule.

## Verification boundaries

Locally, 64 selected runtime PNGs were checked for 256x320 dimensions and real foreground/transparency, then copied byte-for-byte with matching hashes. The actual viewer script passed ten Node playback/control checks using a minimal DOM stub. That is **not** a browser rendering, layout, image-decoding or physical-device test.

The managed local Chromium refused file navigation with ERR_BLOCKED_BY_ADMINISTRATOR. No policy was changed; no browser assertions executed. The image contact boards were inspected separately. Physical Safari and renderer integration remain untested.

## Protected boundary

Only the art branch and offline review files are involved. No main deployment, live game source, Firebase rules, sign-in, roster, Player Card data or Hall of Fame records are changed. Sean remains the sole initial Master under the existing account design. Stay in the character group; items follow character production.
