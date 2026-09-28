# Production plan — v1

## What is done in this handoff

The art bible, five written costume briefs, three world briefs, 64-frame first-hero schedule, design tokens, 153-entry asset register, atlas packer, validator and browser review page are supplied. Script checks apply to the tools, not to finished art or a shipped game. The source references already exist; new production sprites do not.

## Immediate batch: identity before animation

1. **Five-costume lineup candidate.** Same Jamesy face, orange hair, 4 shield and J belt across all costumes. Render on a quiet background, at the same scale, with full silhouettes. Label it concept / candidate outside the art. Do not call it a sprite atlas.
2. **Hulk five-pose proof.** Front-three-quarter, rear, rear-left lean, rear-right lean, Smash contact. Compare at 96px and at gameplay size. Check hands, boots, cape, emblems and camera elevation against the original cartoon.
3. **Eight-frame rear run proof.** Use a controlled rig or individually corrected frames after the five poses are stable. A generated contact sheet is a reference for redraw, not automatically usable motion. Keep consistent canvases and a single ground anchor.
4. **Emerald composition proof.** One hero pose, common gem, special star, rock, bumper and goo on a simple track. Build separate background layers. Place prototype HTML controls without changing the current live UI.

Identity drift, opacity errors, frame jitter or an unreadable route means revise the proof. Do not multiply the defect into all five heroes.

## Gates and review roles

| Gate | Responsible role | Exit evidence |
|---|---|---|
| G0 — Bible | Producer / Sean | Versioned decisions and asset IDs; direction accepted in conversation. |
| G1 — Character | Character artist / Sean | Approved lineup and Hulk five-pose comparison. |
| G2 — Motion | Animator / art reviewer | Eight-frame proof, then 64 unique frames; anchor / alpha / continuity review. |
| G3 — Composition | Environment artist / UI developer | Emerald layer stack, five object types and portrait / landscape HUD proof. |
| G4 — Playable slice | Game developer / tester | Hulk + park ID in an isolated renderer adapter; controls and existing records verified. |
| G5 — Expansion | Art + game developer | Two additional worlds; then four hero families, one at a time. |
| G6 — Release | Sean / tester | Visual acceptance, physical iPhone run, regression evidence and rollback commit. |

These are responsibility categories, not assigned people or unattended work. No promised dates are implied.

## First playable slice

Include one finished Hulk costume; Emerald Skyway presentation (stored ID park, index 0); rear-view animation; two treasure types; three hazards; jump, Smash, Thunderclap and burst; results; existing score events; pause and sound settings; gentle effects; responsive touch / keyboard controls; current Hall of Fame and player-card routes.

Defer four alternate heroes' finished animations, new physics, multiplayer races, score formulas, voiced cutscenes, purchases, authentication rewrites, Firebase changes, migrations and full tunnel-loop cameras.

## Integration constraints

- Re-check current main. Documentation snapshots: racer 47d8291eadd9c0848dee38dc508b67f3129b6d11; hub 40a1f4b2355e8e920ecd8a53cdc115cb47c75b49.
- Preserve logic and account adapters. Proposed visual interface: setPose(state), setPower(stage), dispose(). These are not shipped interfaces yet.
- Game events are authoritative. The renderer consumes them, never grants score or writes accounts itself.
- Test only the selected hero and world. Use current dependency pins; no engine upgrade is required for the art pass.
- If abilities later change scoring opportunity, decide rules-version and category policy before combining records. Never silently reset boards.
- Runtime manifest accepts only production_ready files with hashes and approval metadata.
- Preview accounts and scores belong only in demo fixtures, never production Firebase.

## Work items and done

Use asset IDs and revisions, not final-new-v2.png. Every review records asset, state/view, frame range, defect and expected correction. Preserve the identity reference and last approved revision.

Done means real approved art in a playable build, legible hazards and controls, reviewed worlds, honestly labeled unavailable heroes, intact accounts / history, device testing and owner approval. A PDF, lineup or tool-test result alone is not a completed reboot.

## Package scope

The full downloadable production kit also contains the machine-readable asset register, written hero/world briefs, approval checklist, prompts, packer, validator and local review page. This document-only GitHub branch starts by versioning the editorial source and first-hero contract without touching the game.
