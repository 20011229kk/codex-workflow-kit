# Independent Release Review

Date: 2026-09-19. Reviewer: release_security_review, a fresh authorized agent that did not implement the changes. This summary was recorded by the implementation supervisor from the reviewer's reports.

## Scope and Original Findings

The reviewer inspected the actual staged/worktree changes, callers, tests, CI and recorded validation against the beta requirements. The focus covered evaluation credential handling and isolation, bundle safety and native lifecycle boundaries.

1. P1: supervisor fixture probes inherited ambient HOME, CODEX_HOME and credential environment variables.
2. P2: provider URL redaction missed valid indented or literal TOML strings.
3. P2: model timeouts discarded partial events and failure metadata.

All findings were independently reproduced with synthetic data. No real credentials, model services or real user settings were accessed.

## Remediation and Independent Re-review

The implementation now passes an isolated environment to every fixture probe and counterfactual test, using a separate credential-free checks directory. URL redaction accepts indented/basic/literal/quoted-key inputs. Both runners retain sanitized timeout streams and failed metadata; task runs retain available final output and artifacts.

The reviewer independently repeated the original counterexamples, all nine privacy tests, partial-output retention checks and the whitespace check. All passed. No remaining confirmed blocker was found in the reviewed scope. The initial independent pass also ran twelve packaging tests and found no confirmed bundle or native-smoke script blocker.

Reviewed code SHA-256:

| File | SHA-256 |
| --- | --- |
| evals/behavior/live.py | 7c54e0d3cd1d4590dff9377f1eeda3a93f0bf754c9829870eb64c33971206acd |
| evals/behavior/tasks.py | 282699baad096f8fb52f1ef53d15e55eec3af888bf352c3e990be58aaa78c6df |
| tests/test_live.py | 3bb2632c6d3dbeedf8ee653d0fb530a9e8d8f9d39be6f0831433382e274d4c44 |

## Limits

The reviewer did not rerun model sessions or native installation; unchanged lifecycle evidence was inspected. This is scoped independent review, not a guarantee for arbitrary TOML, model behavior or host environments. Hosted checks and public release completion remain separately evidenced.
