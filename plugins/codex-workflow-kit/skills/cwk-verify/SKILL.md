---
name: cwk-verify
description: Assess completion or integration claims for implemented changes. Skip ordinary command execution and code-review-only requests.
---

# Verification Before Completion

Every completion claim needs evidence for the actual changed behavior. Reuse valid evidence; never reuse it solely because a report says "passed".

## Evidence identity and validity

For substantive work, identify the command/check, result, checked revision or actual working-tree content, and relevant configuration, dependency and environment assumptions. An existing task note or tool output is enough; do not create a second evidence ledger.

Reuse results only while those relevant inputs remain unchanged. A code/config/dependency update, merge resolution, changed external service state, or newly discovered uncovered risk invalidates affected results. A new message, skill transition or unchanged documentation comment does not. If identity cannot be established, run the smallest authorized check that resolves the uncertainty.

Read a truncated report at its source before rerunning. Missing or incomplete output is an evidence gap, not proof of failure or permission to repeat a state-changing operation.

Reuse unchanged failure output too: do not rerun a full command merely to change console formatting. Rerun when a relevant implementation, precondition or diagnostic hypothesis changes and the result would add evidence.

## Match the claim to the evidence

| Claim | Minimum meaningful evidence | Not sufficient |
| --- | --- | --- |
| Behavior bug fixed | Original failing behavior reproduced by a targeted check, then passing after the fix | New test only ever seen green |
| Inputs/permissions handled | Relevant allowed and rejected paths at the real decision boundary | Mocking the decision itself |
| Data mutation safe | State after partial failure/retry as relevant; intended boundary preserved | Happy path alone |
| Build/test suite passes | Completed applicable command, exit result and scope | Lint, partial output or another revision |
| Requirements satisfied | Requested outcomes checked against behavior/evidence | Test count alone |
| Ready to merge/release | Required checks and risk-triggered independent review on the current change | Implementer self-review called independent review |

Test-first evidence may come from a safe isolated pre-fix comparison. Never delete user code or repeat shared-environment mutations just to obtain a new timestamp.

## Close the actual gaps

1. Reconcile the user's and project's required commands, document structures and observable acceptance criteria with evidence. Keep their actual requirements intact; reuse existing task records rather than adding a second checklist.
2. Fix failures caused by this task and rerun affected checks. An existing failure that blocks an explicitly required gate must also be fixed when authorized and in scope. Otherwise report the blocked gate and partial completion; never label a required failing gate unrelated to claim full acceptance. Preserve genuinely unrelated baseline failures without expanding scope.
3. For permission, data-integrity, concurrency or cross-module protocol changes, identify the independent reviewer and reviewed diff. Without the required review, report implementation/test completion separately from integration readiness. Honor an explicit, project-permitted waiver without claiming review passed.
4. Report outcomes, verification scope, outstanding relevant failures, and unverified portions. Do not imply the whole suite or real deployment passed from local checks.

If tests, thresholds or suppression/exception settings changed, verify that passing results still prove the agreed contract; use the review [quality-gate checks](../cwk-review/quality-gates.md). Reuse an existing review when it covers the actual diff. A removed check needs a justified replacement or an explicitly accepted limitation, not an automatic rerun or blanket rejection.

This skill does not authorize new subagents, commits, deployments or environment changes. Small wording/configuration tasks need suitable inspection or validation, not ceremonial suites.
