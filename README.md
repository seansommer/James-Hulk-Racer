# Jamesy The Hulk Racer

A playable, family-friendly 3D half-pipe runner for **James Game Center**. The same original Jamesy character explores Emerald Park, Crystal Caverns, and Volcano Jungle. Inspired by the perspective and collect-and-dodge rhythm of classic bonus stages; no Sonic assets are used.

**Game:** https://seansommer.github.io/James-Hulk-Racer/  
**Hub:** https://seansommer.github.io/James-Game-Center/  
**Launch guide:** [docs/SETUP.md](docs/SETUP.md)  
**NEW — Hall of Fame, Player Cards and master activation:** [docs/PLAYER_CENTER.md](docs/PLAYER_CENTER.md)

## Hall of Fame and Player Cards

Version 1.1 introduces James-only registered accounts and records. The initial approved roster is **Sean · Master** only, after the project owner completes the private Firebase UID setup. No live account has been activated merely by committing this code. No sample scores or other players are created.

The six trophy categories are Most Points, Most Adventures, Most Worlds Completed, Highest Average, Highest Single Run, and Longest Clean Streak. Ranked names open detailed player cards with role, lifetime statistics, per-world bests and medals. Both difficulty modes are ranked separately; ties share a rank. New players remain unranked until they earn records. Average ranking requires three attempts.

Google sign-in verifies identity, while the Firestore approval list controls membership. Only the privately configured master can create or approve members. Master Controls may approve additional players later or pause/restore their access. The sole master cannot be demoted, disabled, deleted or duplicated by the client. Guest practice remains playable without creating a card or joining rankings.

## Play

Jamesy runs automatically. Steer across the curved track, follow treasure trails, jump over hazards, and fill the power meter. Touch controls support simultaneous steering and jumping. You can also drag across the track and swipe upward to jump.

Keyboard: arrows or A/D steer, Space jumps, S smashes, C thunderclaps, Escape pauses.

| World | Collectibles | Hazards and setting |
| --- | --- | --- |
| Emerald Park | Green power gems and golden stars | Mossy rocks, floating bumpers, goo, city-park half-pipe |
| Crystal Caverns | Blue shards and moon crystals | Crystal blockers, violet bumpers, glowing cavern palette |
| Volcano Jungle | Amber sunstones and golden suns | Volcanic rocks, warm-colored bumpers, tropical scenery |

At 25 power, Smash clears nearby obstacles. At 65, Thunderclap and a wider pickup magnet unlock. At 100, Super Jamesy temporarily powers through obstacles. Abilities have cooldowns. Little Hero mode has a gentler pace and no game-over; Superhero is faster with three shields. All worlds are available immediately.

Three medals per world reward finishing, collecting half the treasures, and avoiding every bump. Local best scores are separated by difficulty. The trophy room celebrates personal achievements; the Hall of Fame compares approved players' registered records.

## Rendering

The game uses Three.js, real mesh collectibles and obstacles, an articulated procedural Jamesy character, a deforming cape, custom swept hair, green mask, number 4 chest shield, J belt, animated powers, instanced scenery and a curved 3D track. It is a lightweight browser game, not a pre-rendered video or the AI concept illustration. The model is a stylized interpretation rather than an exact production recreation.

The deployment build captures actual game renders to create world previews, icons and sharing artwork. `/qa/` contains browser screenshots and verification reports. Player-center UI tests use an isolated in-memory account fixture, clearly identified in `center-report.json`; they are not proof of live Firebase activation.

## Saving and privacy

The new `james-game-center` project is isolated from the other family and SUJA hubs. Registered accounts use Google Authentication plus **Cloud Firestore**, not Realtime Database. Shared member records contain nicknames, roles and game statistics, never email addresses. Google Authentication itself knows the chosen account's email. Shared records are readable only by approved signed-in members. Run receipts remain private to their owner. No messaging, ads or analytics are included.

Practice progress and registered caches use separate storage keys. Old anonymous practice backups are preserved, but not imported into lifetime rankings because their original schema did not contain enough history. Sign in before a run to record it. Each result uses a UID-bound persistent outbox and an immutable transaction receipt; retries do not count it twice. Uploaded records follow the same Google account across devices. Unsent results still belong to the original browser/device.

Firebase browser configuration is public project configuration, not an administrator password. Access is enforced by `firestore.rules`. Only the owner can manually configure `_admin/launch.masterUid` in the Firebase console. Clients cannot claim or reassign it. Bounded run validation and aggregate checks do not prove gameplay: scores are still client-measured, suitable for friendly family play rather than authoritative anti-cheat competition.

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

`npm run dev` starts the development server. Rules tests are scoped to the **demo-james-game-center emulator**, never production. Direct package versions are pinned. If a dependency lock is available, use `npm ci`; otherwise the CI verification artifact contains the resolved lock for subsequent maintenance.

GitHub Actions checks game logic, model arithmetic, tie handling, account/outbox isolation, private database rules, actual WebGL gameplay, mobile layouts and player-center UI before publishing. These automated Chromium checks do not replace physical iPhone Safari testing, live Google sign-in, or verification of the owner's console configuration. Original music is synthesized with Web Audio after a gesture. Music/effects have separate sliders; Gentle Effects reduces visual effects; the game pauses when focus is lost.

Created by Sean.
