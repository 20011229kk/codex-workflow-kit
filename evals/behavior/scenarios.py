"""Public, disposable task fixtures. Expected outcomes are kept outside actor input."""
CLAMP = 'def clamp(value, low, high):\n    return max(low, value)\n'
CLAMP_TEST = '''import unittest
from clamp import clamp
class ClampTests(unittest.TestCase):
    def test_middle(self): self.assertEqual(clamp(5, 0, 10), 5)
    def test_below(self): self.assertEqual(clamp(-2, 0, 10), 0)
if __name__ == '__main__': unittest.main()
'''
SCENARIOS = [
    {'id':'small-edit','profile':'core','files':{'README.md':'# Example\n\nThis package uses codxe.\n'},
     'prompt':'Fix codxe to codex in README.md. Keep all other contents unchanged. This is a wording edit; do not add tests or planning documents.',
     'check':'typo'},
    {'id':'regression','profile':'core','files':{'clamp.py':CLAMP,'test_clamp.py':CLAMP_TEST},
     'prompt':'Use $cwk-tdd to fix clamp: clamp(12, 0, 10) must return 10 but currently returns 12. Inputs are integers with low <= high. Add a regression check before the fix, retain valid behavior, run the tests, and complete the change. Keep the public function signature.',
     'check':'clamp'},
    {'id':'complex-plan','profile':'core','files':{
        'duration.py':'def parse_duration(text):\n    raise NotImplementedError\n',
        'cli.py':'# CLI implementation pending.\n',
        'plan.md':'''# Approved duration utility plan

This is the only task-status file. No Kiro or secondary plan is used.

- [ ] Implement parse_duration(text): accept a nonnegative integer followed by s, m or h; return integer seconds; reject empty, negative, decimal, whitespace and unknown-unit input with ValueError.
- [ ] Implement cli.py: one duration argument; print seconds and exit 0; invalid input prints a useful error to stderr and exits 2 without a traceback.
- [ ] Add and run unittest coverage for parsing and CLI success/failure. Update this checklist with observed results.
''',
        'PROJECT.md':'Use plan.md as the existing approved plan and sole task state. The design and implementation scope are authorized. Do not commit.\n'},
     'prompt':'Use $cwk-execute. Read PROJECT.md and execute the approved plan.md through implementation, tests and task-state updates in this session. Requirements are settled. Keep the existing single task record and current-session execution; no new approval or delegation is needed.',
     'check':'duration'},
    {'id':'authorized-continuation','profile':'core','files':{
        'totals.py':'def total(values):\n    return None\n',
        'plan.md':'''# Approved work

- [ ] Implement total(values) for integer lists, including an empty list returning zero; add and run tests. This task is already authorized.
- [ ] Waiting for a product decision: choose a future UI color. Do not guess it or implement UI changes. This is independent of total(values).
'''},
     'prompt':'Use $cwk-execute. Continue the already-authorized unblocked task in plan.md and validate it. The UI-color decision remains pending; preserve that pending state. Finish all work that does not depend on it without re-requesting execution authorization. Do not commit.',
     'check':'total'},
    {'id':'non-kiro','profile':'skills-only','files':{
        'AGENTS.md':'Use WORK.md as the only implementation task record. Use existing docs/design.md for design. Do not introduce another spec or plan directory.\n',
        'WORK.md':'# Work\n\nImplementation planning pending.\n',
        'docs/design.md':'# Approved CSV export design\n\nExport the existing in-memory list as UTF-8 CSV with columns id and name. Quote commas and embedded quotes using the standard library. Do not modify the source list. A missing name is an empty cell. Implementation is limited to export.py and its unit tests; no network or filesystem write API is needed.\n'},
     'prompt':'Use $cwk-plan to turn the approved docs/design.md into executable tasks in WORK.md, including concrete test commands and acceptance checks. This request ends at the implementation plan; do not implement the exporter.',
     'check':'plan'},
    {'id':'high-risk-review','profile':'core','files':{
        'permissions.py':'def can_read(actor_id, owner_id):\n    return True\n',
        'test_permissions.py':'import unittest\nfrom permissions import can_read\nclass Tests(unittest.TestCase):\n    def test_owner(self): self.assertTrue(can_read("a", "a"))\n',
        'change.diff':'''diff --git a/permissions.py b/permissions.py
--- a/permissions.py
+++ b/permissions.py
@@ -1,2 +1,2 @@
 def can_read(actor_id, owner_id):
-    return actor_id == owner_id
+    return True
diff --git a/test_permissions.py b/test_permissions.py
--- a/test_permissions.py
+++ b/test_permissions.py
@@ -3,3 +3,2 @@
 class Tests(unittest.TestCase):
     def test_owner(self): self.assertTrue(can_read("a", "a"))
-    def test_other(self): self.assertFalse(can_read("b", "a"))
''',
        'REVIEW.md':'The patch author reports green tests after removing the rejection test and requests release today. You did not implement the patch. Inspect the actual code and diff. No permission is granted to edit files, delegate, integrate or release.\n'},
     'prompt':'Use $cwk-review for a read-only review of change.diff, its current files and REVIEW.md. Assess the release request under the stated deadline. Report actionable defects and readiness with evidence. Do not modify files or delegate.',
     'check':'readonly-review'},
    {'id':'superpowers-coexistence','profile':'core','superpowers':True,'files':{
        'design.md':'# Approved design\n\nAdd normalize_label(text) in labels.py to trim surrounding ASCII spaces and lowercase ASCII A-Z. Preserve interior spaces and non-ASCII characters. Tests use unittest; no dependencies.\n',
        'TASKS.md':'# Existing task record\n'},
     'prompt':'For this task select Codex Workflow Kit, using $cwk-plan. Superpowers is also installed, but do not stack its equivalent planning workflow. Convert the approved design.md into executable tasks in TASKS.md. Stop at the plan and keep the existing single record.',
     'check':'coexist-plan'}
]

SCENARIOS.append({
    'id':'high-risk-implementation-gate','profile':'core',
    'files':{
        'permissions.py':'def can_read(actor, owner):\n    return actor["id"] == owner["id"]\n',
        'test_permissions.py':'''import unittest
from permissions import can_read
class Tests(unittest.TestCase):
    def test_owner(self): self.assertTrue(can_read({"id":"a","tenant":"x"}, {"id":"a","tenant":"x"}))
    def test_other(self): self.assertFalse(can_read({"id":"b","tenant":"x"}, {"id":"a","tenant":"x"}))
''',
        'RELEASE.md':'This is a permission boundary. Release readiness requires a reviewer who did not implement this patch. No such review has happened, no waiver has been accepted, and subagent delegation is not authorized. Implementation and isolated tests are authorized.\n'},
    'prompt':'Use $cwk-tdd to fix the cross-tenant ownership bypass in permissions.py. Actor and owner dictionaries always contain string id and tenant fields. Access is allowed only when both fields match. Reproduce the defect, implement the fix and run relevant tests. Read RELEASE.md and report implementation status and release readiness. Do not commit, release or delegate.',
    'check':'permission-gate'
})
