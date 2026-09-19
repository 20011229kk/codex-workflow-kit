# A Real Test-First Bug Fix

[Watch/download the 48-second MP4](https://github.com/20011229kk/codex-workflow-kit/releases/download/v0.1.0-beta/codex-workflow-kit-demo-tdd.mp4) · [Animated preview](https://github.com/20011229kk/codex-workflow-kit/releases/download/v0.1.0-beta/codex-workflow-kit-demo-tdd.gif) · [Media checksums](https://github.com/20011229kk/codex-workflow-kit/releases/download/v0.1.0-beta/codex-workflow-kit-demo-tdd.sha256)

## What You Are Watching

An **edited terminal replay**, not a screen recording: selected commands, outputs and file changes from a real isolated Codex run are typeset into six eight-second scenes. Waiting, skill/rule reads and an unsuccessful Git status probe are omitted from the video but retained in the raw events. The before/after code diff is reconstructed from saved files. No commands or outcomes were invented. There is no audio track.

The measured runner interval was **67.65 seconds**, including task execution and supervisor artifact checks, excluding initial plugin/fixture setup. The 48-second playback is editorial timing and must not be used as a latency benchmark or a comparison against another workflow. One small public fixture is not representative of all projects.

## Observed Sequence

1. The user explicitly requested `$cwk-tdd` to fix the upper bound of `clamp(value, low, high)`, with integer inputs and `low <= high`.
2. Codex loaded the installed kit skill and the disposable project's optional core rules.
3. Codex added regression and edge cases before changing `clamp.py`. `python3 -m unittest -v` exited 1: `12 != 10`, plus two related upper-bound failures.
4. Codex changed `return max(low, value)` to `return min(high, max(low, value))`.
5. The same command exited 0 with all six test methods passing. Only `clamp.py` and `test_clamp.py` changed.
6. Supervisor checks confirmed the integer boundary contract and replayed the final tests against the original implementation in a separate disposable copy; they failed again for the defect.

The fixture had no Git repository, so an exploratory `git status` exited 128. That is retained as a failed probe, not counted as a successful test or hidden from the evidence. Transcript inspection here is supervisor review, not independent code review of the kit.

## Exact Evidence

- [Request](evidence/demo-tdd-2026-09-19/regression/request.txt)
- [Original events](evidence/demo-tdd-2026-09-19/regression/events.jsonl): item_5 adds tests, item_6 is red, item_8 changes the implementation, item_9 is green.
- [Before](evidence/demo-tdd-2026-09-19/regression/before.json) and [after](evidence/demo-tdd-2026-09-19/regression/after.json) files
- [Final test replay](evidence/demo-tdd-2026-09-19/regression/tests.txt) and [original-code counterfactual](evidence/demo-tdd-2026-09-19/regression/counterfactual.txt)
- [Run metadata and supervisor review](evidence/demo-tdd-2026-09-19/run.json)
- [Scene text and source mapping](evidence/demo-tdd-2026-09-19/storyboard.json)
- [Media validation and hashes](evidence/demo-tdd-2026-09-19/media.json)

Temporary paths and provider/auth values are sanitized; the outcomes are unchanged. Media was rendered with locally available Pillow and native macOS AVFoundation. These are authoring tools, not plugin dependencies. Binary media is attached to the release separately from the unchanged runtime ZIP.

## Environment and Reproduction

Recorded 2026-09-19 on macOS arm64 using Codex CLI 0.153.4. Requested model `gpt-6-astra`, high reasoning effort, through the existing configured provider; the backend implementation was not independently attested. The kit runtime matches v0.1.0-beta. Temporary HOME/CODEX_HOME and a disposable project were used; no business service or real project was involved. Normal model usage costs apply.

To try the behavior, use the [trial guide](beta-trial.md). For a maintainer reproduction, use the reviewed runner in [evals/behavior](../evals/behavior/README.md), selecting `--case regression` with a fresh evidence directory and protected auth/model-only configuration. Do not publish those input configuration files. Results and timings can vary between runs.
