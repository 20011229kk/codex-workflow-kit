# Evidence Conventions

These files contain public synthetic fixtures and actual Codex observations. They contain no business-project data. Failed selection runs remain alongside later runs; their original input snapshots identify the content evaluated at the time.

- `input.json` and `request.txt` describe what each selection actor received, without answer rubrics.
- `events.jsonl`, responses and task before/after snapshots retain observed events and artifacts. Temporary/source paths are replaced with stable labels such as `<EVAL_ROOT>`, `<CODEX_STATE>` and `<SOURCE_ROOT>`.
- Auth values and provider addresses are excluded or redacted. JSONL whitespace and Unicode escaping are normalized, and trailing whitespace in terminal evidence is trimmed; decoded events and test outcomes are unchanged. Non-ASCII characters generated as test data remain escaped data, while documentation and evaluation instructions use English.
- `score.json` is an offline selection score. Task `run.json` separates deterministic artifact checks from transcript review.
- Transcript review was performed by the implementation supervisor and is not independent code review of this kit. The task actors ran in fresh sessions without the rubric.
- Model metadata records the requested model and effort through the existing configured provider. The underlying provider implementation was not independently attested.

A clean evaluation run is a finite observation, not a universal correctness, routing-accuracy, latency or cost guarantee. Evidence from earlier content is retained as history and must not be silently relabeled as validation of a later version.
