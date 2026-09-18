# Security

The runtime plugin contains instructions and references, with no credential collection, connector, hook or telemetry. Installation uses native Codex plugin management. Optional project rule adoption is a separate user-reviewed action.

The development-only live evaluation tools can use an explicitly supplied auth file and model-only configuration. They copy these into protected temporary state, exclude them from public results and remove the temporary directory when the run exits normally or raises an exception. Never place credentials in the repository, command text, issue reports or published artifacts. Abrupt process termination can leave temporary files; inspect and remove that run's private temporary state before sharing machine diagnostics.

The content checker is heuristic and cannot certify that a tree is secret-free or legally cleared. Release artifacts use a separate explicit runtime allowlist.

## Reporting

The intended private route is [GitHub private vulnerability reporting](https://github.com/20011229kk/codex-workflow-kit/security/advisories/new). Private vulnerability reporting was enabled and confirmed through the repository API on 2026-09-19. If the route becomes unavailable, contact the maintainer privately before disclosing details. Never post exploit details, private configuration or customer data in a public issue.

Supported release scope is recorded in docs/compatibility.md. This beta does not promise a fixed response SLA or support for untested hosts.
