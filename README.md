# Jamesy The Hulk Racer

A playable Three.js family half-pipe runner for James Game Center. Explore Emerald Park, Crystal Caverns and Volcano Jungle with the same articulated Jamesy hero: red hair, green mask, purple cape, 4 shield and J belt.

**Game:** https://seansommer.github.io/James-Hulk-Racer/  
**Hub:** https://seansommer.github.io/James-Game-Center/

## Realtime Database update — v1.2

Both apps now use **Firebase Realtime Database**, at `https://james-game-center-default-rtdb.firebaseio.com`, in the new **james-game-center** project. Firestore is no longer used by the runtime. The familiar email-plus-nickname entry uses Firebase Anonymous Authentication underneath. No Google sign-in or password is required.

[Setup and master activation](docs/PLAYER_CENTER.md) · [Launch guide](docs/SETUP.md)

The only initial approved player is **Sean · Master**, after the owner privately sets `_admin/masterUid` in the Realtime Database. No account is automatically made master. Other players require explicit approval. Master access on another browser needs console authorization at `_admin/masterDevices/<authUid>`; knowing the email/nickname alone does not grant master authority.

The Hall of Fame and Player Cards retain their green/purple presentation, six categories, tied ranks, per-difficulty statistics and nine world medals. Completed attempts are stored as immutable per-player run receipts. Retries do not double-count, and totals are derived from receipts. Failed Superhero attempts count as adventures; quitting midway does not.

## Play

Jamesy runs automatically. Steer across the half-pipe and follow treasure trails. Arrows or A/D steer, Space jumps, S smashes, C thunderclaps, Escape pauses. Touch buttons support simultaneous steering and jumping; dragging steers and upward swipes jump.

| World | Treasures | Setting |
|---|---|---|
| Emerald Park | Green gems, golden stars | Landscaped city park, mossy obstacles |
| Crystal Caverns | Blue shards, moon crystals | Enclosed glowing crystal cave |
| Volcano Jungle | Amber sunstones, golden suns | Tropical volcanic scenery |

25 power unlocks Smash. 65 unlocks Thunderclap and a gem magnet. 100 triggers Super Jamesy, briefly powering through hazards. Little Hero has a gentler pace and no game-over; Superhero is faster with three shields. Music, sound effects and Gentle Effects are adjustable. All worlds are available from the start.

## Privacy, persistence and migration

Email/nickname is a trust-based match, not verified authentication. Raw emails are not saved in Realtime Database, cards or rankings. Normal approved players can be opened by someone who knows their pair. The founding master additionally requires an authorized device UID. This is for trusted family play, not sensitive records.

Only approved members can read shared records; guests can practice locally. Practice, registered account caches and pending results remain separate. Display nickname changes do not change the original sign-in nickname. The existing family and SUJA accounts/databases are not imported or modified.

Old Firestore data is not deleted or migrated automatically. Leave it intact for a deliberate migration if it contains results. Local practice remains saved. Ranked results follow the James profile after successful upload; unsent results stay on their original browser/device. App Check is not enabled. Browser-measured results are not authoritative anti-cheat scores.

## Development

Node 22.12+; Java 21 for emulator tests.

```sh
npm install
npm test
npm run test:database
npm run build
npx playwright install chromium
npm run test:browser
npm run offline
```

`npm run rules:build` generates `firebase-database.rules.json` from the readable rule serializer at `scripts/database-rules.mjs`. The exact generated file is tested and copied into the deployed website. Generation does not publish live Firebase rules. Database tests are hard-scoped to **demo-james-game-center**. CI gates Pages deployment on rules, logic and browser checks. Keep pinned dependencies; CI supplies a resolved lock artifact for future maintenance.

Cards currently derive totals by reading each player's immutable run history, suitable for a small family roster. Use trusted server aggregation before scaling to many players/runs. Actual phone performance and live Firebase setup need owner testing.

All preview pictures are real game renders, not the earlier cinematic concept illustrations. The procedural 3D hero is a stylized interpretation, not a production character-model recreation. Original Web Audio music starts after interaction.

Created by Sean.
