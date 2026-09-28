# Hall of Fame, Player Cards and Sean's master account

This update adds James-only player records, a six-category Hall of Fame, searchable player cards, and protected Master Controls. The initial approved roster is **Sean, Master, only**. No existing family/SUJA accounts are imported. No sample players or scores are created in the live database.

## One-time activation: the new James Firebase project only

The code cannot configure your Firebase console or identify your new Firebase UID for you. Until the following steps are complete, the interface stays closed to unapproved accounts and offers local practice instead.

1. Open Firebase Console and select **james-game-center**. Do not change the older family or SUJA projects.
2. In **Authentication → Sign-in method**, enable **Google**, choose your project support email if requested, and save. The email is used by Firebase Authentication; it is never copied onto player cards or the leaderboard.
3. Under **Authentication → Settings → Authorized domains**, add **seansommer.github.io** if it is missing. Use the domain only, without either repository path.
4. In the default **Cloud Firestore** database, open **Rules**. Publish the entire current [`firestore.rules`](../firestore.rules) file. This replaces the earlier practice-only rules while preserving owners' private practice data. Do not paste it into Realtime Database.
5. Open James Game Center, choose **Hall of Fame** or your profile button, then **Sign in with Google** using the Google account you want to use as master. This verifies identity but does not grant master access by itself.
6. In **Account setup · Your User ID**, press **Copy User ID**. It is also visible in Firebase **Authentication → Users**. Use the new James project's UID, not your old Game Center ID or a nickname.
7. In **Firestore Database → Data**, create collection **`_admin`**, document **`launch`**, with one **string** field named **`masterUid`**. Paste your exact copied User ID as its value. Save. This is a private console administration step; the app cannot write or replace the field.
8. Return to James Game Center and press **Check access**. The configured identity creates the sole initial card, **Sean · Master**. The same Google identity works in both the hub and racer. Check that Player Cards shows exactly one approved player before adding anyone else.

If `_admin/launch` already exists, inspect its value rather than overwriting an unrelated setup. If it points at another account unexpectedly, stop and verify the correct Firebase project and account. There is intentionally no public 'claim master' button and no 'first visitor becomes master' behavior.

Opening a page does not create a player. Another visitor who explicitly tries Google sign-in may appear as an identity in Firebase Authentication, but remains unapproved: no card, no leaderboard access and no master rights. Only the configured master can approve another player. Leave **Add a player later** closed to keep the roster master-only.

## Your Hall of Fame

Six separate record categories: Most Points, Most Adventures, Most Worlds Completed, Highest Average, Highest Single Run, and Longest Clean Streak. Select a trophy to see its ranked table; select a player name to open their card. Equal values share a rank, such as 1, 1, 3. A brand-new master has a card but no unearned championship.

**Little Hero** and **Superhero** records are separate. An adventure counts when a run reaches its results screen, including a Superhero game-over. Quitting a run does not add a result. Average rankings require at least three results in that difficulty. A clean streak is consecutive no-bump world completions; a bumped or unsuccessful result resets it. Streak order follows accepted run receipts, so overlapping sessions across devices should not be used to measure a strict chronological streak.

Cards include role, lifetime points, adventures, completions, average, best run, clean streak, treasures, smashes, power bursts, no-bump finishes, completion rate and world medals. Per-world best scores and medals remain visible. Empty categories clearly explain how to qualify.

Only approved signed-in accounts can read the shared roster and records. Nicknames and game statistics are shared within that approved group. Emails are not stored in these shared documents. Future public distribution, especially to children, needs a separate privacy and consent review; this update is a private family setup, not a public child-account system.

## Saving and migration

Sign in **before** starting a run. Results are bound to the account present at the start, queued under its UID, and uploaded using an immutable receipt so retries do not add the run twice. The Firestore rules verify the matching aggregate calculation and block editing another player's records. In-browser measurement is still client-controlled: this is friendly family scoring, not a server-authoritative anti-cheat system.

Guest practice remains local and is kept separate from registered progress. Old anonymous backup data is preserved but is not guessed into new lifetime statistics: it did not contain the run history needed to reconstruct points, completions and streaks. The new Hall starts with signed-in results from this update.

Registered Google accounts can recover uploaded records on another device by signing into the same account. Unsent runs stay on the original browser/device. Do not clear site data while runs are pending. Unavailable browser storage is reported; those results remain in memory only until upload. A connection error never intentionally substitutes zeroes for another player's missing records.

## Adding anyone later

Only the master sees **Master Controls**. Future players sign in and share their new James User ID. The master enters that ID and a nickname, checks the confirmation, and approves them. This is optional and not part of the initial one-player setup. The master may pause/restore another player's access without deleting records. The configured master itself cannot be disabled, removed or demoted in the app.

## Deployment and testing

Both repositories must publish their new builds. The hub pins the racer's shared-account module as a Git submodule so both apps use the same identity and data model. GitHub Pages needs **Settings → Pages → Source → GitHub Actions** in both repositories.

Automated checks cover model arithmetic, tie handling, per-account cache/outbox isolation, Firestore access and atomic updates in `demo-james-game-center`, and local Chromium UI flows using test fixtures. The fixtures are not production users and are never uploaded to the live Firebase project. The generated `qa/center-report.json` identifies that scope. Real Google popup sign-in, live rules activation and physical iPhone Safari behavior still require the owner's live setup test.

App Check enforcement is not configured by this update. Do not enable enforcement before adding and testing the client integration. No service-account keys, master passwords or server secrets belong in the public repositories.

Official references:
- Google authentication: https://firebase.google.com/docs/auth/web/google-signin
- Rules conditions and atomic getAfter checks: https://firebase.google.com/docs/firestore/security/rules-conditions
- Transactions and retry behavior: https://firebase.google.com/docs/firestore/manage-data/transactions
- Firebase public web keys: https://firebase.google.com/docs/projects/api-keys
