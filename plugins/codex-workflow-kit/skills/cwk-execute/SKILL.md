---
name: cwk-execute
description: Use when executing a written implementation plan in the current session, the default unless the user explicitly requests subagents.
---

# Executing Plans

Execute the authorized scope in the current session through completion. This is the default mode; no separate execution-mode confirmation is needed. Delegate only when the user explicitly requests subagents, preserving the authorized scope.

## Prepare

Read the plan and applicable project rules, reuse existing decisions, and check the working tree so user changes are preserved. Use an isolated worktree only when needed or requested; do not require one for every plan. Where the project or user has selected Kiro, `tasks.md` is the only persistent completion checklist.

## Execute

For each deliverable, implement the scoped change, run the relevant verification, fix failures caused by that change, and update its status and evidence. Adapt ordinary implementation details to real code while preserving required behavior. Update the design when implementation changes it materially.

## Failure and decision boundaries

- A failing test is evidence to investigate, not an automatic reason to stop. Distinguish new failures from pre-existing or unrelated ones. If a pre-existing failure blocks an explicitly required acceptance gate and repair is authorized and in scope, fix it; otherwise report the gate as blocked, not passed.
- Inspect missing development tooling and use an existing supported environment where possible. Do not silently install new production dependencies or change global configuration.
- Resolve routine ambiguity from the repository and conversation. Ask only when the missing decision affects business behavior, data, security, interfaces or authorized scope.
- If investigation stops making progress, report the evidence and exact missing input. Continue work that does not depend on that input.
- Do not bypass permissions, alter production/shared environment settings or broaden the task to make a check pass.

## Completion

Finish implementation, applicable checks, in-scope fixes and required spec updates; report what changed, the evidence and any remaining limits. Reuse still-valid check results instead of repeating them merely at a workflow boundary.

Handle branch integration only when requested or when a genuine integration decision is necessary, using the project's existing workflow. An implementation task may be complete with reviewed uncommitted changes; do not default to a commit, push, merge or release.
