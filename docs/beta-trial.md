# First Five Codex Trials

We are recruiting five developers who already use Codex to try the beta on one disposable task. You do not need to star the repository, promote it, provide an email address, or share private code. We want to understand installation failures and workflow friction as much as successful runs.

## A Small Trial

1. Record your Codex CLI version and operating system. Read the [support boundaries](compatibility.md) and [coexistence FAQ](troubleshooting.md#will-this-change-my-existing-workflow).
2. Follow the [pinned installation command](../README.md#install-the-beta), keeping your existing project rules. Start a fresh Codex session.
3. In a disposable project, choose one small bug you understand. For a public example, start with `def clamp(value, low, high): return max(low, value)` and ask `$cwk-tdd` to fix the upper bound while retaining lower-bound behavior. Use synthetic data and no external services. Your normal Codex usage charges or limits may apply.
4. Observe whether it adds a meaningful regression, sees it fail for the defect, fixes the implementation, and runs the relevant tests. Note unnecessary questions, irrelevant skills or conflicts with existing providers.
5. [Submit a trial report](https://github.com/20011229kk/codex-workflow-kit/issues/new?template=beta_trial.yml). Incomplete or unsuccessful attempts are welcome. Include only short, sanitized evidence you are comfortable making public.

Prefer another task? A small wording correction should not need a design/TDD workflow. A plan already approved in your project's task file should continue without asking for the same approval again. These are useful boundaries to test too.

## What Counts as a Trial?

A volunteer or star is not a completed trial. A useful report identifies the environment, task, observed outcome and friction; a failed installation can itself be a useful trial outcome. Reports are self-reported unless independently reproduced. The maintainer records the five-person target in the existing [task record](../.doc/specs/public-core/tasks.md), without inventing participants or treating the invitation as adoption.

Please do not post access tokens, full configurations, organization names, proprietary patches or customer logs. Use the private reporting path in [SECURITY.md](../SECURITY.md) for a suspected vulnerability. Removal instructions are in the [README](../README.md#update-or-remove).
