# Launch James Game Center and Jamesy The Hulk Racer

## Website publishing

Both repositories use GitHub Actions for Pages. In Settings → Pages → Build and deployment → Source select GitHub Actions. Successful main-branch checks publish the static builds automatically.

- Hub: https://seansommer.github.io/James-Game-Center/
- Racer: https://seansommer.github.io/James-Hulk-Racer/

Deploy both versions together. The hub pins shared account code from the racer as a Git submodule; update that pin when changing account behavior.

## Firebase — Realtime Database, not Firestore

Project **james-game-center**. Database **https://james-game-center-default-rtdb.firebaseio.com/**.

1. Enable **Anonymous** in Authentication → Sign-in method.
2. Open Realtime Database → Rules. Publish this version's generated `firebase-database.rules.json`, not the old Firestore rules.
3. Open the hub; enter your email and **Sean** as your sign-in nickname.
4. Copy the User ID shown under Account setup.
5. In Realtime Database → Data, add the string `_admin/masterUid` with that exact ID. Do not replace the database root or import other users.
6. Return to the app and press Check access. Player Cards should show only **Sean · Master**.

Full instructions, new-device authorization and privacy limits: [PLAYER_CENTER.md](PLAYER_CENTER.md).

Google sign-in is not required. The email/nickname entry is trust-based, not email verification; master permissions additionally require a privately authorized device identity. No Cloudflare Worker or third-party provider API is used.

Old Firestore data is left intact and not automatically migrated. Local practice remains available while registered account setup is incomplete. Existing family and SUJA projects are untouched.

## First phone test

Use Little Hero → Emerald Park. Try steering while jumping, power unlocks, pause/resume and both orientations. Finish a signed-in run, return to the Hall of Fame, and refresh. Automated Chromium tests do not replace physical Safari testing.
