"""Offline selection evaluation, never a replacement for Codex's runtime router."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SUITE = Path(__file__).with_name('cases.json')


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def unique_strings(value):
    if not isinstance(value, list) or any(not isinstance(x, str) or not x for x in value):
        raise ValueError('Expected a list of nonempty skill IDs')
    if len(set(value)) != len(value):
        raise ValueError('Duplicate IDs')
    return set(value)


def catalog(repo):
    result = []
    for path in sorted((repo/'plugins/codex-workflow-kit/skills').glob('*/SKILL.md')):
        text = path.read_text(encoding='utf-8')
        frontmatter = text.split('---', 2)
        if len(frontmatter) < 3 or frontmatter[0].strip():
            raise ValueError(f'Invalid skill frontmatter: {path}')
        policy = path.parent/'agents/openai.yaml'
        result.append({'id': path.parent.name,
                       'frontmatter': frontmatter[1].strip(),
                       'invocation_metadata': policy.read_text(encoding='utf-8') if policy.exists() else '',
                       'skill_sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    unique_strings([s['id'] for s in result])
    return result


def validate_suite(suite, known):
    cases = suite['cases']
    if not isinstance(cases, list) or not cases:
        raise ValueError('Suite must contain cases')
    unique_strings([c['id'] for c in cases])
    for c in cases:
        if not isinstance(c['prompt'], str) or not c['prompt'].strip():
            raise ValueError('Missing prompt')
        required, allowed = unique_strings(c['required']), unique_strings(c['allowed'])
        if not required <= allowed <= known:
            raise ValueError('Unknown or contradictory skill expectations')
        if not isinstance(c['one_of'], list):
            raise ValueError('one_of must be a list')
        seen = set()
        for group in c['one_of']:
            choices = unique_strings(group)
            if not choices or not choices <= allowed or choices & seen or len(choices & required) > 1:
                raise ValueError('Invalid exclusive alternative group')
            seen |= choices


def prepare(repo, suite, profile='skills-only'):
    if profile not in ('skills-only', 'core'):
        raise ValueError('Unknown rule profile')
    skills = catalog(repo)
    validate_suite(suite, {s['id'] for s in skills})
    return {'schema': 1, 'scope': 'public core skills; not built-in/plugin discovery',
            'instructions': 'Choose only skills materially needed for the request, from this catalog. '
                            'An empty selection is valid. Return one decision per case with id and selected IDs. '
                            'Do not execute the requests. Judge each case independently. Select for the requested '
                            'deliverable, not hypothetical later lifecycle stages. External skills are out of scope.',
            'profile': profile,
            'rules': (repo/'templates/AGENTS.core.md').read_text(encoding='utf-8') if profile == 'core' else '',
            'catalog': skills, 'suite_sha256': digest(suite),
            'cases': [{'id': c['id'], 'prompt': c['prompt']} for c in suite['cases']]}


def grade(repo, suite, bundle, observations):
    if bundle != prepare(repo, suite, profile=bundle.get('profile')):
        raise ValueError('Rules, catalog, suite or prepared input changed; prepare a fresh evaluation')
    if observations.get('method') not in ('offline-decisions', 'author-informed'):
        raise ValueError('Declare offline-decisions or author-informed; runtime validation is separate')
    if not isinstance(observations.get('run_label'), str) or not observations['run_label'].strip():
        raise ValueError('Missing run label')
    decisions = observations['decisions']
    if not isinstance(decisions, list):
        raise ValueError('decisions must be a list')
    ids = unique_strings([d['id'] for d in decisions])
    if ids != {c['id'] for c in suite['cases']}:
        raise ValueError('Incomplete run or unknown case IDs')
    known = {s['id'] for s in bundle['catalog']}
    selected = {}
    for d in decisions:
        selected[d['id']] = unique_strings(d['selected'])
        if not selected[d['id']] <= known:
            raise ValueError('Unknown selected skill')
    results = []
    for c in suite['cases']:
        actual = selected[c['id']]
        missing = sorted(set(c['required'])-actual)
        extra = sorted(actual-set(c['allowed']))
        bad_groups = [g for g in c['one_of'] if len(actual & set(g)) != 1]
        results.append({'id': c['id'], 'passed': not (missing or extra or bad_groups),
                        'missing': missing, 'unexpected': extra, 'exclusive_choice_failures': bad_groups})
    return {'schema': 1, 'scope': 'offline skill-selection decisions only',
            'method': observations['method'], 'run_label': observations['run_label'],
            'bundle_sha256': digest(bundle), 'observations_sha256': digest(observations),
            'passed': all(r['passed'] for r in results), 'passed_cases': sum(r['passed'] for r in results),
            'total_cases': len(results), 'results': results,
            'limitations': 'No actual loading, task execution, independence or speed claim is established by this scorer.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['check', 'prepare', 'grade'])
    parser.add_argument('--repo', type=Path, default=ROOT)
    parser.add_argument('--suite', type=Path, default=SUITE)
    parser.add_argument('--bundle', type=Path)
    parser.add_argument('--observations', type=Path)
    parser.add_argument('--profile', choices=['skills-only', 'core'], default='skills-only')
    args = parser.parse_args()
    try:
        suite = json.loads(args.suite.read_text(encoding='utf-8'))
        if args.action == 'grade':
            if args.bundle is None or args.observations is None:
                raise ValueError('grade requires --bundle and --observations')
            result = grade(args.repo, suite, json.loads(args.bundle.read_text(encoding='utf-8')),
                           json.loads(args.observations.read_text(encoding='utf-8')))
        else:
            result = prepare(args.repo, suite, profile=args.profile)
            if args.action == 'check':
                result = {'valid_cases': len(result['cases']), 'catalog_skills': len(result['catalog']),
                          'model_evaluation': 'not run'}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result.get('passed') is False else 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(f'Invalid evaluation: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
