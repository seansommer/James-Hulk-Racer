# James account setup — email and nickname (v1.3)

This replaces the earlier User ID / master-device instructions. No Firestore database, Google sign-in, codes, account import, or score migration is needed.

## The only setup

1. Select Firebase project **james-game-center**. Under **Authentication → Sign-in method**, enable **Anonymous** if it is not already enabled.
2. Open **Realtime Database → Rules** for `https://james-game-center-default-rtdb.firebaseio.com/`. Paste the complete **personalized v1.3 rules file supplied privately to the owner**, replacing the earlier rules, and press **Publish**.
3. Refresh both James websites. Open the sign-in form, enter the existing master email address and nickname **Sean**, and press **Sign in**.

The first matching sign-in atomically creates `jamesV1/members/sean` as the single **Sean · Master** player. All scores start at zero. Further sign-ins, including other browsers, open this SAME player using the same pair. Nothing must be copied from Authentication into Data. Do not add `_admin/masterUid`, `masterDevices`, or any Firestore document.

The account does not appear before a successful matching sign-in. A permission error means the replacement rules have not been published to the correct database. The public rule file on GitHub/the website is a safe TEMPLATE with `OWNER_LOGIN_KEY_GOES_HERE`; it deliberately cannot activate a new master. Use the personalized file, not that template or the earlier v1.2 file.

## Privacy and access

The personalized rules reserve the owner's existing email/nickname matching key. Neither the actual email nor its matching key is embedded in the public game source or the public rules template. Keep the personalized rules file private; do not commit it to GitHub. A nickname alone, wrong pair, or first visitor cannot create the master. Browser clients cannot create a second master, alter the account's role, or change its sign-in identity.

This is the requested trust-based family sign-in model, not verified email authentication. Anyone who knows the correct pair can use that account, including Master access, from another browser. There is no additional device-authorization step. The pair must be treated as private sign-in details. Scores are measured by the client for friendly family play, not cheat-proof competition.

## What appears in Realtime Database

`jamesV1/members/sean` contains the display nickname, Master role, active flag, and joining timestamp. `jamesV1/identities` and `jamesV1/loginLookup` hold private matching records, not raw email addresses. `jamesV1/sessions` stores each browser's selected profile automatically. Registered race results go to `jamesV1/racerRuns/sean`.

Earlier experimental root-level requests are left untouched and are no longer used. They do not appear as players. No family or SUJA data is accessed. The new namespace starts fresh, and no old scores are imported. Local practice remains separate.

## Additional players later

Leave **Add a player later** closed to keep the initial roster limited to Sean. When ready, the master enters the intended person's email and nickname in that form and explicitly adds them. They sign in with that pair. No User IDs are required. Pausing a player blocks their shared-record access without deleting history.

## Verification

The demo-emulator suite tests first sign-in, incorrect details, two browsers sharing one master, concurrent activation, role protection, adding ordinary players, immutable race results, and absence of raw emails. Browser tests verify the preserved Hall of Fame/cards and email/nickname form. They never create production players. Live sign-in requires the owner to publish the personalized rules first.
