# Launch James Game Center and Jamesy The Hulk Racer

## GitHub Pages — both repositories

Open each repository: `James-Game-Center` and `James-Hulk-Racer`.

1. Go to **Settings → Pages**.
2. Under **Build and deployment → Source**, select **GitHub Actions**.
3. Open **Actions**, choose the publish workflow, and use **Run workflow** if a deployment ran before Pages was enabled.
4. Wait for both build and deploy jobs to turn green.

Case-sensitive addresses:
- https://seansommer.github.io/James-Game-Center/
- https://seansommer.github.io/James-Hulk-Racer/

The racer generates actual game preview pictures during its build. The hub's linked game images require the racer's first successful deployment. Its own icons and sharing artwork build independently.

Reference: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## Version 1.1: master account and registered player records

**Follow the complete [Player Center activation guide](PLAYER_CENTER.md).** It supersedes the initial anonymous-backup setup. The roster starts with Sean's master account only, after private console activation.

Use only **james-game-center**, not the old family or SUJA Firebase projects. Enable **Google Authentication**, authorize `seansommer.github.io`, create the default **Cloud Firestore** database in Production mode if it does not exist, and publish the full current `firestore.rules`. Sign in on the website, copy your new James User ID, and privately set `_admin/launch.masterUid` to that exact UID in Firestore. Press **Check access** to activate the sole initial master card.

Do not enable open test rules. Do not use the old family profile ID or nickname as the Firebase UID. No private admin key or master password belongs in GitHub. The connected repository tools cannot configure the live Firebase project for you.

Local guest practice still works before account setup. It does not create a registered player or leaderboard record. Existing anonymous backups remain owner-private, but are not imported into the new Hall of Fame.

## Phone test

Open the hub in Safari, sign in to your approved master account, launch the racer, and start **Little Hero → Emerald Park**. Try portrait and landscape. Hold a steering arrow while tapping Jump. Collect until Smash and Thunderclap unlock. Adjust audio to a comfortable level.

Finish a run, return to the hub, and open Hall of Fame or Player Cards. Confirm it has uploaded and the new record appears under the correct difficulty. Refresh the pages; your identity and uploaded records should remain. Use the same Google account on another device to retrieve uploaded records. Verify there is exactly one approved player before adding anyone later.

Safari's **Share → Add to Home Screen** creates an app shortcut. Initial loads need internet. The service worker caches the built app shell; sign-in and uploaded records require connectivity. Pending runs remain on their original device, so do not clear site data before they upload.

The generated `/James-Hulk-Racer/qa/` reports distinguish automated game/UI tests from live Firebase and physical Safari checks. App Check enforcement is not enabled by this initial account implementation; do not switch on enforcement before integrating and testing the client.
