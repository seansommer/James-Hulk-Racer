# Publish and activate James Game Center

Both repositories use GitHub Pages with **Settings → Pages → Source → GitHub Actions**. The shared module in James-Game-Center is pinned to the corresponding James-Hulk-Racer commit.

- Hub: https://seansommer.github.io/James-Game-Center/
- Racer: https://seansommer.github.io/James-Hulk-Racer/

## Account setup

Use only Firebase project **james-game-center** and its **Realtime Database**. Enable Anonymous Authentication, publish the personalized v1.3 rules supplied privately to the owner, then sign in with the existing master email and **Sean**. The app creates one fresh master player automatically.

There are no User IDs to copy, device approvals to enter, JSON account imports, Firestore setup, or scores to migrate. The public rules file is an intentionally incomplete owner-key template. The privately supplied rules file is the one to paste into the Firebase Rules tab.

See [PLAYER_CENTER.md](PLAYER_CENTER.md) for exact instructions and the trust-based sign-in limitation. Do not follow the superseded v1.1/v1.2 master-device instructions.

## First play

Sign in, finish one Little Hero race, then open Player Cards or Hall of Fame and refresh. Local practice is separate from signed-in scores. On an iPhone, test portrait and landscape in Safari; browser automation is not a physical-device test.
