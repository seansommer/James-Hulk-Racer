# James project checkpoint — 28 September 2026 / Jump 04

## Overall assessment

**Software foundation built; visual reboot in production; not release-ready.** The project is not starting from scratch, but completed source code and attractive still art do not mean the new game presentation is assembled or tested.

## Artwork and graphics

The current art bible v1.2 defines a dimensional storybook 2.5D presentation and a consistent five-costume Jamesy lineup. Permanent upright J branding replaces the old age numeral. Actual source files, transparent exports, checksums, manifests and review viewers are stored on the art branch.

Hulk has 29 selected drawing candidates across rear idle, run, both banks, jump and land, plus six separate pose studies. The 64-frame first-hero plan still requires the action/reaction/presentation clips and a unified motion-polish pass. None of this count implies automatic final approval. The other four costumes are at reference-design stage. Items, layered environments, interface graphics and effects are still to be produced as groups.

The strongest progress is visual identity and reusable asset preparation. The biggest remaining risk is temporal consistency: a pose may look polished alone yet change head scale, cape shape, stride rhythm or contact timing when played. Treat this as a motion-review problem rather than generating more general style posters.

## Racer foundation

`James-Hulk-Racer/main` contains the original procedural 3D half-pipe game: three themed worlds, automatic forward running, steering, collectibles/hazards, jump, Smash, Thunderclap, power progression, two difficulties, audio/effect settings and score persistence. The authored sprite-based visual reboot is not integrated into that renderer.

## Game Center foundation

`James-Game-Center/main` contains the hub, game/world links, six Hall of Fame categories and Player Cards with nickname, role, lifetime/per-world records and medals. Shared account modules are pinned through the racer submodule. The v1.3 system is the familiar email/nickname matching flow over Anonymous Authentication and Realtime Database. It is designed to create only Sean as initial Master after the owner's private rules are activated; no extra players or sample scores are part of art work.

This describes repository implementation, not verified live database state. Trust-based matching is not verified email authentication. Never publish the private matching key or personalized rules in artwork/source control.

## Remaining whole-project stages

1. Complete the character-art group and its combined motion/identity review.
2. Produce item families, layered world kits, matching menus/icons/cards/Hall decoration, and separate effects.
3. Assemble the new 2.5D presentation against the existing simulation and account interfaces; keep score rules and world identifiers stable.
4. Apply the matching visual identity to the hub, then test cross-app navigation, sign-in/progress and rankings without importing or resetting records.
5. Verify performance, controls, readability, sound, pause/resume, saving and installation behavior on physical iPhone/Safari and other target devices. Confirm the live Firebase setup separately from emulator tests.
6. Release only after the combined visual/game/account checks and owner acceptance, keeping a rollback point.

The user-requested art order stays characters → items → environments → interface → effects → assembly. Small offline sprite reviewers belong within the art stage; they are not a live-game rollout.

## This handoff and next

Jump 04 adds six rear jump and three landing candidates, transparent files and a one-shot review viewer. Next: rear-view Smash and Thunderclap action frames. The existing art bible PDF is unchanged; this status note and the per-batch review ledger track new work.

## Evidence

Repository README files inspected in this session:
- https://github.com/seansommer/James-Hulk-Racer/blob/main/README.md
- https://github.com/seansommer/James-Game-Center/blob/main/README.md

Art decisions and current counts:
- `ART_BIBLE_v1.2.md`
- `../../art/PROGRESS.md`
- `../../art/01-characters/hulk/jump-reviews/v01/REVIEW.md`

Art tests do not prove that production rules are published, that all real accounts work, or that a physical device meets the intended frame rate.
