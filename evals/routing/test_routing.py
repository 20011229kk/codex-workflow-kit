"""Scorer contracts; these tests do not exercise an agent's skill selection."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
import subprocess
import sys

import routing


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        (self.repo/'templates').mkdir()
        (self.repo/'templates/AGENTS.core.md').write_text('Follow project rules.')
        for name in ('alpha', 'beta', 'gamma'):
            folder = self.repo/'plugins/codex-workflow-kit/skills'/name
            folder.mkdir(parents=True)
            (folder/'SKILL.md').write_text(f'---\nname: {name}\ndescription: Select {name}.\n---\nBody')
        self.suite = {'cases': [
            {'id': 'positive', 'prompt': 'Complete the specified task', 'required': ['alpha'],
             'allowed': ['alpha', 'beta'], 'one_of': []},
            {'id': 'negative', 'prompt': 'Only answer the question', 'required': [], 'allowed': [], 'one_of': []},
            {'id': 'competition', 'prompt': 'Choose one debugging workflow', 'required': [],
             'allowed': ['beta', 'gamma'], 'one_of': [['beta', 'gamma']]}
        ]}
        self.bundle = routing.prepare(self.repo, self.suite)
        self.observations = {'method': 'offline-decisions', 'run_label': 'unit-fixture', 'decisions': [
            {'id': 'positive', 'selected': ['alpha']},
            {'id': 'negative', 'selected': []},
            {'id': 'competition', 'selected': ['gamma']}
        ]}

    def grade(self):
        return routing.grade(self.repo, self.suite, self.bundle, self.observations)

    def test_valid_alternative(self):
        self.assertTrue(self.grade()['passed'])
        self.assertEqual(self.grade()['scope'], 'offline skill-selection decisions only')

    def test_missing_required(self):
        self.observations['decisions'][0]['selected'] = []
        self.assertFalse(self.grade()['passed'])

    def test_negative_rejects_extra_skill(self):
        self.observations['decisions'][1]['selected'] = ['alpha']
        self.assertFalse(self.grade()['passed'])

    def test_competing_workflows_not_stacked(self):
        self.observations['decisions'][2]['selected'] = ['beta', 'gamma']
        self.assertFalse(self.grade()['passed'])

    def test_missing_competition_choice(self):
        self.observations['decisions'][2]['selected'] = []
        self.assertFalse(self.grade()['passed'])

    def test_incomplete_run_is_invalid(self):
        self.observations['decisions'].pop()
        with self.assertRaises(ValueError): self.grade()

    def test_duplicate_case_is_invalid(self):
        self.observations['decisions'].append(self.observations['decisions'][0])
        with self.assertRaises(ValueError): self.grade()

    def test_unknown_case_or_skill_is_invalid(self):
        for field, value in [('id', 'unknown'), ('selected', ['unknown'])]:
            with self.subTest(field=field):
                obs = copy.deepcopy(self.observations)
                obs['decisions'][0][field] = value
                with self.assertRaises(ValueError): routing.grade(self.repo, self.suite, self.bundle, obs)

    def test_duplicate_skill_is_invalid(self):
        self.observations['decisions'][0]['selected'] *= 2
        with self.assertRaises(ValueError): self.grade()

    def test_rule_drift_invalidates_bundle(self):
        self.bundle = routing.prepare(self.repo, self.suite, profile='core')
        (self.repo/'templates/AGENTS.core.md').write_text('Changed')
        with self.assertRaises(ValueError): self.grade()

    def test_description_and_policy_drift(self):
        p=self.repo/'plugins/codex-workflow-kit/skills/alpha/SKILL.md'
        p.write_text(p.read_text().replace('Select alpha.', 'Something else.'))
        with self.assertRaises(ValueError): self.grade()
        self.bundle = routing.prepare(self.repo, self.suite)
        policy=p.parent/'agents/openai.yaml'
        policy.parent.mkdir()
        policy.write_text('policy:\n  allow_implicit_invocation: false\n')
        with self.assertRaises(ValueError): self.grade()

    def test_bundle_hides_answers(self):
        self.assertEqual(self.bundle['cases'], [{'id': c['id'], 'prompt': c['prompt']} for c in self.suite['cases']])
        self.assertNotIn('required', json.dumps(self.bundle))
        self.assertEqual(len(self.bundle['catalog']), 3)

    def test_skills_only_does_not_inject_optional_rules(self):
        bundle = routing.prepare(self.repo, self.suite)
        self.assertEqual(bundle['profile'], 'skills-only')
        self.assertEqual(bundle['rules'], '')
        (self.repo/'templates/AGENTS.core.md').write_text('Unadopted change')
        self.assertTrue(routing.grade(self.repo, self.suite, bundle, self.observations)['passed'])

    def test_core_profile_includes_actual_rules(self):
        bundle = routing.prepare(self.repo, self.suite, profile='core')
        self.assertEqual(bundle['rules'], (self.repo/'templates/AGENTS.core.md').read_text())
        self.assertEqual(bundle['profile'], 'core')

    def test_unknown_profile_rejected(self):
        with self.assertRaises(ValueError):
            routing.prepare(self.repo, self.suite, profile='invented')

    def test_bad_suite_rejected(self):
        for mutation in ('duplicate', 'unknown', 'contradiction', 'empty-group'):
            with self.subTest(mutation=mutation):
                s=copy.deepcopy(self.suite)
                if mutation=='duplicate': s['cases'].append(s['cases'][0])
                if mutation=='unknown': s['cases'][0]['allowed'].append('unknown')
                if mutation=='contradiction': s['cases'][0]['allowed']=[]
                if mutation=='empty-group': s['cases'][0]['one_of']=[[]]
                with self.assertRaises(ValueError): routing.prepare(self.repo, s)

    def test_unknown_method_rejected(self):
        self.observations['method']='actual-host-routing-proved'
        with self.assertRaises(ValueError): self.grade()

    def test_suite_drift_and_tampering(self):
        self.bundle['cases'][0]['prompt'] = 'Changed request'
        with self.assertRaises(ValueError): self.grade()
        self.bundle = routing.prepare(self.repo, self.suite)
        self.suite['cases'][0]['required'] = []
        with self.assertRaises(ValueError): self.grade()

    def test_malformed_selection(self):
        for value in ('alpha', [3], [['alpha']]):
            with self.subTest(value=value):
                self.observations['decisions'][0]['selected'] = value
                with self.assertRaises(ValueError): self.grade()

    def test_cli_exit_codes_and_prepare(self):
        paths = {}
        for name, value in [('suite', self.suite), ('bundle', self.bundle), ('observations', self.observations)]:
            paths[name] = self.repo/(name+'.json')
            paths[name].write_text(json.dumps(value))
        base = [sys.executable, str(Path(routing.__file__)), '--repo', str(self.repo), '--suite', str(paths['suite'])]
        prepared = subprocess.run([*base, 'prepare'], capture_output=True, text=True)
        self.assertEqual(prepared.returncode, 0)
        self.assertEqual(json.loads(prepared.stdout), self.bundle)
        command = [*base, 'grade', '--bundle', str(paths['bundle']), '--observations', str(paths['observations'])]
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
        self.observations['decisions'][0]['selected'] = []
        paths['observations'].write_text(json.dumps(self.observations))
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 1)
        paths['observations'].write_text('{}')
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)


if __name__ == '__main__': unittest.main()
