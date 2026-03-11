# Changelog

All notable changes to this staged repository will be documented in this file.

## [Unreleased]

### Added
- Initial repository staging metadata for `personal-agent-skills`.
- `.gitignore` rules to keep live workspace state out of the staged repository.
- `manifests/skills.yaml` describing the current initial manifest batch.
- `manifests/compatibility.yaml` documenting packaging and runtime assumptions.

### Clarified
- Distinguished **live workspace candidate skills** from the **initial manifest batch** to avoid mixing “currently exists in workspace” with “already formally included in repo”.
- Locked the current initial manifest batch to exactly three skills:
  - `openclaw-x-intel-report`
  - `proactive-agent`
  - `self-improving-agent`
- Documented that `skills/` must not contain empty placeholder subdirectories; a skill directory is created only when real content has entered the repo.
- Aligned README, architecture, install, migration, safety checklist, and manifests around the same packaging boundary.

### Packaging decisions
- Skills are staged via per-directory symlink entries.
- Templates use `copy_if_missing` to avoid overwriting existing local files.
- Live workspace state is explicitly excluded from packaging, including:
  - `memory/`
  - `reports/`
  - `.learnings/`
  - session state / WAL / local cache
  - Gateway runtime config and state
- Gateway changes remain out of scope for this repository.
