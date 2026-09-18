"""Run explicitly requested real Codex evaluations in isolated local state.

No model is run by unit tests or CI. Supply an existing auth source and a minimal
model-only TOML config; never use this tool to export a complete user config.
"""
import argparse
import ast
import hashlib
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'evals/routing'))
import routing


def private_redactions(auth, config):
    """Mask supplied auth values and provider addresses without exposing either."""
    result = {}
    def collect(value):
        if isinstance(value, dict):
            for nested in value.values(): collect(nested)
        elif isinstance(value, list):
            for nested in value: collect(nested)
        elif isinstance(value, str) and len(value) >= 8:
            result[value] = '<AUTH_REDACTED>'
    collect(json.loads(Path(auth).read_text()))
    pattern = r'''(?:\bbase_url|"base_url"|'base_url')\s*=\s*("(?:\\.|[^"\\])*"|'[^']*')'''
    for encoded in re.findall(pattern, Path(config).read_text()):
        address = encoded[1:-1] if encoded.startswith("'") else ast.literal_eval(encoded)
        result[address] = '<PROVIDER_ENDPOINT>'
        host = urlsplit(address).netloc
        if host: result[host] = '<PROVIDER_HOST>'
    return result


def scrub(text, replacements):
    for original, label in sorted(replacements.items(), key=lambda x: -len(x[0])):
        text = text.replace(original, label)
    return text


def scrub_events(text, replacements):
    """Redact decoded JSON values, then retain their meaning in ASCII JSONL."""
    def visit(value):
        if isinstance(value, str): return scrub(value, replacements)
        if isinstance(value, list): return [visit(item) for item in value]
        if isinstance(value, dict):
            return {scrub(key, replacements): visit(item) for key, item in value.items()}
        return value
    lines = []
    for line in text.splitlines():
        try: value = json.loads(line)
        except ValueError: lines.append(scrub(line, replacements))
        else: lines.append(json.dumps(visit(value), ensure_ascii=True))
    return '\n'.join(lines)+('\n' if text.endswith('\n') else '')


