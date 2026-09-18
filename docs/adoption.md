# Adoption, Updates and Removal

## Distribution Contract

The supported distribution is the complete `plugins/codex-workflow-kit` bundle, installed through the repository marketplace. Do not copy individual skill directories: cwk-verify references cwk-review resources. The release archive also includes the marketplace, INSTALL.md, VERSION and BUNDLE.json with content hashes.

Use [INSTALL.md](../INSTALL.md) for the local checkout/archive lifecycle. Native Codex commands own plugin cache and registration. The kit has no custom global synchronization engine and does not overwrite AGENTS or model settings.

## Git Marketplace

After the first public tag exists:

```sh
codex plugin marketplace add 20011229kk/codex-workflow-kit --ref v0.1.0-beta
codex plugin add codex-workflow-kit@codex-workflow-kit
```

A pinned tag gives a fixed source. To move to another version, remove only this marketplace registration, register the desired tag and reinstall. For a deliberately moving branch such as main, `codex plugin marketplace upgrade codex-workflow-kit` refreshes its snapshot, followed by `codex plugin add codex-workflow-kit@codex-workflow-kit`. Updating a moving branch does not change a pinned tag into a newer release.

Start a new session after installation, update or removal. Do not manually edit plugin caches. Reinstall from the intended version to roll back; preserve a copy of any project rules you adopted separately.

## Optional Rule Profiles

Installing skills does not install rule fragments. Review templates/AGENTS.core.md and merge only compatible clauses into the rule file your project actually uses. Keep its existing spec, ADR, issue and authorization conventions. Add the Kiro or delegation profile only when chosen; appending contradictory rules does not resolve them.

Evaluations declare `skills-only` or `core`. The former injects no core template; the latter uses that exact template in the test project. Kiro is not silently enabled in either profile.

## Removal and User Changes

Remove the plugin and its marketplace with the native commands in INSTALL.md. Unrelated plugins and project files should remain. Manually adopted rules are not removed automatically: review the current file and remove only the kit-related clauses, preserving later changes.

Never run the original personal workflow's sync commands against this package. That tool has a different scope and installation model.
