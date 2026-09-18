---
name: cwk-review
description: Use for substantial code changes, security/data/concurrency/interface risk, project-required reviews, or explicit code-review requests.
---

# Requesting Code Review

Check the actual change against the request and realistic counterexamples. Review is not a replay of the implementer's explanation.

## Choose the review depth

- A small, bounded change can be reviewed inline against its contract and affected tests.
- Security/permission boundaries, persistent-data changes, concurrency control and cross-module protocol changes require an independent reviewer before integration readiness is claimed. A fresh authorized agent or human who did not implement the change can provide that review.
- Delegation still requires the user's permission. If it is not authorized, ask once for that review or identify pending human review while continuing independent implementation/verification. Do not silently substitute self-review. An explicit project-permitted waiver is a recorded exception, not a passed independent review.
- For other substantial changes, perform a focused adversarial pass; do not invent an independent review merely by changing the same agent's role label.

## Review inputs and method

- Provide the request, relevant project/spec constraints, actual staged/unstaged/new-file diff and verification evidence. Use committed ranges only when they contain the actual change.
- Give the reviewer enough context to reason independently. Do not supply the implementer's conclusion as the expected verdict.
- Use [code-reviewer.md](code-reviewer.md). Inspect relevant callers/configuration when needed to establish a concrete risk; a diff-only restriction must not hide a cross-component defect.
- Probe the assumptions that could make the passing tests misleading: rejected inputs, caller permissions, interrupted operations, retry/replay, concurrent changes and compatibility as applicable. These are risk prompts, not a mandatory list for every typo.
- When tests, check configuration, exceptions or unfinished implementation change, use [quality-gates.md](quality-gates.md) to distinguish a legitimate replacement from making the gate easier to pass. Inspect the actual diff and coverage evidence, not just the green summary.
- Fix confirmed in-scope important findings, verify the fix, and re-review the affected risk. Preserve unrelated findings as evidence without expanding the task.

Report what was inspected, what remains uncertain and whether review was independent. A "no findings" result is not proof of correctness. Reuse still-valid review evidence; neither review nor a readiness verdict grants commit/push/deploy permission.
