# Jamesy The Hulk Racer

A playable 3D half-pipe runner for James Game Center. Explore Emerald Park, Crystal Caverns and Volcano Jungle with the same stylized Jamesy hero. Steer, collect treasures, jump, Smash, Thunderclap and build up to Super Jamesy. Little Hero and Superhero have separate records.

Game: https://seansommer.github.io/James-Hulk-Racer/
Hub: https://seansommer.github.io/James-Game-Center/

## v1.3 — familiar email and nickname sign-in

The owner uses the existing master email and nickname **Sean**. After publishing the personalized Realtime Database rules, the first matching sign-in automatically creates ONE fresh master player. There is no User ID copying, master-device approval, Google sign-in, Firestore database, account import or score migration.

[Simple setup instructions](docs/PLAYER_CENTER.md)

The public `firebase-database.rules.json` is a fail-closed TEMPLATE. The owner receives the personalized copy privately; never place the owner's real matching key or email in GitHub, CI, logs, or published assets. The generator is `scripts/database-rules.mjs`; security tests compile it with a dummy fixture matching key, never the owner's.

James uses only `https://james-game-center-default-rtdb.firebaseio.com/`, namespace `jamesV1`, with Anonymous Authentication underneath email/nickname matching. Existing root-level experimental data is not deleted or imported. All new ranked scores start fresh. The family and SUJA databases are not accessed.

This is trust-based family sign-in, not verified email authentication. Anyone who knows the correct email/nickname pair can access that player, including the master. There is deliberately no extra device approval. Raw email addresses are not stored in the game database or shown on cards. The privately supplied rule file contains a matching credential and must not be published.

## Player features

Six Hall of Fame categories, clickable rankings, searchable lifetime Player Cards, protected Master/Player roles, per-world records, medals and a separate personal trophy room. Additional players are created explicitly by the master using their email and nickname. No automatic signup or sample scores.

Runs are immutable and retry-safe. Cards derive totals from per-player run receipts. Local practice, registered profiles and queued uploads remain separate. Client-measured scores are intended for friendly play, not authoritative anti-cheat competition.

## Game and testing

Three.js renders an articulated procedural hero, flowing cape, mesh collectibles, curving track and themed scenery. Artwork in the build is captured from the actual game. Music and effects have separate controls. Gentle Effects reduces glow and particles. Touch and keyboard controls are supported.

```sh
npm install
npm test
npm run test:rules
npm run build
npx playwright install chromium
npm run test:browser
npm run offline
```

Node 22.12+ and Java 21 are used in CI. Tests use only demo emulators or in-memory browser fixtures. They cover first master creation, incorrect details, second-browser sign-in, concurrent creation, role protection, result persistence, gameplay and responsive layouts. Physical iPhone Safari and live account setup must be checked separately.

Created by Sean.
