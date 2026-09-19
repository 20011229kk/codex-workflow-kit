# Why Two of Our First Twenty Workflow-Selection Cases Failed

Codex Workflow Kit began as an attempt to make a personal development workflow reusable: do simple work directly, add planning when decisions matter, and require evidence for behavior changes. It contains eight skills adapted from [Superpowers](https://github.com/obra/superpowers), with optional project rules. The source lineage is Superpowers v6.2.0; MIT attribution and file-level provenance are retained in [our source notes](../sources.md).

The first twenty-case selection evaluation passed eighteen cases. The two failures were small but instructive: a verification skill was being chosen where another full workflow did not help the requested deliverable.

## Failure One: Running an Existing Check

Case 03 asked only to run the project's existing check command and report its exit status. The model selected `cwk-verify`. Our rubric expected no workflow skill: the task already specified the operation and deliverable.

The original description covered assessing evidence for substantive changes or integration readiness. That was broad enough to attract a request containing a check command even though no readiness judgment was requested.

## Failure Two: Reviewing a Patch

Case 14 asked for review only: a patch skipped a permission-denial test and claimed checks passed. The review skill was appropriate, including checking the weakened quality gate. The model also selected `cwk-verify`, adding a second workflow to the review-only task.

We narrowed the verification description to completion/integration claims for implemented changes and explicitly excluded ordinary command execution and code-review-only requests. The review requirement remained; we changed the selection boundary, not the expected safety judgment.

[The original requests and failures](../evidence/routing-skills-only-2026-09-18/score.json) remain public, alongside the exact catalog supplied to the model.

## A Third Boundary Appeared

The second run passed nineteen cases. Case 17 added `cwk-design` while continuing unaffected work from an approved plan, even though a separate product decision was pending. We clarified that the design skill should not reopen already-approved execution merely because independent work remains unresolved.

The final catalog passed all twenty cases in that campaign. Expectations were not weakened. These are **selection observations against a supplied catalog**, not proof of host auto-loading accuracy or universal reliability. The same cases informed the refinements, so this is not an unseen holdout benchmark. [Run details and limits](../validation.md#real-model-selection).

## Selection Is Only One Layer

We also exercised eight distinct synthetic task scenarios: a small edit, a regression fix, a complex approved plan, continuing existing authorization, a non-Kiro project, a high-risk review, Superpowers coexistence and an independent-review gate. Requests, original events and before/after files are retained. Artifact checks and supervisor transcript review are different kinds of evidence; neither should be mislabeled independent code review.

The tool harness has 52 offline tests. An independent release review found three harness issues involving subprocess environment isolation, endpoint redaction and timeout evidence. Those were corrected and stored task artifacts replayed through the corrected checks. See [validation](../validation.md) for the precise scope.

## Watch One Actual Repair

[The short demo](../demo.md) replays a fresh isolated Codex run fixing the upper bound of a small `clamp` function. It shows the regression fail, the implementation change and the tests pass. Idle time is shortened and excerpts are typeset from the recorded output; the video is not a wall-clock speed claim.

This is a deliberately small example that is easy to inspect. It does not establish behavior on production repositories, every model, or every operating system. We have not run a matched speed or cost comparison with Superpowers, and do not claim superiority.

## Try It and Tell Us Where It Adds Friction

The published beta is [on GitHub](https://github.com/20011229kk/codex-workflow-kit). Native installation was validated with Codex CLI 0.153.4 on macOS arm64:

```sh
codex plugin marketplace add 20011229kk/codex-workflow-kit --ref v0.1.0-beta && codex plugin add codex-workflow-kit@codex-workflow-kit
```

Start a new session, explicitly select a kit skill, and use a disposable task. Keep existing project rules and choose one equivalent workflow provider per task. Namespacing alone does not resolve competing instructions.

We are looking for [five actual trial reports](../beta-trial.md), including installation failures. The useful questions are concrete: could you install it, did it choose the expected workflow, and did it ask you to repeat decisions already made?
