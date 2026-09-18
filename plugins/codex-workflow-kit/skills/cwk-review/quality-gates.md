# Review changes to quality gates

Use when the diff changes tests, gate configuration, exceptions, or contains potentially unfinished behavior. Read the relevant baseline and current diff, including new files and the CI/test command that actually runs. A green exit code can result from running fewer checks.

| Change | Evidence to inspect |
| --- | --- |
| Skipped/deleted tests or narrower test discovery | Is the scenario obsolete under the agreed contract, or covered by a replacement that still runs? Preserve distinct parametrized cases. |
| Weaker assertions, snapshots or mocks | Would the original defect or a realistic wrong implementation now pass? Does the assertion still observe the real boundary? |
| Lower thresholds or disabled CI steps | Did the agreed acceptance criterion change, or only the command that enforces it? Check both configuration and invocation. |
| New suppressions or broader exclusions | Identify affected paths/rules and actual risk. A justified narrow type/lint exception differs from silencing security, coverage or secret checks. Never print matched secrets. |
| New exceptions | Check reason, scope, existing authorization, alternative evidence and owner/expiry where the project requires them. Do not invent a mandatory exception system. |
| Stubs, constant success or swallowed errors | Show the reachable path that violates the contract; an interface stub, test double or unrelated TODO is not automatically unfinished production behavior. |

For a suspected bypass, state the changed gate, the behavior no longer proved and the concrete evidence. Fix in-scope problems or report the unmet gate. Deadline pressure and a failing old test do not authorize lowering the bar. Pause only the part requiring a new acceptance decision.

Legitimate changes include removing an exact duplicate, replacing a brittle internal assertion with an equally discriminating public-behavior check, or applying an already-approved narrow exception. Verify the reason and replacement; do not demand another approval for the same scope. Record findings or accepted limitations in the existing task/review evidence, without a second checklist or a full-suite rerun solely for this review.
