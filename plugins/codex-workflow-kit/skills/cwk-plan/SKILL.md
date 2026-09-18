---
name: cwk-plan
description: Use when a substantial implementation task needs an executable plan grounded in requirements and project constraints.
---

# Writing Plans

Create a plan that another engineer can execute without duplicating the entire implementation in prose.

## Source of truth

Read relevant rules and determine whether the task actually needs a written plan. For a bounded existing-flow change permitted by project/global rules, a concise in-chat scope and verification statement is enough; do not create Kiro files just because this skill was considered. Only when the project or user selects Kiro, use its `tasks.md` as the only persistent checklist, linking requirements/design. Preserve stricter project conventions and update existing affected spec entries.

## Plan content

- State the outcome, boundaries, dependencies and non-negotiable project constraints.
- Group tasks into meaningful, testable deliverables. Do not force every step into a 2–5 minute unit or a separate review/commit.
- For each task, identify relevant files, interface or data changes, acceptance criteria, and concrete verification commands or observations.
- Include code snippets only where they settle a non-obvious interface or fragile operation. Full implementation and test code are not required in a plan.
- Specify regression-first checks for behavior bugs and test-first checks for complex logic, permission, data-integrity, concurrency and compatibility changes. Identify independent review for high-risk boundaries before integration. Use appropriate schema/scenario checks for documentation or declarative configuration instead of artificial unit tests.
- Include commit, push, deployment or dependency changes only where explicitly authorized. Do not make an unrequested commit a prerequisite for the next task.
- Self-check requirement coverage, dependency order, consistent interfaces and executable verification. Resolve routine gaps locally; surface critical unresolved decisions.

## Execution — default to the current session

If the user requested only a plan, deliver it and stop at that requested boundary.

If implementation is requested, execute the authorized plan in the current session by default. Do not pause to ask for an execution-mode choice or permission already granted.

- Use `cwk-execute` for inline execution.
- Only when the user explicitly requests subagents, use available authorized delegation tools for bounded tasks and reviews. This core package does not bundle a subagent orchestration skill; its absence does not block inline work.
- Preserve an explicit choice across workflow steps; tool availability does not authorize delegation.

Continue through implementation, applicable verification, fixes and spec updates. Ask only for a material unresolved decision or permission, continuing independent authorized work while it is pending.
