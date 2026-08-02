# MediaForge

MediaForge reads embedded metadata, normalizes filenames,
organizes media into a canonical library, and synchronizes
that library to offline destinations such as USB drives.

## Goals

- Organize music downloaded from MeTube
- Normalize filenames
- Extract metadata when available
- Produce consistent filenames
- Safely copy music to the BMW USB drive
- Never overwrite files
- Support dry-run mode
- Provide an OpenClaw skill for AI-driven organization

## Project Structure

```
mediaforge/
├── config/
├── docs/
├── logs/
├── scripts/
├── skills/
├── src/
└── tests/
```

## Current Status

🚧 Under development.

The first milestone is implementing a deterministic music organizer that can:

1. Scan the MeTube download directory
2. Parse artist/title information
3. Generate normalized filenames
4. Preview planned changes
5. Apply approved changes

## Principles

- Local-first development
- Deterministic behavior
- Git is the source of truth
- Dry-run before modification
- Never destroy source files
- Extensive logging