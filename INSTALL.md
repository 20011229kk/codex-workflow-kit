# Install Codex Workflow Kit

This archive contains a complete repository marketplace. Use a compatible Codex CLI; the tested version is recorded in the source repository's compatibility guide.

From the extracted archive directory:

```sh
codex plugin marketplace add .
codex plugin add codex-workflow-kit@codex-workflow-kit
codex plugin list --marketplace codex-workflow-kit --json
```

Start a new Codex session. Try: `Use $cwk-route to choose the appropriate workflow for this task.` An explicit cwk request selects this kit; keep a single workflow provider per task. Installing this plugin does not install optional AGENTS templates or change model settings.

For an updated archive, extract it to a new directory. Remove the old marketplace registration, add the new directory, and reinstall the plugin:

```sh
codex plugin marketplace remove codex-workflow-kit
codex plugin marketplace add .
codex plugin add codex-workflow-kit@codex-workflow-kit
```

Start a new session after updates. To uninstall:

```sh
codex plugin remove codex-workflow-kit@codex-workflow-kit
codex plugin marketplace remove codex-workflow-kit
```

Project rules adopted manually remain under your control. Keep the plugin's LICENSE, THIRD_PARTY_NOTICES.md and licenses/ directory with redistributed copies.

Source, detailed instructions and issue reporting: [20011229kk/codex-workflow-kit](https://github.com/20011229kk/codex-workflow-kit).
