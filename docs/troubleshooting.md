# Troubleshooting

| Symptom | Check and action |
| --- | --- |
| `codex --version` fails or the binary is missing | Resolve the host installation first. Record the error and use the host's supported installation/update path. |
| `plugin` command is unavailable | Compare your version with the tested compatibility baseline; do not assume older hosts support this distribution. |
| Marketplace not found | Register the checkout/archive root containing .agents/plugins/marketplace.json, not the nested plugin directory. |
| Plugin installed but skills absent | Check `codex plugin list --marketplace codex-workflow-kit --json`, verify it is enabled, and start a new session. |
| Public tag not found | The release may not be published yet. Use a reviewed local checkout or an existing published tag; do not invent a version. |
| Changed local content appears stale | Reinstall from the updated source with a changed version/cache identity, then start a new session. Do not patch the cached copy. |
| Unexpected Superpowers workflow loads | Explicitly choose a cwk skill and inspect project/global provider preferences. Keep one equivalent workflow per task. Distinct names alone do not reconcile conflicting rules. |
| Kiro or core rules seem inactive | They are optional templates. Inspect the project's actual rule file; plugin installation does not merge it. |
| A reference cannot be found | Reinstall the complete plugin. Individual skill copies are unsupported. |
| A build reports an existing output archive | Choose a new output path or inspect/remove your old generated artifact yourself. The builder preserves existing files. |
| A check finds an unlisted or modified file | Review the actual change and update the publication allowlist intentionally; do not blindly accept all discovered files. |

For a report, include kit and host versions, platform, profile, other workflow plugins, the minimal public request and sanitized evidence. Never include credentials, full user configuration or private project logs. Use [the issue template](../.github/ISSUE_TEMPLATE/bug_report.md).
