# Publication and Runtime File Scope

[PUBLICATION_MANIFEST.json](../PUBLICATION_MANIFEST.json) is the reviewed repository file allowlist with hashes. It excludes its own digest. The runtime archive uses the narrower, explicit bundle contract in scripts/release.py and records packaged hashes in BUNDLE.json.

| Path | Purpose |
| --- | --- |
| .agents/plugins/marketplace.json | Repository marketplace for native installation |
| plugins/codex-workflow-kit/ | Versioned manifest, eight cwk skills, references and retained licenses |
| templates/ | Optional project rules, core, Kiro and delegation preferences |
| scripts/ and tests/ | Read-only inspections, deterministic packaging, native smoke test and offline contracts |
| evals/ | Answer-separated routing and disposable real-task evaluation tools |
| docs/evidence/ | Public toy-task observations and sanitized run evidence; failed observations remain visible |
| docs/ | Adoption, support, validation, provenance, comparison and release guidance |
| .github/ | Fast CI and issue/PR templates; no automatic paid model runs |
| .doc/specs/public-core/ | Requirements, design and the sole beta task-state record |
| Root documentation and VERSION | Onboarding, maintenance, security, license and version identity |

Generated archives under dist/, caches, credentials, complete user configuration, original private Git history, business skills, internal logs, branding assets and personal runtime state are excluded. Model evidence is limited to public synthetic fixtures; authentication and provider endpoints are never included.

The original personal synchronization engine remains excluded. Native host plugin management provides installation and removal. Source-file fingerprints identify original inputs; publication and archive fingerprints identify delivered content.
