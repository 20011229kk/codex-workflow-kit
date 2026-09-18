# Compatibility and Coexistence

## Validated Baseline

Native installation, new-host discovery, changed-version/resource installation and uninstall were exercised with **Codex CLI 0.153.4 on macOS arm64**, using temporary HOME/CODEX_HOME. The lifecycle also passed with the real Superpowers v6.3.0 plugin installed. See [evidence](validation.md) for exact bundle fingerprints and model-run limits.

This is one tested configuration, not a minimum-version claim. The desktop app's plugin UI, other Codex versions, Linux and Windows have not been exercised end to end. Fast Python checks in CI are distinct from host installation support.

## Provider Selection

All kit directories and skill names use the cwk namespace. The host also prefixes plugin skills, such as `codex-workflow-kit:cwk-plan`. The kit never overwrites upstream Superpowers files.

Two workflow providers can still cover similar tasks. For a kit task, explicitly request a cwk skill or adopt a compatible project preference choosing Codex Workflow Kit. For an upstream task, choose Superpowers. When project instructions explicitly choose another provider, follow them; resolve contradictions before adopting a second rule set.

Native lifecycle checks establish distinct discovered names and preserved unrelated content. They do not prove that every implicit prompt selects the desired provider. Real coexistence task observations are listed separately in the validation report.

## Rule Profiles

| Profile | What is active |
| --- | --- |
| skills-only | Installed skill catalog plus the user's existing host and project rules; no core template is injected by installation |
| core | The same plugin plus explicitly adopted templates/AGENTS.core.md clauses |
| core with Kiro | Core plus the explicitly selected Kiro fragment, where compatible with project conventions |

The public routing tool defaults to skills-only and supports an explicit core profile. It never silently enables Kiro. Behavior fixtures state their actual profile and may carry their own project conventions.

## Dependencies and Boundaries

Fast tooling requires Python 3.9+ standard library. Model evaluations additionally require a working Codex CLI, authorized access to a model and a protected model-only configuration. They are not run by CI or by installation.

The package configures no model, reasoning level, production dependency, connector, hook or telemetry service. Optional project rules remain owned by the user. The complete eight-skill bundle is the supported distribution; individual folder copies can break cross-skill references.
