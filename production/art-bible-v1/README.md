# Storybook arcade production — identity revision v1.1

**Start with [EMBLEM_REVISION_v1.1.md](EMBLEM_REVISION_v1.1.md).** The owner approved the five-costume lineup and requested **J instead of the age-based 4** on every chest emblem. The belt keeps J; the Captain-style shield also uses J. This revision supersedes numeral-emblem instructions in the original bible and any earlier reference images or exports.

Then read [ART_BIBLE.md](ART_BIBLE.md), the original v1.0 editorial baseline, and [PRODUCTION_PLAN.md](PRODUCTION_PLAN.md). [animations.json](animations.json) defines the first 64-frame Hulk package. [sources.json](sources.json) pins the application/account references. Technical numbers such as frame counts and world indices are unchanged.

This review branch versions documentation and specifications only. It changes no application source, dependencies, Firebase rules, account records, score logic or deployment workflow. Do not merge it as though it were the new playable renderer.

## Current status

- Storybook arcade / 2.5D direction: accepted by the owner.
- Five-costume lineup: accepted as a visual reference, with the new J-emblem correction.
- Current emblem rule: upright white J on the chest, existing J on the belt, J on the Captain-style shield; no age numeral in new branding.
- Next review: Hulk front-three-quarter, rear, both rear steering leans, and Smash-contact proof.
- Production animation frames, transparent sprites and world layers: not yet approved by the lineup decision.
- Renderer and shipped icons: existing game remains unchanged during art review.
- Accounts: existing v1.3 email/nickname flow preserved; Sean remains the sole initial Master; no sample roster or scores.

## Production order

Approved lineup with J correction → Hulk five-pose proof → eight-frame rear run → Emerald composition → isolated playable slice. Fix identity, transparency, anchors and loop defects before expanding the roster.

## Earlier companion kit

The prior handoff describes a separate **Jamesy Art Production Kit v1**, including an illustrated 22-page PDF, editable Markdown, reference images, hero/world briefs, design tokens, asset register, approval checklist, prompts, atlas tooling and a browser review studio. Those larger companion files are not represented as committed in this documentation-only branch. Their v1.0 numeral-emblem instructions are historical and superseded by the v1.1 revision; they have not been re-exported by this commit.

## Verification scope

The original handoff recorded 11 Python toolkit checks, seven local Chromium review-tool checks using synthetic fixtures, and visual inspection of 22 PDF pages. Those earlier checks do not validate this new artwork, approve production animation, test a rebuilt game or replace physical iPhone testing. This revision records a design decision and the next proof specification only.
