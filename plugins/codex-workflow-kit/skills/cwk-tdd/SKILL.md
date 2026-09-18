---
name: cwk-tdd
description: Default TDD workflow for behavior bugs, complex or high-risk logic, and requested test-first work. Skip prose-only edits and tasks where the user selected another test-first workflow.
---

# Test-Driven Development

Prove that a test distinguishes the required behavior from the defect, then make the smallest coherent fix. Lightweight documentation does not waive regression evidence.

## When to use it

- For a reproducible behavior bug, establish a regression test before changing production behavior.
- Default to test-first for complex logic and permission, persistent-data, concurrency or compatibility boundaries. Follow stricter project rules.
- Plain documentation, instruction skills, generated assets or declarative configuration may need schema checks, realistic scenario evaluation or a safe execution check instead. Do not assert words/headings merely to manufacture a green test.
- Use this as the kit's TDD entrypoint. Honor an explicitly selected alternative without loading both. A user-requested exploration can remain throwaway without a complete test suite; keeping it as production behavior requires the appropriate checks.

## Red, green, refactor

1. Identify the observable contract, a boundary case that violates it, and the narrowest real test seam. Read existing callers and tests where they determine the contract.
2. Write/run the check on the unmodified behavior. Verify it fails for the intended assertion; an import error, unavailable service or missing fixture is not a demonstrated regression.
3. Change the root cause and rerun the same check. Include the valid-path behavior so rejecting all inputs cannot pass as a fix.
4. Add relevant failure/edge cases, then run affected integration and project-required checks. Refactor only within scope and rerun checks affected by that refactor.

Preserve existing implementation and user edits. If code was written first, prove the test's sensitivity against the original revision or a controlled broken variant in a separate temporary copy. Do not delete implementation, reset the checkout, or replay mutations in a shared environment to reconstruct red–green.

## Failure signals and next actions

| Signal | Required response |
| --- | --- |
| New regression test passes on the known-broken code | Check the assertion and the executed code path; no regression proof yet |
| Test mocks the changed decision itself | Exercise the decision through a real boundary; mocks may isolate external I/O |
| Fix makes the happy path pass but ignores rejected input or partial failure | Test the contract's relevant negative path and state after failure |
| Timing/retry change makes a flaky test pass | Establish an observable ordering/condition; do not hide the race with a larger sleep |
| Setup or shared-service access prevents safe red/green | Report the limitation and the best safe alternative; do not claim a reproduced fix |

Before finishing, identify the failing assertion/exit result, the post-fix result, and remaining scope limits in existing task evidence. Do not require a separate log document for a small task.

Read [writing-good-tests.md](writing-good-tests.md) when choosing assertions, mocks or test seams is uncertain. Keep useful tests stable across internal refactoring; do not insist that every helper have its own test.
