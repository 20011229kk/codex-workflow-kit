# Sources and Maintenance

## Superpowers

Upstream: [obra/superpowers](https://github.com/obra/superpowers).

Pinned base: v6.2.0, commit 3dcbd5c4b48e02263fbf4a3c01e3fe4f81d584d9. Copyright (c) 2025 Jesse Vincent. The complete license is retained in [Superpowers-MIT.txt](../licenses/Superpowers-MIT.txt).

This package further adapts eight core entries from personal customization commit 469b80d. It is neither a complete upstream mirror nor a claim to contain the latest release. Exact input files and their original digests are recorded in [source-files.json](source-files.json). Files under plugins/codex-workflow-kit/skills/ retain the Superpowers MIT notice conservatively as derived material; quality-gates.md is a locally added method.

Public names and directories are mapped in [skill-names.json](skill-names.json). The current upstream v6.3.0 comparison is recorded in [upstream-comparison.md](upstream-comparison.md).

Main changes include independent cwk names, narrower triggers, authorization continuity, preserved quality gates, reuse of valid evidence, project-selected documentation formats and removal of required dependencies on omitted workflows. Upstream plugins and session hooks are not included.

## Method References

- [OpenAI skills and prompts article](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra): task-specific activation and on-demand loading. This is a method reference; the article body is not reproduced and does not prove this package's performance.
- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/c004a74784a08295d52749b04cda634125b9a581): ideas for reviewing quality-gate changes and separating structural, selection and behavior evaluation. Its code and substantial template passages are not copied.

## Project-authored Material

Templates, public documentation, evaluation utilities and English cases, and publication checks were authored or adapted for this project and are released under the root MIT license. The personal-workflow source label in source-files.json records local lineage; it does not identify an already public, accessible remote repository.

The maintainer confirmed publication authorization and MIT adoption on 2026-09-19. This authorization does not replace retained third-party notices. Other personal skills and internal business material are excluded.

## Update Method

Pin the upstream base, inspect the proposed version outside this candidate, compare each local adaptation, preserve user and project conventions, run relevant checks, and update provenance and CHANGELOG.md. Do not treat a wholesale upstream overwrite as a conflict-free update or upstream claims as validation of this package.

Source-file digests identify the original inputs and remain unchanged when editing the candidate. Candidate digests belong in PUBLICATION_MANIFEST.json. Review the actual diff and file scope before updating that manifest; adding every discovered file automatically would defeat the allowlist.
