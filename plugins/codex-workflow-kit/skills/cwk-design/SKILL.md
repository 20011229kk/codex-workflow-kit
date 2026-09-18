---
name: cwk-design
description: Resolve requirements, significant design alternatives, or architecture decisions before implementation. Skip execution of already-approved or unaffected plan tasks.
---

# Brainstorming Ideas Into Designs

Develop an executable design that preserves the user's goal, project constraints and acceptance criteria. Clear, bounded changes and already-approved designs do not need a new cwk-design cycle.

## Explore and decide

1. Read the relevant project rules, existing spec and affected code. Do not map the entire repository unless the design needs it.
2. Resolve what can be established from existing evidence. Ask only questions whose answers materially change scope, behavior, safety or architecture. Batch related questions when helpful.
3. Compare alternatives only where there is a real choice. Explain the recommendation and tradeoffs without requiring a fixed number of options.
4. Record scope, interfaces, component/data flow, failure handling, constraints and applicable verification. Preserve existing patterns; avoid unrelated refactoring.

## Documentation and review

- First apply the project/global scope and risk classification. For a bounded existing-flow change whose requirements and verification are clear, use a short in-chat design if needed; do not create a spec by default. Only where the project or user has selected Kiro, update `.doc/specs/<feature>/requirements.md` and `design.md`; do not create a parallel design document. Keep User Story, EARS and required design sections.
- Without a project convention, choose an existing relevant document or a concise design artifact only when the task needs one.
- Self-check for missing decisions, contradictory requirements and scope creep.
- When approval is needed for substantive unresolved choices, show one coherent design or written spec and obtain one approval. Do not request approval after every section and again after saving identical content.
- Existing approval remains valid unless the design materially changes. If the user has already authorized the concrete design, continue without another approval.
- Do not commit, push or publish a design unless explicitly authorized.

## Continue to the requested outcome

If the user asked only for design, deliver the design. If implementation is requested, prepare an appropriately sized plan and continue authorized work in the current session by default; use subagents only when explicitly requested. Planning is not a substitute for the requested implementation.

## Visuals

Use diagrams when they clarify a real choice. No companion service is bundled or required; use available authorized tools only when helpful.
