# Image-production workflow

## Current owner direction

Use the built-in ChatGPT image generator for new character artwork. Do not use Runway unnecessarily for image generation. Do not default to Runway for transfers either. Use another paid generation/editing service only when the owner explicitly requests it for a specific task.

Reuse a suitable image already attached or archived instead of generating a duplicate. Preserve original source bytes, record checksums and distinguish source drawings, processed review exports, approved production art and live integration.

Continue in groups: characters first, then items, environments, interface and effects. The existing art bible v1.2 and permanent J-emblem identity remain authoritative. Costumes are not player accounts.

## Direct native-image archive

Generated files can be uploaded directly to the art branch without going through an image service. The Victory 07 processing workflow watches its exact source PNG path, verifies the expected source checksum, creates local transparent review exports and commits the art-only result. It never generates an image or contacts Runway.

When this conversation's GitHub connector has not transferred image bytes, record the batch as pending_direct_upload. A local file, planned path, source hash or text commit is not evidence that the source image has reached GitHub. Never mark the archive complete until real repository files are present.

The next batch is documented in `01-characters/hulk/victory-reviews/v01/README.md`.
