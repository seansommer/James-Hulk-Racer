# Launch James Game Center and Jamesy The Hulk Racer

## 1. GitHub Pages — both repositories

Open each repository: `James-Game-Center` and `James-Hulk-Racer`.

1. Go to **Settings → Pages**.
2. Under **Build and deployment → Source**, select **GitHub Actions**.
3. Open **Actions**, choose the publish workflow, and use **Run workflow** if the initial deployment ran before Pages was enabled.
4. Wait for both the build and deployment jobs to turn green.

The addresses are case-sensitive project paths:

- https://seansommer.github.io/James-Game-Center/
- https://seansommer.github.io/James-Hulk-Racer/

The racer generates its real preview pictures during the build. Until its first successful publish, the hub's linked preview pictures may show their gradient fallbacks.

Reference: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## 2. Optional cloud backup — only the new James Firebase project

**Project ID: `james-game-center`. Do not change rules in the existing family or SUJA Firebase projects.**

The game already saves on the current device. Firebase is only needed for the optional private backup button.

1. Open the Firebase console and choose **james-game-center**.
2. Open **Authentication → Sign-in method** and enable **Anonymous**.
3. Under **Authentication → Settings → Authorized domains**, add `seansommer.github.io` if it is not already present. Enter the domain, not a repository path.
4. Open **Build → Firestore Database** and create the default database. Use **Standard edition / Native mode** where these choices are shown. Choose a suitable region and start with **Production mode**, not open Test mode.
5. Open that database's **Rules** tab. Replace its contents with the complete [`firestore.rules`](../firestore.rules) file and click **Publish**.
6. In the game or hub, open the hero nickname in the header, then press **Connect cloud backup**. A successful connection says **Private cloud backup connected**.

No Storage bucket, Realtime Database, Cloudflare Worker, SerpApi key, server service account, or paid image service is needed for this game. This app never requests access to your previous Firebase databases.

If the rules are not published, the application explains the cloud error and continues saving locally. The included rules restrict each player to their own private record, reject unexpected fields and invalid values, and deny profile listing. They do not create an anti-cheat leaderboard.

Before broader public promotion, review the Firebase project's API-key API restrictions and quotas, and configure/test App Check for supported services. App Check is not enabled in this initial code, and its enforcement should not be switched on before the client integration is ready. The repository cannot verify or modify your live Firebase console settings.

Firebase references:
- https://firebase.google.com/docs/auth/web/anonymous-auth
- https://firebase.google.com/docs/firestore/security/rules-fields
- https://firebase.google.com/docs/projects/api-keys
- https://firebase.google.com/docs/app-check

## 3. Try it on the phone

Open the hub in Safari, launch the racer, and start in **Little Hero** mode. Try portrait and landscape. Hold a steering arrow while pressing Jump. Collect until Smash and Thunderclap unlock. Turn the music/effects sliders down to a comfortable level.

Use Safari's **Share → Add to Home Screen** for an app shortcut. The initial load needs internet. The service worker caches the built game shell afterward; cloud saving still needs connectivity. First-time users of a new device start a new anonymous profile rather than recovering a previous device's identity.

## 4. Confirm the first run

Finish one world, go back to the hub, and check that the treasure and medal totals match. Refresh both pages; the nickname and local progress should remain. Test cloud backup separately after completing Step 2.

A generated browser test report is published at `/James-Hulk-Racer/qa/`. These automated Chromium checks do not replace a real iPhone Safari test.
