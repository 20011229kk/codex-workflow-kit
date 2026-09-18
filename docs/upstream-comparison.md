# Comparison with Superpowers v6.3.0

Comparison baseline: [Superpowers v6.3.0](https://github.com/obra/superpowers/releases/tag/v6.3.0), commit b36e0829c6d0140e93cfef2ca599b1b07d4a7797. The kit's included source lineage remains v6.2.0 plus local adaptations; this review does not relabel those files as a v6.3.0 fork.

The v6.3.0 release notes already describe task-scaled brainstorming, reduced subagent dispatch overhead, continuation through some plan conflicts and rereading existing test evidence instead of rerunning the suite. Those ideas are not unique advantages of this kit. Upstream has broader host integration, more workflow entries and a real-session evaluation system.

The kit intentionally focuses on Codex, eight independently named entries, optional project rule fragments, existing authorization and task-state continuity, inline execution by default, and explicit verification limits. These are design choices; they do not establish superiority in speed, cost or correctness.

| Area | Kit policy |
| --- | --- |
| Planning strength | Scale to scope and risk; preserve the project's existing records |
| Execution mode | Current session by default; delegation follows user authorization |
| Documentation | Kiro is optional; one authoritative task-state source when adopted |
| Tests | Meaningful behavior regression evidence; suitable checks for prose/configuration |
| Review | Inspect actual changes and weakened quality gates; preserve independent review requirements |
| Distribution | Native Codex plugin with a cwk namespace; no upstream file replacement |
| Validation claims | Separate tool tests, host lifecycle checks, selection observations and actual tasks |

The kit omits upstream worktree/branch-finishing automation, subagent orchestration, companion servers and other-host adapters. These omissions define first-release scope and must not be presented as equivalent feature coverage.

Upstream [testing documentation](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/docs/testing.md) distinguishes plugin code tests from live model sessions and notes that the latter are not all part of CI. This kit follows the same evidence distinction. A fair performance comparison would require matched tasks, host/model settings, repetitions and quality criteria; none is claimed here.
