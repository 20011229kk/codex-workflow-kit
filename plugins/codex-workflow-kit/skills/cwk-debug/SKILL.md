---
name: cwk-debug
description: Use for unclear, cross-component, intermittent, or repeatedly failing bugs that need structured root-cause investigation.
---

# Systematic Debugging

Find evidence that discriminates between causes before changing behavior. Choose one debugging workflow for an investigation; do not stack an external alternative with this one. A known local error does not need a full incident process.

## Establish the failure boundary

1. Record the actual error and expected behavior, affected input, relevant version/configuration and whether reproduction is safe. Read the affected source and recent changes.
2. Trace one failing request or state transition across relevant boundaries using logs and correlation IDs. A successful transport response is not proof the business operation succeeded.
3. Separate facts from hypotheses. Compare a working case with the failing case; rank causes by what the observations support, then choose a check whose result would distinguish them.
4. Change one explanatory variable at a time. Record what the result rules out; do not accumulate speculative patches until something passes.

When reproduction is unavailable, continue permitted read-only investigation and label the limit. Shared QA/sandbox mutations, logging switches or deployment need the applicable authorization; never dump environments or credentials as a shortcut.

## Escalate investigation based on evidence

- Trace a failing value back through callers to its first invalid transition.
- For order-dependent failures, inspect observable conditions, shared state and isolation; increasing sleeps does not establish causality.
- If repeated fixes add no discriminating evidence, revisit the last unproven assumption and compare alternatives.
- Validate multiple boundaries only when the same invalid state can actually cross them; do not add unrelated defensive layers.

Repeated failures alone do not prove an architecture defect. Ask only for unresolved decisions affecting scope, business behavior, data or safety; continue independent investigation.

## Fix and verify

- A diagnosis/review request does not authorize a fix or new instrumentation.
- For an authorized fix, first establish a regression check that fails for the original behavior; use test-first for complex/high-risk behavior. Preserve user work and use an isolated comparison if the implementation already changed.
- Fix the identified cause within scope. Check the original symptom, the relevant negative/partial-failure path, and affected integration contracts. Distinguish new failures from unrelated baseline failures.
- For an external/environmental cause, explain the correlation and limitation. Do not add retries, timeout increases or monitoring merely to make the symptom disappear.
- Remove only this task's temporary instrumentation when appropriate. Reuse still-valid evidence and report what remains unverified.

Warning signs of incomplete diagnosis: naming a cause without a falsifiable observation; changing several mechanisms together; asserting a fix from a different input/environment; accepting a passing test that never exercises the defective branch. Resolve the corresponding evidence gap before calling the bug fixed.
