# Jamesy The Hulk Racer

A playable, family-friendly 3D half-pipe runner for **James Game Center**. The same original Jamesy character explores Emerald Park, Crystal Caverns, and Volcano Jungle. Inspired by the perspective and collect-and-dodge rhythm of classic bonus stages; no Sonic assets are used.

**Intended game address:** https://seansommer.github.io/James-Hulk-Racer/  
**Hub:** https://seansommer.github.io/James-Game-Center/  
**Setup:** [docs/SETUP.md](docs/SETUP.md)

## Play

Jamesy runs automatically. Steer across the curved track, follow treasure trails, jump over hazards, and fill the power meter. Touch controls support simultaneous steering and jumping. You can also drag across the track and swipe upward to jump.

Keyboard: arrows or A/D steer, Space jumps, S smashes, C thunderclaps, Escape pauses.

| World | Collectibles | Hazards and setting |
| --- | --- | --- |
| Emerald Park | Green power gems and golden stars | Mossy rocks, floating bumpers, goo, city-park half-pipe |
| Crystal Caverns | Blue shards and moon crystals | Crystal blockers, violet bumpers, glowing cavern palette |
| Volcano Jungle | Amber sunstones and golden suns | Volcanic rocks, warm-colored bumpers, tropical scenery |

Power grows visibly with pickups. At 25 power, Smash clears nearby obstacles. At 65, Thunderclap and a wider pickup magnet unlock. At 100, Super Jamesy temporarily powers through obstacles. Abilities have cooldowns. Little Hero mode has a gentler pace and no game-over; Superhero is faster with three shields. All worlds are available immediately.

Three medals per world reward finishing, collecting half the treasures, and avoiding every bump. Local best scores are separated by difficulty. The private hero card tracks adventures and achievements.

## What is actually rendered

The game uses Three.js, real mesh collectibles and obstacles, an articulated procedural Jamesy character, a deforming cape, custom swept hair, green mask, number 4 chest shield, J belt, animated powers, instanced scenery and a curved 3D track. It is a lightweight browser game, not a pre-rendered video or the AI concept illustration. The 3D character is a stylized interpretation of the supplied reference; it is not an exact production character-model recreation.

The deployment build captures **actual game renders** to create the world previews, app icons, and sharing image. `/qa/` contains real browser screenshots and the verification report. These should not be confused with the higher-detail concept artwork created during planning.

## Saving and privacy

The game works without configuring Firebase. Nickname and progress save locally first. The hub and racer share the same versioned storage keys on `seansommer.github.io` in the same browser. Other Game Center projects are unaffected.

Cloud backup is optional and uses the new `james-game-center` project, Anonymous Authentication, and **Cloud Firestore**. It is not Realtime Database. Profiles are private to their authenticated UID. No emails, chat, public leaderboard, analytics, advertising, service-account credentials, or private API secrets are included. Anonymous backup is not a cross-device sign-in; clearing browser credentials may lose access to the backup. Local/cloud merging retains maximum counters and medal bits, so simultaneous runs in multiple tabs are not an exact accounting system.

Firebase web configuration identifies the project and is public browser configuration. Access is enforced by the included `firestore.rules`, not by hiding the web key. Scores are client-calculated for private family play, not authoritative anti-cheat records.

## Development

Node 22.12+ and Java 21 are used in CI.

```sh
npm install
npm test
npm run test:rules
npm run build
npx playwright install chromium
npm run test:browser
npm run offline
```

`npm run dev` starts the development server. Rules tests are hard-scoped to `demo-james-game-center` in the emulator, never production. The first CI installation produces `package-lock.json` in the verification artifact; commit that lock before dependency maintenance, then use `npm ci`. Direct package versions are pinned.

GitHub Actions tests the game rules and private database rules, builds the app, checks WebGL gameplay in Chromium, captures mobile/landscape layouts and creates the scoped offline cache before deployment. Physical iPhone/Safari performance and touch feel still need device testing. The generated pictures are browser renders, not a promise of console-quality graphics.

Original source music is synthesized with Web Audio after a play gesture. Music and effects have separate sliders. Gentle Effects disables particles and expanding power rings. The game pauses when focus is lost.

Created by Sean.
