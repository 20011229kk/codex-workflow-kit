# Offline Skill-Selection Evaluation

This suite covers only the eight core skills in this candidate. It is not Codex's host router. Twenty English prompts exercise positive and negative selection, competing lifecycle entries, existing authorization and pressure cases. Structural checks and scorer tests do not establish real model or host behavior.

## Prepare

```sh
python3 evals/routing/routing.py check
python3 -m unittest discover -s evals/routing -p 'test_*.py' -v
routing_run_dir=$(mktemp -d)
python3 evals/routing/routing.py prepare > "$routing_run_dir/input.json"
```

Preparation reads the public catalog and invocation metadata. The default skills-only profile injects no optional rules; --profile core includes the exact core template. The profile is part of the immutable evaluation input. Only case IDs and requests are exported; required/allowed answers and rationales stay in cases.json. No model is invoked, no credentials are read, and no user configuration changes.

Give the evaluator only input.json, without cases.json, tests or scoring code. Selection results cannot demonstrate actual loading behavior, even when the plugin is installed in the evaluation host. For a controlled evaluation, use an independent context per case and record model settings and raw responses. Do not delegate or call paid APIs without applicable authorization.

## Score

Collect a complete observation file in the temporary directory. This example shows only the format; an actual run must include all case IDs:

```json
{"method":"offline-decisions","run_label":"model-and-run-id","decisions":[{"id":"01","selected":[]}]}
```

```sh
python3 evals/routing/routing.py grade --bundle "$routing_run_dir/input.json" --observations "$routing_run_dir/observations.json"
```

Required skills must be selected; skills outside allowed are forbidden. Each one_of group, if present, requires exactly one choice. Missing, duplicate or unknown cases, unknown skills or a changed input snapshot invalidate the run. Exit codes: 0 = all cases match, 1 = selection failures, 2 = invalid input.

Use author-informed for observations made with knowledge of the answers. A label does not prove independence; the reviewer must inspect raw responses. Prepare a new bundle after changing rules or cases. Do not remove meaningful counterexamples or broaden allowed choices merely to improve a score.

Scorer tests establish tool contracts only. Actual model observations and host/task traces are recorded separately in [validation](../../docs/validation.md). No cross-model comparison or speed measurement is claimed. Test fixtures and manually constructed choices must never be presented as model results.
