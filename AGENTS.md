# Codex Workflow Kit Maintenance Rules

This file governs maintenance of this repository. It is not the global rule template installed for users; optional user rules live in templates/.

- Preserve the requested scope and existing user changes. Routine documentation work needs no heavy workflow. Record behavior-changing requirements, design and task status in the relevant .doc/specs/ files without duplicate plans.
- Existing authorization persists for the same action and scope. Work inline by default. Delegation, commits, pushes, publication and installation into real user directories require applicable user authorization; this file grants none.
- This is a public candidate tree. Do not add business-system data, personal paths, credentials, runtime state, the original private Git history or unverified third-party material.
- Generic templates defer to users' project conventions. Kiro and execution preferences are optional. Never install into global AGENTS.md or config.toml, or install dependencies, by default.
- Preserve third-party licenses and attribution. Update relevant provenance, PUBLICATION_MANIFEST.json and CHANGELOG.md when included files change.
- Review new scripts and test them with isolated temporary fixtures. Never use real HOME for installation tests. Distinguish structural checks and scorer tests from actual model behavior.
- Before delivery run python3 scripts/check_public.py, python3 scripts/release.py check, python3 -m unittest discover -s tests -v, and python3 -m unittest discover -s evals/routing -p 'test_*.py' -v. Reuse unchanged evidence; do not claim untested host routing or platform installation passed.
- Use English throughout the candidate, including README.md, specs, rule templates, evaluation requests and test fixtures.
- .doc/specs/public-core/tasks.md is the sole publication-preparation status record. Publication criteria and validation reports are supporting references, not additional completion ledgers.
