# Jamesy · Emerald Park playable art preview

Use the separately delivered `Jamesy-Emerald-Preview.html`, or build it with the commands below, then open it in a current browser with WebGL support. The file contains the game and artwork; no account, install, or web server is needed. On phones, download and open the file in a browser, rather than a file-manager preview. A hosted phone playtest remains the next delivery step.

The **Art & motion** button opens animation playback, speed, frame scrubbing, light/dark/checkerboard backgrounds, and the detailed asset collection.

## What is playable

- A 720-unit Emerald Park practice course built on a real curved 3D half-pipe. Steering changes Jamesy's position along its rounded floor and rising side walls.
- The existing movement, jump, collectible, power, smash, thunderclap, and collision rules.
- 56 archived hero drawings in 11 clips, exported from 512 × 640 sources to registered 384 × 480 runtime frames.
- Five independently animated object types, plus a tree sway study: 41 selected drawings in six clips.
- Ten original detailed Emerald asset designs, with transparent scenery and an opaque park backdrop.
- Keyboard and touch controls, synthesized sound, pause/resume, finish/retry, and reduced background motion.

This practice entry does not import Firebase, account, profile, leaderboard, or score-submission code. It makes no external requests and writes no account or score storage. The main game entry and deployment workflow are unchanged. Preview artwork lives under `preview-public` and is excluded from the main app build.

## Art status

All new art is **candidate artwork**, not final approval. AI generated the actual animation drawings; runtime code plays the frames and supplies movement, placement, and effects. These are sprite animations, not Runway videos. Runway remains reserved for future cutscenes at the owner's request.

| Clip | Selected drawings | Behavior | Remaining work |
| --- | ---: | --- | --- |
| Gem | 12 | Facets change through a turn | More consistent angular speed and seamless loop |
| Star | 6 | Thick star turns | Add in-betweens for smoother close-up motion |
| Rock | 8 | Cracks, separates, collapses into rubble | Better impact/dust timing and lingering rubble |
| Bumper | 6 | Violet lenses pulse | Verify casing stability in motion |
| Goo | 6 | Jelly mound wobbles | Refine highlight and footprint continuity |
| Tree | 3 | Selected poses play forward and backward | Steadier trunk and more wind in-betweens |

The first tree sheet clipped the leaves. The second sheet's lower row changed branch identity. Those poses are deliberately excluded. The hero's previously noted cape, scale, support-foot and run-to-clap transitions still need review. Track lighting, surface detail, arrow markings, contact shadows and camera framing are the next visual polish tasks; this build is not the finished concept-art look.

## Development and reproduction

```sh
npm install
npm run preview:dev
# Open http://127.0.0.1:4174/preview/
npm run preview:build
npm run preview:package
npx playwright install chromium
npm run preview:test
```

The source art and generation prompts live on the racer repository's art branch under `art/02-items/park/v02`, `art/03-environments/park/v01`, and the two `art/emerald-*-session.json` files. To rebuild runtime exports from that checkout:

```sh
node scripts/export-emerald-preview.mjs /absolute/path/to/art-checkout
```

Exports preserve source hashes, frame rectangles, pivot registration, clip timing, and review notes. No frames are independently stretched to a new size. Hero registration is inherited from the existing art review.

Validation: 28 existing unit tests and the main build pass. The preview browser test covers load, keyboard/touch steering, jump, pause, smash-triggered rock animation, review controls, finish, retry, phone layout, and isolation from external/account writes. Screenshots are generated under `test-results/emerald`.