def command(cli, env, cwd, args, timeout=60):
    result = subprocess.run([str(cli), *args], cwd=cwd, env=env, capture_output=True,
                            text=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError('Codex command failed: '+str(args[:3])+'; '+result.stderr[:1000])
    return result.stdout


def run_captured(args, **kwargs):
    """Retain partial model/probe output on timeout instead of losing evidence."""
    try:
        result = subprocess.run(args, **kwargs)
        result.timed_out = False
    except subprocess.TimeoutExpired as exc:
        def decoded(value):
            return value.decode('utf-8', errors='replace') if isinstance(value, bytes) else value or ''
        result = subprocess.CompletedProcess(args, 124, decoded(exc.stdout),
            decoded(exc.stderr)+'\nProcess exceeded the configured timeout.\n')
        result.timed_out = True
    except OSError as exc:
        result = subprocess.CompletedProcess(args, 127, '', 'Process could not start: '+str(exc)+'\n')
        result.timed_out = False
    return result


def isolated_env(home):
    keys = ('PATH', 'TMPDIR', 'LANG', 'LC_ALL', 'HTTPS_PROXY', 'HTTP_PROXY', 'NO_PROXY',
            'SSL_CERT_FILE', 'SSL_CERT_DIR')
    env = {key: os.environ[key] for key in keys if key in os.environ}
    env.update(HOME=str(home), CODEX_HOME=str(home/'.codex'), PYTHONDONTWRITEBYTECODE='1')
    return env


def run_routing(cli, auth, config, output, profile):
    if output.exists():
        raise FileExistsError('Keep prior evidence: choose a new output directory')
    output.mkdir(parents=True)
    suite = json.loads((ROOT/'evals/routing/cases.json').read_text())
    bundle = routing.prepare(ROOT, suite, profile=profile)
    (output/'input.json').write_text(json.dumps(bundle, indent=2)+'\n')
    observations = {'method': 'offline-decisions', 'run_label': output.name, 'decisions': []}
    metadata = {'scope': 'real model selection; no task execution', 'profile': profile,
                'cli_version': subprocess.check_output([str(cli), '--version'], text=True).strip(),
                'model_settings': {key: json.loads(value) for key, value in re.findall(
                    r'^(model|model_provider|model_reasoning_effort)\s*=\s*("[^"\n]*")',
                    config.read_text(), re.M)},
                'input_sha256': routing.digest(bundle), 'cases': [],
                'sanitization': 'Temporary and source root paths replaced with stable labels; auth/config excluded.'}
    with tempfile.TemporaryDirectory(prefix='cwk-live-routing-') as temp:
        base = Path(temp).resolve()
        home, project = base/'home', base/'project'
        state = home/'.codex'
        state.mkdir(parents=True); project.mkdir()
        shutil.copyfile(auth, state/'auth.json'); (state/'auth.json').chmod(0o600)
        shutil.copyfile(config, state/'config.toml'); (state/'config.toml').chmod(0o600)
        env = isolated_env(home)
        command(cli, env, project, ['plugin', 'marketplace', 'add', str(ROOT)])
        installed = json.loads(command(cli, env, project, ['plugin', 'add', 'codex-workflow-kit@codex-workflow-kit', '--json']))
        if profile == 'core':
            (project/'AGENTS.md').write_text(bundle['rules'])
        replacements = {str(base): '<EVAL_ROOT>', str(state): '<CODEX_STATE>', str(home): '<EVAL_HOME>', str(ROOT): '<SOURCE_ROOT>', **private_redactions(auth, config)}
        metadata['installed_version'] = installed['version']
        schema = base/'response-schema.json'
        schema.write_text(json.dumps({'type':'object','properties':{'id':{'type':'string'},'selected':{'type':'array','items':{'type':'string'}}},'required':['id','selected'],'additionalProperties':False}))
        for case in bundle['cases']:
            case_dir = output/case['id']; case_dir.mkdir()
            request = ('This is a workflow-selection evaluation, not an implementation task. '
                       'Use only the supplied catalog and request. Do not execute the request, use tools, '
                       'or inspect grading material. Choose only skills materially needed for the requested '
                       'deliverable, not hypothetical later stages. An empty selection is valid. '
                       'Return the case id and selected catalog IDs.\n'+json.dumps({
                           'catalog':bundle['catalog'], 'rules':bundle['rules'], 'case':case}))
            (case_dir/'request.txt').write_text(request+'\n')
            final = base/'answer.json'
            if final.exists(): final.unlink()
            start = time.monotonic()
            result = run_captured([str(cli), 'exec', '--ephemeral', '--skip-git-repo-check',
                '--sandbox', 'read-only', '--json', '-C', str(project), '--output-schema', str(schema),
                '-o', str(final), request], env=env, cwd=project, capture_output=True, text=True, timeout=240)
            (case_dir/'events.jsonl').write_text(scrub_events(result.stdout,replacements))
            (case_dir/'stderr.txt').write_text(scrub(result.stderr,replacements))
            record = {'id':case['id'], 'exit':result.returncode, 'timed_out':result.timed_out, 'seconds':round(time.monotonic()-start,2)}
            metadata['cases'].append(record)
            (output/'run.json').write_text(json.dumps(metadata,indent=2)+'\n')
            if result.returncode or not final.exists():
                raise RuntimeError('Real model case failed: '+case['id'])
            decision = json.loads(final.read_text())
            (case_dir/'response.json').write_text(json.dumps(decision,indent=2)+'\n')
            observations['decisions'].append(decision)
            (output/'observations.json').write_text(json.dumps(observations,indent=2)+'\n')
            print('Completed routing case '+case['id'], flush=True)
    graded = routing.grade(ROOT, suite, bundle, observations)
    (output/'score.json').write_text(json.dumps(graded,indent=2)+'\n')
    print(json.dumps({k:graded[k] for k in ('passed','passed_cases','total_cases')}), flush=True)
    return 0 if graded['passed'] else 1


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cli', required=True, type=Path)
    parser.add_argument('--auth-source', required=True, type=Path)
    parser.add_argument('--model-config', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--profile', choices=['skills-only','core'], default='skills-only')
    args=parser.parse_args()
    return run_routing(args.cli,args.auth_source,args.model_config,args.output,args.profile)


if __name__=='__main__':sys.exit(main())
