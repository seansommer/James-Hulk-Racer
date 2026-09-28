# James Game Center — Realtime Database setup (v1.2)

This guide supersedes the earlier Firestore/Google-sign-in directions. Both James apps now use Firebase Realtime Database:

`https://james-game-center-default-rtdb.firebaseio.com/`

Project: **james-game-center**. Do not change the family or SUJA Firebase projects.

## 1. Enable Anonymous Authentication

Open Firebase Console → james-game-center → Authentication → Sign-in method. Enable **Anonymous**, then Save. You do not need Google or Email/Password providers for this version. Do not enable automatic anonymous-account cleanup: this app deliberately retains device identities.

The visible login is email plus nickname. Firebase Anonymous Authentication runs underneath it, like the family hub. No password, Google popup, email delivery service, or Cloudflare Worker is required. The email/nickname pair is hashed locally to locate a player; raw emails are not stored in the Realtime Database or displayed on cards. This is convenience-based, trust-based entry, **not verified email authentication**. Anyone who knows an ordinary player's matching pair could open that approved player. Use this for trusted family play, not sensitive information.

## 2. Publish the new Realtime Database rules

Open **Build → Realtime Database → Rules** for the exact database above. Replace all of the rule text with the complete **firebase-database.rules.json** from this version and press **Publish**.

Do not paste the earlier `rules_version = '2'` Firestore file. Realtime Database rules are JSON with a top-level `rules` object. Keep the database locked until the new rules are published. Never set the root `.read` or `.write` to true to fix sign-in.

The deterministic source is `scripts/database-rules.mjs`; `npm run rules:build` generates the JSON. The SAME JSON is loaded into the demo emulator for testing and published at:

https://seansommer.github.io/James-Hulk-Racer/firebase-database.rules.json

The build also exports it in the verification artifact. Generating/committing the file does not publish Firebase console rules.

## 3. Register your master device

Open the updated James Game Center in the browser you plan to use. Open Hall of Fame or your profile. Enter **your email address** and **Sean** as the sign-in nickname. Press **Sign in / Request access**.

An initial request is not yet a player card. Open **Account setup → Your User ID** and copy the exact ID. In **Realtime Database → Data**, add:

- Key `_admin` at the root, if absent.
- Within `_admin`, key `masterUid`.
- Value: your exact copied User ID, stored as a **string**.

This is a Realtime Database path `_admin/masterUid`, **not** the old Firestore `_admin/launch` document. Do not import a JSON file over the database root; add only this key. If `masterUid` already exists, check its value rather than overwriting an established master identity blindly.

Return to the website and press **Check access**. The designated identity can now atomically create **Sean · Master**, the only initial approved card. No visitor can become master by arriving first or typing Sean. The browser cannot assign/change `masterUid`, authorize master devices, create another master, demote the founding master, or delete that card.

Leave **Add a player later** closed. No previous family accounts, demo users or sample scores are imported. A request alone does not appear in rankings. The master is unranked until a signed-in result is earned.

## 4. Try a registered race

Sign in before pressing Play. Complete a Little Hero run. Return to Hall of Fame and press Refresh. Confirm the points and adventure count on your card. Refresh both apps and confirm the same player remains selected. Little Hero and Superhero statistics stay separate.

Results are immutable, UID-owned run receipts in `racerRuns`. Repeated upload of the same receipt does not double-count. Cards and rankings derive their totals from those receipts rather than trusting a separately writable total. Pending uploads stay with the original player on the original device. Practice remains a separate local profile and never becomes a leaderboard record automatically.

This version calculates lifetime totals by reading a player's run receipts, appropriate for this small family setup. Before a much larger rollout, use a trusted aggregation service to avoid reading a growing history for every card. Run measurements still originate in the browser; this is friendly competition, not cheat-proof scoring.

## 5. Master access from another browser/device

The master is intentionally safer than ordinary email/nickname entry. A different browser does **not** gain administrative access merely by knowing your email and Sean.

Enter your original pair on that browser, copy its displayed User ID after access is refused, and privately authorize that exact browser in Realtime Database:

`_admin/masterDevices/NEW_BROWSER_USER_ID` = **true** (boolean)

Then submit the email/nickname pair again on the new browser. This opens the SAME master player and records, not a second master card. Keep `_admin/masterUid` unchanged. To revoke that device, delete its `masterDevices` entry; its existing session immediately loses authorization under the rules. The initial master device remains the founding UID.

App Sign out removes its James session, but keeps the underlying anonymous device identity so the founding device can sign in again. Clearing browser data, using private browsing, or automatic anonymous-account deletion may require this new-device authorization. Anyone with access to an already approved, unlocked device and the matching account details may use the master; protect the device itself.

## Adding ordinary players later

Have the intended person enter their email and nickname and share the displayed James User ID. In Master Controls, expand Add a player later, enter that exact ID and a display nickname, check the confirmation, and approve. They should submit their original email/nickname again. Only explicitly approved members can view cards/rankings or submit records. Pausing a member blocks these actions and hides their active card without deleting history.

Changing a display nickname on the hero card does not change the original sign-in nickname. Keep using the original pair to sign in. No raw email is stored for automatic rename-based recovery.

## Existing Firestore data

No Firestore data, auth users, or other Firebase projects are deleted or changed by this code update. The new runtime no longer reads/writes Firestore and no longer opens Google sign-in. Old Firestore records are NOT automatically copied to Realtime Database. Keep them intact for a deliberate migration if they contain results you need. Local practice saves remain unchanged. Do not assume an empty RTDB leaderboard means old Firestore data was erased.

## Verification and limits

CI tests use **demo-james-game-center**, never production. They check master-only bootstrap, ordinary player approval, master impersonation rejection, device revocation, private identity paths, immutable run receipts, invalid data, score aggregation, card/Hall navigation and phone layouts. UI fixtures are in memory; they do not create production players. The owner still must verify actual Firebase console configuration and physical iPhone/Safari behavior.

Public web configuration is not an administrator credential. Security rests on Authentication, these database rules, and the privately assigned master UID. Review API restrictions and quotas; App Check is not enabled here and must not be enforced before client integration/testing.

Official references:
- https://firebase.google.com/docs/database/web/start
- https://firebase.google.com/docs/database/security/core-syntax
- https://firebase.google.com/docs/auth/web/anonymous-auth
- https://firebase.google.com/docs/database/web/read-and-write
