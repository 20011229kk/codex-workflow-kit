# Getting Started

## Prerequisites

Use the [tested CLI baseline](compatibility.md), a working Codex login and a source checkout or extracted release archive. Run `codex --version` first. If the command fails before starting, repair your Codex installation using its supported installer; installing this kit cannot repair a missing CLI binary.

## Install and Verify

From the kit directory, run the commands in [INSTALL.md](../INSTALL.md). `codex plugin list --marketplace codex-workflow-kit --json` should show an installed, enabled plugin with the expected version. Start a new session. Confirm the eight cwk skills are available; the UI may prefix them with `codex-workflow-kit:`.

Installation adds only the plugin. Decide separately whether your project should adopt the core or Kiro rule fragments. Preserve existing rule files and compare changes before merging.

## First Tasks

Try these in a disposable project first:

1. Ask `Fix codxe to codex in README.md; change nothing else.` Expect the wording fix without a planning cycle.
2. Give a reproducible bug and ask `Use $cwk-tdd to establish a regression check and fix this defect.` Expect a check that distinguishes the defect from the intended behavior, followed by relevant verification.
3. Provide an already-approved task file and ask `Use $cwk-execute to finish this plan in the current session, using this file as the only task record.` Expect continued execution within existing authorization.

A skill improves guidance; it does not supply missing business decisions, tools or permissions. Review the resulting changes and evidence. High-risk readiness may still require independent review.

## Existing Superpowers

Keep the upstream installation unchanged. For a kit task, explicitly choose a cwk skill or write a project preference for this kit. For an upstream task, explicitly choose Superpowers. Do not load both equivalent workflows to resolve a disagreement. See [compatibility](compatibility.md) for the exact tested scope.

## Finish the Trial

Use the removal commands in [INSTALL.md](../INSTALL.md). Verify that the plugin is absent from the installed list and start another new session. Manually adopted AGENTS clauses remain until you review and remove them; the host does not own those edits.
