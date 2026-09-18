# Beta Validation

Validation dates: 2026-09-18 to 2026-09-19. Local environment: macOS arm64, Python 3.9.6, Codex CLI 0.153.4. Publication hashes identify repository content; BUNDLE.json and the archive digest identify distributed runtime content. Task state remains in [tasks.md](../.doc/specs/public-core/tasks.md).

## Fast Tool Checks

- 32 unit tests cover publication inspection, deterministic packaging, exact upstream license retention, resource completeness, namespace/version agreement, output preservation, evaluation privacy/isolation and rejection of an empty unknown-case run, and JSON-escaped secret redaction.
- 20 routing-tool tests cover expectations, exclusive choices, malformed inputs, content/profile identity, answer separation and CLI exit codes.
- All 8 namespaced skill entries and the plugin manifest passed the installed creator validators. The package's own required fast checks use only the standard library.
- The final publication scan checks the reviewed file manifest, digests, local Markdown links and heuristic content findings. It cannot certify legal clearance or absence of every secret.

The packaging and evaluation changes were tested before implementation where applicable. Concrete negative checks demonstrated that an altered upstream license and an unknown task selector were incorrectly accepted before their fixes, then rejected afterward. A JSON-escaped synthetic credential also survived the old raw-text scrub, then was redacted after decoding event values. These tool tests are not model results.

## Native Host Lifecycle

[Final native run](evidence/native-final-2026-09-19.json) passed installation from the built archive, fresh-host discovery of all eight plugin-qualified names, changed-version/resource reinstall, and removal with unrelated skills and project rules preserved. The run also installed actual Superpowers v6.3.0 at b36e0829c6d0140e93cfef2ca599b1b07d4a7797 and verified coexistence through the native catalog.

The validated runtime archive SHA-256 is `69e727f9888ac92a48dff0f9365f8544411965488f0dce59ca5938ea7f3742ea`. Native checks use temporary HOME/CODEX_HOME and make no model calls. Earlier native runs are retained as historical evidence.

## Real Model Selection

Requested model: gpt-6-astra; reasoning effort: high; existing configured provider: openai-custom. The runner used protected temporary auth and model-only configuration. Each request ran in a fresh real Codex session. The backend model implementation was not independently attested.

| Run | Result | Finding and response |
| --- | --- | --- |
| [Initial](evidence/routing-skills-only-2026-09-18/score.json) | 18/20 | cwk-verify overactivated for an existing command and a review-only request. Narrowed its description; kept expectations unchanged. |
| [Second](evidence/routing-skills-only-2026-09-18-r2/score.json) | 19/20 | cwk-design was added while continuing unaffected approved work. Clarified its execution exclusion. |
| [Final catalog](evidence/routing-skills-only-2026-09-19-r3/score.json) | 20/20 | Tested the refinement in a separate candidate, applied identical content, and regraded against the actual current catalog. |

These are selection observations for the skills-only profile, not automatic host-loading accuracy or a statistical reliability claim. Raw requests, events, responses and prepared snapshots are retained. The core profile's content identity is tested in the scorer and its behavior is exercised below; no separate 20-case core selection run is claimed.

## Real Task Outcomes

Eight distinct public scenarios were exercised. [Initial seven-task run](evidence/behavior-2026-09-18/run.json), [affected execution reruns](evidence/behavior-2026-09-19-r2/run.json), and [permission implementation gate](evidence/behavior-review-gate-2026-09-19/run.json) retain exact requests, events, before/after files, deterministic checks and supervisor review notes.

| Scenario | Observed outcome |
| --- | --- |
| Small edit | Only the requested typo changed; no workflow loading or planning/test artifacts. |
| Regression | A real upper-bound assertion failed before the fix, then passed; final tests also rejected the original defective implementation in an isolated counterfactual. |
| Complex plan | Parser and CLI implemented, external behavior probes passed, and the single approved task record completed without another approval cycle. |
| Existing authorization | Unblocked work completed and tests passed while the independent product decision remained pending. |
| Non-Kiro project | Only the existing WORK.md changed; no Kiro structure or implementation was created. |
| High-risk review | Detected the permission bypass and removed denial coverage; reproduced the failing denial assertion and rejected release. |
| Superpowers coexistence | Explicit kit choice loaded cwk-plan without the upstream equivalent; only the existing task record changed. |
| Independent-review gate | Permission fix and tests completed, while release readiness remained blocked for the missing independent review. |

The design-description refinement changed selection guidance, not workflow bodies. The complete selection suite and affected complex-plan/continuation tasks were rerun; unchanged task-body evidence was reused. A few non-Git fixtures produced failed Git status/diff probes; actors continued the authorized work and did not count those commands as successful tests.

Transcript review was performed by the implementation supervisor. It is not independent review of the kit's code, a broad benchmark, or evidence for all prompts and models.

Independent code review subsequently found that supervisor artifact probes inherited the ambient process environment, although the model actors themselves used isolated state. The probes now use a separate, credential-free temporary HOME/CODEX_HOME. [Artifact rechecks](evidence/artifact-replay-2026-09-19.json) replayed all ten stored task outcomes (eight distinct scenarios) through the corrected checks and passed. This is offline artifact verification, not ten additional model runs. Endpoint redaction now handles indented and literal TOML strings, and both model runners preserve sanitized partial evidence on timeout; synthetic regression checks cover these paths.

## Hosted State and Remaining Release Gates

The [repository settings record](evidence/repository-settings-2026-09-19.json) confirms enabled issues, description/topics and private vulnerability reporting. The user-created initial commit is preserved on the local codex/public-beta branch. Fast CI files are prepared; a hosted run, public tag and release are not yet claimed.

The maintainer authorized MIT publication and independent review on 2026-09-19. [Independent review and re-review](evidence/independent-review-2026-09-19.md) passed after correcting three reproduced evaluation-tool findings. Hosted release checks remain pending. Desktop UI installation, other Codex versions, Linux/Windows host installation, cross-model comparisons and performance measurements remain unverified.
