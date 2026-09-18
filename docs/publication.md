# Release Procedure

Completion state lives only in [the beta tasks](../.doc/specs/public-core/tasks.md). The target repository is [20011229kk/codex-workflow-kit](https://github.com/20011229kk/codex-workflow-kit).

## Review Gates

Review the actual file set, source notices, English documentation and requested scope. Confirm maintainer rights to distribute original contributions under MIT; attribution is not a substitute for that confirmation. Review changes against Superpowers v6.3.0 without changing the retained source lineage or claiming unsupported performance benefits.

Run the fast commands in README. Inspect the complete runtime bundle and actual native lifecycle evidence. Review model transcripts and fixture outcomes separately from tool tests. An evaluation failure remains evidence: fix the cause or explicitly retain the affected release gate as pending; do not silently remove cases.

The user-created repository's initial history must be preserved. Use a normal branch and ordinary reviewable commits; do not force-push or import private repository history. Commit/push/tag/release actions require applicable user authorization.

Prepared text for the first beta is in [v0.1.0-beta release notes](releases/v0.1.0-beta.md). Remove its preparation-only notice only after the release gates are satisfied.

## Versioned Artifact

Keep VERSION and the plugin manifest version identical. Build with:

```sh
python3 scripts/release.py check
python3 scripts/release.py build
```

The builder emits a deterministic ZIP containing the complete installable marketplace and BUNDLE.json. It refuses to overwrite an existing output. Record the archive SHA-256 in release notes and attach the reviewed archive to the matching version tag. Verify that the tag points to the reviewed commit and that its hosted fast checks pass. A local green run is not a hosted CI result.

## Repository Configuration

Enable issues and verify the issue/PR templates, configure GitHub private vulnerability reporting, and update SECURITY.md after checking the live reporting route. Record the repository description and supported scope. A prepared workflow file does not prove hosted checks have run.

## Update and Rollback

Publish content changes under a new version. Users install the desired tag or archive and start a new session. A moving-branch marketplace needs a refresh followed by plugin reinstall; a pinned tag remains pinned. Roll back by registering and reinstalling a previously verified version, preserving project rule edits. See [adoption](adoption.md).

Public GitHub release and official plugin-directory submission are separate steps. Official directory submission and additional platform support are outside this beta's initial distribution route.
