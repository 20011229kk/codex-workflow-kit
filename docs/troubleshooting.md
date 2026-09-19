# Troubleshooting

| Symptom | Check and action |
| --- | --- |
| `codex --version` fails or the binary is missing | Resolve the host installation first. Record the error and use the host's supported installation/update path. |
| `plugin` command is unavailable | Compare your version with the tested compatibility baseline; do not assume older hosts support this distribution. |
| Marketplace not found | Register the checkout/archive root containing .agents/plugins/marketplace.json, not the nested plugin directory. |
| Plugin installed but skills absent | Check `codex plugin list --marketplace codex-workflow-kit --json`, verify it is enabled, and start a new session. |
| Public tag not found | Verify the exact published tag and network access. The current beta tag is v0.1.0-beta; do not guess a version. |
| Changed local content appears stale | Reinstall from the updated source with a changed version/cache identity, then start a new session. Do not patch the cached copy. |
| Unexpected Superpowers workflow loads | Explicitly choose a cwk skill and inspect project/global provider preferences. Keep one equivalent workflow per task. Distinct names alone do not reconcile conflicting rules. |
| Kiro or core rules seem inactive | They are optional templates. Inspect the project's actual rule file; plugin installation does not merge it. |
| A reference cannot be found | Reinstall the complete plugin. Individual skill copies are unsupported. |
| A build reports an existing output archive | Choose a new output path or inspect/remove your old generated artifact yourself. The builder preserves existing files. |
| A check finds an unlisted or modified file | Review the actual change and update the publication allowlist intentionally; do not blindly accept all discovered files. |

For a report, include kit and host versions, platform, profile, other workflow plugins, the minimal public request and sanitized evidence. Never include credentials, full user configuration or private project logs. Use [the issue template](../.github/ISSUE_TEMPLATE/bug_report.md).

## Codex Fails with Spawn ENOENT

If `codex --version` itself reports `spawn .../vendor/.../codex ENOENT`, the launcher could not start its native executable. The plugin command has not run yet. This was observed with an incomplete npm Codex 0.111.0 installation on macOS arm64; the error alone does not establish why a different installation is broken.

Check which launcher is selected:

```sh
command -v codex
codex --version
```

Repair/update that installation through its supported distribution, then verify `codex --version` and `codex plugin --help`. Avoid deleting configuration or plugin caches as a first response to a missing executable.

On a Mac where this application-bundled binary **already exists**, the following alternative was validated with version 0.153.4:

```sh
"/Applications/ChatGPT.app/Contents/Resources/codex" --version
"/Applications/ChatGPT.app/Contents/Resources/codex" plugin marketplace add 20011229kk/codex-workflow-kit --ref v0.1.0-beta && \
"/Applications/ChatGPT.app/Contents/Resources/codex" plugin add codex-workflow-kit@codex-workflow-kit
```

That path is installation-specific, not a universal macOS or Windows/Linux path. Using it does not repair the broken `codex` entry on PATH. The documented command installs through the CLI; it is not evidence that desktop UI installation was tested.

## Will This Change My Existing Workflow?

The native installer registers/enables this plugin in Codex configuration. The kit has eight namespaced skills and references; it ships no hooks, MCP server or app connector. It does not overwrite existing Superpowers files, select a different model, or automatically merge the optional AGENTS templates.

Skills becoming available can still change workflow selection. Some descriptions address general design, planning, testing and review tasks. The route skill's selection condition does **not** hard-gate every other skill. Distinct names prevent name collisions, not competing instructions.

For a cautious trial, keep existing rules and explicitly choose a kit skill for one task. If you want to keep your current provider as the default, review and add a compatible project rule such as:

```text
Default to our existing workflow. Use Codex Workflow Kit only when explicitly
selected. Do not stack equivalent Codex Workflow Kit and Superpowers workflows.
```

This is a model instruction, not a technical loader restriction. If behavior is still unsuitable, remove the plugin and start a fresh session:

```sh
codex plugin remove codex-workflow-kit@codex-workflow-kit
codex plugin marketplace remove codex-workflow-kit
```

Any AGENTS clauses you manually adopted remain yours to review and remove. Report competing provider choices with a minimal public example; do not upload full personal configuration.
