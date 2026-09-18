# Public Beta Requirements

## User Story

As a Codex user unfamiliar with the maintainer's personal setup, I want to install, verify, update and remove a versioned workflow plugin without replacing my project conventions or other skills.

## EARS Acceptance Criteria

- When installing version 0.1.0-beta, the documented Codex CLI path shall load the complete eight-skill plugin in a fresh session on an explicitly tested operating system and CLI version.
- When Superpowers is present, distinct cwk-prefixed skill names and a documented single-provider choice shall prevent name collisions and unintended stacking in the tested coexistence scenarios; installation shall not edit or remove Superpowers.
- When a user installs only the plugin, it shall not silently install AGENTS rules. Optional core and Kiro profiles shall be documented separately, and evaluation bundles shall declare and reproduce their selected profile.
- When updating or uninstalling the plugin, the documented native host commands shall change only the selected plugin; local project rules and unrelated plugins shall remain intact in isolated lifecycle tests.
- When packaging a release, all referenced skill resources and applicable licenses shall be included; the archive shall be deterministic and identify its version and content fingerprints.
- When evaluating behavior, real Codex sessions shall cover the 20 selection requests and representative typo, regression, complex-plan, authorization, non-Kiro, high-risk review and coexistence scenarios. Raw observations, settings, checks and failures shall be retained without credentials or personal paths. Tool tests shall not be counted as model results.
- When documenting support, README shall provide a reproducible quick start, first task, validation, update, removal and troubleshooting path, with tested and untested surfaces distinguished.
- When preparing GitHub delivery, the tree shall include fast CI, issue/PR templates, release instructions, attribution, and a private security-reporting route once the actual repository is provided. Rights and license decisions shall be confirmed by the maintainer rather than inferred by the agent.
- When comparing upstream, documentation shall identify the retained v6.2.0 provenance and reviewed v6.3.0 changes without claiming unmeasured performance superiority.
- All included documentation, rules, prompts and fixtures shall use English. Tests shall use isolated HOME and Codex state; the existing personal workflow and real global configuration shall remain unchanged.
- Public repository creation remains with the user. Remote configuration and publication shall use the provided repository and applicable authorization; pending external decisions remain explicit in tasks.md.
