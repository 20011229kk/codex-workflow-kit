# Real Codex Evaluation

These tools run real model sessions and can incur provider costs. They are opt-in and are never invoked by fast CI or plugin installation. Use disposable fixtures only. Running a model evaluates observed behavior; it does not establish general accuracy or a performance advantage.

## Inputs and Isolation

Supply a working Codex CLI, an existing authorized auth JSON file, and a protected **model-only** TOML file. Keep that file outside the repository and include only the selected model, reasoning effort and required provider connection fields. Use double-quoted TOML strings for model metadata. Do not copy a complete user config with plugins, project permissions, MCP services or personal instructions.

Each run creates temporary HOME/CODEX_HOME, installs the actual plugin with native commands and starts fresh sessions. Only necessary process environment settings are inherited. Supervisor-side fixture checks use a separate credential-free temporary HOME/CODEX_HOME, including counterfactual test runs. Model timeouts retain sanitized partial output, exit status 124 and available task snapshots instead of discarding failure evidence. Auth values, provider addresses and machine paths are redacted from retained results; the temporary state is removed when the context exits. Abrupt termination can leave private temporary state requiring cleanup. Inspect evidence before publication even after automated checks.

## Selection Run

```sh
python3 evals/behavior/live.py \
  --cli /path/to/codex \
  --auth-source /path/to/existing/auth.json \
  --model-config /path/to/private-model-only.toml \
  --output /path/to/new-selection-evidence \
  --profile skills-only
```

Use `--profile core` only when evaluating the explicitly adopted core template. Every case runs in a fresh session with the public catalog and request, without the required/allowed selections or rationales. Output contains the exact prepared bundle, requests, raw sanitized events, responses, settings, observations and score. A fresh output directory is required so failures are preserved.

This is real-model **selection** using supplied catalog data, not proof that the host automatically loaded the chosen skills during a task. Native discovery and actual task traces provide separate evidence.

## Actual Tasks

```sh
python3 evals/behavior/tasks.py \
  --cli /path/to/codex \
  --auth-source /path/to/existing/auth.json \
  --model-config /path/to/private-model-only.toml \
  --superpowers /path/to/pinned-superpowers-checkout \
  --output /path/to/new-task-evidence
```

The coexistence case requires the actual upstream v6.3.0 checkout; its plugin is installed into the same temporary state. Use `--case case-id` to rerun affected cases without repeating unaffected work.

Scenarios cover a small edit, regression proof, complex plan execution, authorization continuity, a non-Kiro project, a high-risk patch review, Superpowers coexistence and the independent-review gate after a permission fix. Expected outcomes and fixture checks stay in the supervisor; the actor sees only the request and project files.

The runner records the skill catalog, core-rule digest and supplied upstream revision before execution. Event logs are decoded for redaction and written as ASCII JSONL without changing their meaning. It retains before/after files, task requests, events, final responses and deterministic checks. A repaired function must satisfy external contract probes; regression tests are also run against the original defective implementation. Plan and review cases still require semantic transcript/artifact review. A passing file check alone is not a passing behavior verdict.

Record transcript review separately, including the reviewer identity/role, observations, failures and limits. The implementation supervisor's evidence review is not independent review of this kit's implementation. Preserve failing runs and identify the exact changed inputs before reusing results.
