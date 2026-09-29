# Emerald object family — first Hulk gameplay slice

Scope: five static designs together. No other world or character is required before the first test. Authoritative order: [Art Bible v1.3](../../../production/art-bible-v1/ART_BIBLE_v1.3.md).

| Asset | Existing game kind | Design |
| --- | --- | --- |
| park.power-gem | gem | Emerald double-pyramid crystal with softened bevels, broad facets and clear symmetry. |
| park.golden-star | special | Thick, rounded five-point gold star, simple and friendly, no face or writing. |
| park.moss-rock | rock | Low gray boulder with irregular broad base, a small moss cap and readable mass. |
| park.bumper | orb | Charcoal rounded floating bumper with violet band and warm warning details; no gem-like facets. |
| park.goo | goo | Low violet irregular puddle with a few rounded bubbles; not a reward and not a liquid splash effect. |

## Shared art recipe

Polished toy-like dimensional storybook rendering; modestly elevated front-three-quarter camera; soft upper-left light; clear outlines at small size. Isolate every object with generous space. No hero, title, labels, panel frame, environment, ground shadow, explosion, aura or speed trail. Reward highlights are contained within the object.

Suggested source layout: six equal cells in a three-column/two-row grid. Top: gem, star, rock. Bottom: bumper, goo, empty. Five designed objects only. The empty cell is intentional, not a missing required design.

## Review before extraction

Inspect shape/camera/material consistency, five-point star count, hazard/reward distinction and near/mid/far readability. Verify actual alpha rather than trusting a transparency claim. A source sheet is not an atlas or a ready-made collision mask.

## Packaging target

Preserve the source. Export separate aspect-preserving RGBA canvases, up to 512-square source and 256-square runtime; no stretching. Center anchors for floating pickups/bumper and bottom-center anchors for ground hazards. Record visible bounds and intended world footprint separately. Ground shadows and FX remain independent. A static bob is enough for a first prototype; full spin animation is deferred.

## Status at brief creation

Specified; no source or export bytes are counted as delivered by this brief. New generation must receive a real file/hash/status record. No gameplay or Firebase change is included.
