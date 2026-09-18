# Codex Workflow Kit

Eight focused development skills for Codex, adapted from Superpowers. Scale process to task risk, preserve project conventions and existing authorization, and verify outcomes with evidence.

**0.1.0-beta is being prepared.** Local installation and evaluation evidence is available in [validation](docs/validation.md). Public release and hosted checks are tracked in [the beta tasks](.doc/specs/public-core/tasks.md). This is an independent project, not an official OpenAI or Superpowers distribution.

## Quick Start

Use a Codex CLI with native plugin commands. The validated local baseline is **Codex CLI 0.153.4 on macOS arm64**. Other versions and platforms require verification; the App UI has not been tested.

From a source checkout or extracted release archive:

```sh
codex --version
codex plugin marketplace add .
codex plugin add codex-workflow-kit@codex-workflow-kit
codex plugin list --marketplace codex-workflow-kit --json
```

Start a new Codex session in your project. Try:

```text
Use $cwk-route to choose the workflow for this task. Follow this project's existing rules.
```

For a simple wording fix, ask directly; a workflow skill is usually unnecessary. For a known bug, try `Use $cwk-tdd to reproduce and fix this defect.` See [first-use examples](docs/getting-started.md) and [troubleshooting](docs/troubleshooting.md).

Once the repository has its first published version, a Git marketplace can be registered with `codex plugin marketplace add 20011229kk/codex-workflow-kit --ref v0.1.0-beta`. The tag must exist; the preparation tree alone does not make it available.

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

[Sources](docs/sources.md) · [Third-party notices](THIRD_PARTY_NOTICES.md) · [License](LICENSE) · [Changelog](CHANGELOG.md) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Publication files](PUBLICATION_MANIFEST.json) · [Release procedure](docs/publication.md)
