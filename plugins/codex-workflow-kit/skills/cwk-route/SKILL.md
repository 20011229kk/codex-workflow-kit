---
name: cwk-route
description: Select the appropriate Codex Workflow Kit skill when the user or project chooses this kit for a development task.
---

# Select a Codex Workflow Kit Workflow

Select the workflow that materially helps the requested task. An explicit cwk request selects this kit for that task; do not also load an equivalent Superpowers workflow. If the project chooses another provider, respect that choice. Distinct names prevent name collisions but do not resolve contradictory project policies by themselves. Read project rules and relevant source evidence first when needed to choose correctly.

- Directly handle questions, read-only inspection, existing commands, wording edits and small scoped fixes; they do not require a process skill merely because a skill exists.
- Use cwk-design for unresolved requirements or significant design choices, cwk-plan for substantial implementation planning, and one debugging workflow for a difficult failure.
- Do not stack competing planning, debugging or TDD workflows. Domain-specific business constraints remain authoritative.
- Within this kit, use `cwk-tdd` for test-first work. Honor an explicitly selected external workflow without stacking another TDD or planning process.
- Reuse decisions and approvals already established for this task. Do not create a second checklist or plan where project rules specify one source of truth.
- Execute inline by default without an execution-mode question. Delegate only when the user explicitly requests subagents; preserve that choice and its scope across workflow steps.
- Continue authorized work through its agreed completion criteria. Pause only the portion requiring a new decision or permission.

## Project and host compatibility

Follow the project's existing spec and task convention. Kiro applies only if the project or user selected it. This kit does not choose a model, permission mode or reasoning level.

Use only tools exposed by the host. Additional skills or delegation tooling are optional external capabilities, not bundled prerequisites. A bounded subagent assignment should not restart workflow selection. User and project instructions override generic skill defaults.
