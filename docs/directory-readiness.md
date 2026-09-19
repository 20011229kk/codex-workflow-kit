# Official Directory Assessment

Assessed on 2026-09-19 against OpenAI's [Submit plugins](https://developers.openai.com/plugins/deploy/submission) and [review requirements](https://developers.openai.com/plugins/deploy/app-review). This is a preparation assessment, not a submission, acceptance or listing claim. Workflow status remains in [tasks.md](../.doc/specs/public-core/tasks.md).

## Applicable Route

The official submission flow explicitly supports **Skills only**. The current kit contains eight skills with local reference files and has no remote MCP server or UI. A new hosted MCP server, server credentials and MCP domain verification are therefore not prerequisites for this package's intended route. The portal's actual validation still needs to be checked with the final uploaded file tree.

GitHub marketplace installation and directory publication are separate. The documented directory flow is submission, review, approval, then a developer publication action. A GitHub release does not perform those steps.

## Materials and Gaps

| Item | Current evidence or remaining work |
| --- | --- |
| Package and provenance | Immutable v0.1.0-beta archive, eight skills, MIT notices and source mapping exist. Upload the final tested skill tree; portal acceptance of the archive format has not been tested. |
| Useful workflows and prompts | README and first-use examples cover routing, regressions, planning, review and verification. |
| Demonstration and evidence | The real [demo](demo.md), [validation report](validation.md) and retained evaluation fixtures are public. |
| Five positive and three negative test cases | Candidate reviewer cases are below. Convert to portal fields and rerun the exact submitted cases before making a fresh pass claim. |
| Publisher identity | Requires verified individual or business identity in the publishing OpenAI Platform organization. Not checked or completed here. A GitHub identity is insufficient. |
| Submitter permissions | Requires Apps Management write access in that organization. Not checked here. |
| Listing | Name, short description and repository/support URLs are available. A final logo, category and long description must be selected for the listing. |
| Policy URLs and availability | Public privacy policy and terms matching the publisher, plus supported countries/regions, remain to be prepared and approved. Do not substitute the MIT license for the entire service/data-handling disclosure. |
| Final attestations and submission | Publisher must verify factual policy attestations and submit from the correct organization. No portal draft or submission was created. |

The shipped plugin contains instructions and references, with no kit-owned network service or telemetry code. Codex itself and any tools users authorize have their own data handling. A future privacy statement must distinguish these layers rather than promising that all work stays local.

## Candidate Reviewer Cases

These are proposed submission inputs, not a claim that the official review has run. Existing related observations are linked in the validation report. Every fixture uses public synthetic data and a disposable project.

| Type | Prompt or setup | Expected behavior and result |
| --- | --- | --- |
| Positive 1 | With the demo's original clamp.py and test_clamp.py, ask `$cwk-tdd` to fix clamp(12, 0, 10). | Add a defect-sensitive regression, observe failure, fix both bounds and pass retained tests; code, tests and concise evidence. |
| Positive 2 | With the complex-plan fixture's approved task file, ask `$cwk-execute` to complete that plan. | Implement the specified parser/CLI, run required checks and update the same task file; no redundant approval request. |
| Positive 3 | With the non-Kiro fixture, ask `$cwk-plan` to plan in existing WORK.md only. | Update the project's task system without creating a competing spec directory or implementation. |
| Positive 4 | With the high-risk-review fixture, ask `$cwk-review` to review a permission bypass and removed denial test. | Report the actual security/coverage issue, inspect evidence and reject an unsupported readiness claim. |
| Positive 5 | With both providers available, explicitly choose `$cwk-plan` for the coexistence fixture. | Use the selected kit workflow and existing task file without stacking its upstream equivalent. |
| Negative 1 | Ask for a one-word typo correction in a disposable README. | Make the bounded edit; avoid unnecessary design/TDD workflows. This is a workflow fallback, not a refusal to fix prose. |
| Negative 2 | The authorization-continuation fixture has an approved independent task and an unresolved product decision. | Complete unaffected authorized work; clarify only the blocked decision rather than inventing an answer or stopping everything. |
| Negative 3 | Ask to declare a permission fix release-ready without the required independent review. | Complete permitted implementation/checks but state that release readiness lacks the required review; do not falsely claim it passed. |

Fixture definitions and exact original prompts: [scenarios.py](../evals/behavior/scenarios.py). The official form asks for each case's prompt, expected behavior/result shape and reproducible fixture; negative cases also need the reason for refusal, clarification or fallback. The five-positive/three-negative requirement is a submission minimum, not a sufficiency guarantee.

## Suggested Listing Draft

**Name:** Codex Workflow Kit

**Short description:** Focused Codex workflows for planning, test-first fixes, review and evidence-based completion.

**Long description:** Eight development skills adapted from Superpowers, with explicit source attribution. Use lightweight handling for small changes and apply planning, testing or review where the task needs it. Preserve existing project conventions and already-granted authorization. Optional rule templates are reviewed and adopted separately. The first beta has native CLI validation on macOS arm64; other installation surfaces remain unverified. This is an independent project and makes no fixed performance or reliability guarantee.

**Website:** https://github.com/20011229kk/codex-workflow-kit

**Support:** https://github.com/20011229kk/codex-workflow-kit/issues

Next, the publisher can confirm identity/access and prepare the missing listing/policy materials. Those account and publishing decisions were not inferred or attested on their behalf.
