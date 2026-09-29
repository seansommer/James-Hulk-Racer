# Image-production workflow

## Current owner direction

Use the built-in image generator for new artwork. Do not use Runway for generation or transfers. Another paid service requires an explicit task-specific request. Reuse a suitable existing image rather than generating a duplicate.

**Current scope is Hulk first.** Make Emerald objects and the first environment kit, then test gameplay before the other four costumes. This supersedes the older instruction to finish all characters first. See [Art Bible v1.3](../production/art-bible-v1/ART_BIBLE_v1.3.md).

## Source discipline

Preserve original source bytes and hashes. Distinguish design candidates, processed review exports, approved source art and production-ready assets. Contact sheets, source copies and multiple export resolutions do not add animation counts. Pose or object approval is not automatic motion, collision or device approval.

## Direct native-image archive

Use direct GitHub source uploads or a supported binary write, without routing through an image service. Existing Victory 07 processing watches its exact source path, verifies its checksum and builds review exports locally.

When image bytes have not been transferred, record `pending_direct_upload`. A planned repository path, local file, source hash, workflow definition or text commit is not proof of an archive. Report `archived` only after the real image exists at the intended branch/path with matching bytes.

Keep original master, review exports and file manifest together. Do not create a new archive workflow per request unless needed; avoid repeatedly regenerating unrelated old art. The current art library stays separate from live game/account code and deployments.
