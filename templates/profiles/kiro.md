# Optional Kiro Documentation Profile

Adopt this fragment only when explicitly selected and compatible with project conventions. Selecting the core template does not automatically enable Kiro.

- For a bounded, reversible, low-risk change with clear requirements and verification, use existing records or a brief conversation note instead of mechanically creating three documents.
- When a full specification is needed for a subsystem, architecture decision, cross-module protocol, permissions, data migration or concurrency boundary, use .doc/specs/<feature>/requirements.md, design.md and tasks.md.
- Requirements contain a User Story and EARS acceptance criteria. Design covers Overview, Architecture, applicable sequence diagrams, component/data/workflow design, constraints/tradeoffs and testing strategy. Tasks is the only executable completion checklist.
- Update affected entries in an existing spec; do not create parallel Superpowers design or plan files. Read-only reviews, reports and wording edits do not need a new spec just to store output.
- Make requirements, design and tasks executable before implementation. Do not reapprove unchanged decisions merely because they were written into documents. Update material design deviations and record status and valid evidence in tasks.
