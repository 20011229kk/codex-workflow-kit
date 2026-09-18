# Core Skills and Provenance Names

The complete plugin contains eight skills. Codex may display a plugin prefix, for example `codex-workflow-kit:cwk-plan`. Each skill retains its upstream provenance while using an independent public name.

| Public skill | Upstream entry | Intended use |
| --- | --- | --- |
| cwk-route | using-superpowers | Select this kit's relevant workflow when it is chosen |
| cwk-design | brainstorming | Resolve requirements or significant design alternatives |
| cwk-plan | writing-plans | Produce an executable plan using project conventions |
| cwk-execute | executing-plans | Execute and verify an authorized plan |
| cwk-tdd | test-driven-development | Regression-first or complex test-first work |
| cwk-debug | systematic-debugging | Investigate unclear, recurring or cross-component failures |
| cwk-review | requesting-code-review | Review actual changes, counterexamples and quality gates |
| cwk-verify | verification-before-completion | Assess completion or integration evidence |

The mapping is also recorded in [skill-names.json](skill-names.json). Supporting resources cover test quality, review structure and quality-gate changes. All eight entries ship together so relative references remain valid.

This is not a mandatory sequence for every task. Routine questions, existing commands and small wording edits can need no skill. Explicit user/project workflow choices take precedence. Kiro, external orchestration tools, multimedia skills and business-specific extensions are not prerequisites.
