# Codex Workflow Kit

**Codex development workflows that scale to the task: direct edits for small fixes, test-first repairs for bugs, and planning or review when the risk calls for it.**

Eight focused skills adapted from Superpowers. Keep your project's conventions, continue already-authorized work, and tie completion claims to evidence. This is an independent project, not an official OpenAI or Superpowers distribution.

## Install the Beta

With a working Codex CLI that supports native plugins, run this single command:

```sh
codex plugin marketplace add 20011229kk/codex-workflow-kit --ref v0.1.0-beta && codex plugin add codex-workflow-kit@codex-workflow-kit
```

Validated native baseline: **Codex CLI 0.153.4, macOS arm64**. Other host versions/platforms and desktop UI installation remain unverified. [CLI ENOENT or installation trouble?](docs/troubleshooting.md#codex-fails-with-spawn-enoent)

Start a **new Codex session** in your project, then try:

```text
Use $cwk-tdd to reproduce and fix this defect. Follow this project's existing rules.
```

Unsure which workflow fits? Ask `Use $cwk-route to choose the workflow for this task.` For a simple wording fix, ask directly. Installation makes skills available and records the plugin in Codex configuration; it does not merge global/project AGENTS rules. Already using Superpowers? [Choose one provider per task](docs/troubleshooting.md#will-this-change-my-existing-workflow).

## Watch a Real Bug Fix

[![Actual Codex run: failing regression, focused fix, passing tests](https://github.com/20011229kk/codex-workflow-kit/releases/download/v0.1.0-beta/codex-workflow-kit-demo-tdd.gif)](https://github.com/20011229kk/codex-workflow-kit/releases/download/v0.1.0-beta/codex-workflow-kit-demo-tdd.mp4)

[Watch/download the short MP4](https://github.com/20011229kk/codex-workflow-kit/releases/download/v0.1.0-beta/codex-workflow-kit-demo-tdd.mp4) · [Full run and editing disclosure](docs/demo.md) · [First-use examples](docs/getting-started.md)

The video is an edited terminal replay of a real isolated Codex run, with idle time shortened. It demonstrates behavior, not elapsed performance. No speed or token-saving advantage is claimed.

## Help Shape the First Beta

We are looking for **five Codex developers** to try one small, disposable task and report what happened. Successful installs, failures, and workflow conflicts are all useful. [Try the beta and share feedback](docs/beta-trial.md).

Read the development story: [Why two of our first twenty workflow-selection cases failed](docs/articles/two-routing-failures.md). Evidence includes retained failures, later selection runs, and real task artifacts; it is not a universal reliability benchmark.

## Included Workflows

| Skill | Purpose |
| --- | --- |
| cwk-route | Select a relevant workflow when this kit is chosen |
| cwk-design | Resolve meaningful requirements and design alternatives |
| cwk-plan | Build an executable plan in the project's existing task system |
| cwk-execute | Complete an authorized plan and relevant verification |
| cwk-tdd | Establish useful failing tests for behavior defects and complex logic |
| cwk-debug | Investigate unclear or recurring failures using evidence |
| cwk-review | Review actual changes and detect weakened quality gates |
| cwk-verify | Assess completion and integration claims against valid evidence |

Codex may display plugin-qualified names such as `codex-workflow-kit:cwk-plan`. The bundle ships all eight skills and their references together. [Skill scope and upstream names](docs/skills.md).

## Choose Your Rules

Installing the plugin makes skills available; it does **not** install AGENTS rules, change models or enable Kiro. The root [AGENTS.md](AGENTS.md) governs this repository's maintenance.

- **Skills only:** keep your current project rules. This is the installation default.
- **Optional core:** review [AGENTS.core.md](templates/AGENTS.core.md) and merge compatible clauses into your project's rule file.
- **Optional Kiro:** explicitly adopt the [Kiro profile](templates/profiles/kiro.md) if your project wants that spec structure.
- **Optional delegation preference:** adopt [explicit-delegation.md](templates/profiles/explicit-delegation.md) if it matches your policy.

With Superpowers also installed, explicitly select one provider per task. The kit uses distinct names and does not replace upstream files. Names alone do not reconcile contradictory instructions; see [coexistence and compatibility](docs/compatibility.md).

## Update or Remove

For a local checkout, update its source and reinstall with `codex plugin add codex-workflow-kit@codex-workflow-kit`, then start a new session. Use a new version/cache identity when publishing changed plugin content. For Git marketplace updates and rollback, see [adoption](docs/adoption.md).

```sh
codex plugin remove codex-workflow-kit@codex-workflow-kit
codex plugin marketplace remove codex-workflow-kit
```

These commands leave manually adopted project rules under your control. Restore only kit-related clauses after reviewing subsequent local edits.

## Validation and Development

Fast checks require Python 3.9+ and its standard library. They make no model calls:

```sh
python3 scripts/check_public.py
python3 scripts/release.py check
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s evals/routing -p 'test_*.py' -v
python3 evals/routing/routing.py check
python3 scripts/release.py build
```

[Validation](docs/validation.md) separates tool tests, native installation, real selection observations and actual task results. Passing local examples is not a guarantee across users or models. No fixed speed or token reduction is claimed.

## Sources and Maintenance

The skills derive from **Superpowers v6.2.0**, with v6.3.0 reviewed for [current differences](docs/upstream-comparison.md). MIT notices and file provenance are retained; the kit is not a full upstream mirror.

[Sources](docs/sources.md) · [Third-party notices](THIRD_PARTY_NOTICES.md) · [License](LICENSE) · [Changelog](CHANGELOG.md) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Publication files](PUBLICATION_MANIFEST.json) · [Release procedure](docs/publication.md) · [Directory assessment](docs/directory-readiness.md)
