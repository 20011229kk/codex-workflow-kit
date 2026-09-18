"""Exercise native plugin lifecycle in temporary HOME/CODEX_HOME; no model calls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import zipfile
import platform

import release


def environment(home):
    keys = ('PATH', 'TMPDIR', 'LANG', 'LC_ALL', 'HTTPS_PROXY', 'HTTP_PROXY', 'NO_PROXY')
    env = {k: os.environ[k] for k in keys if k in os.environ}
    env.update(HOME=str(home), CODEX_HOME=str(home/'.codex'))
    return env


def run(cli, env, cwd, args):
    result = subprocess.run([str(cli), *args], cwd=cwd, env=env, capture_output=True,
                            text=True, timeout=60)
    if result.returncode:
        raise RuntimeError('Native command failed: '+str(args[:3])+'; '+result.stderr[:1000])
    return result.stdout


def discover(cli, env, cwd):
    """Start a fresh host and inspect its actual skill catalog over JSON-RPC."""
    process = subprocess.Popen([str(cli), 'app-server', '--stdio'], cwd=cwd, env=env,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1)
    lines = queue.Queue()
    reader = threading.Thread(target=lambda: [lines.put(line) for line in process.stdout], daemon=True)
    reader.start()
    try:
        messages = [
            {'id': 1, 'method': 'initialize', 'params': {'clientInfo': {'name':'cwk-smoke','version':'0.1.0'},'capabilities':{'experimentalApi':True}}},
            {'method':'initialized'},
            {'id':2,'method':'skills/list','params':{'cwds':[str(cwd)],'forceReload':True}}]
        for message in messages:
            process.stdin.write(json.dumps(message)+'\n');process.stdin.flush()
        deadline = time.monotonic()+30
        while time.monotonic()<deadline:
            try: data=json.loads(lines.get(timeout=max(0.1, deadline-time.monotonic())))
            except queue.Empty: break
            if data.get('id') != 2: continue
            if 'error' in data: raise RuntimeError(str(data['error']))
            groups = data['result']['data']
            if any(g.get('errors') for g in groups): raise RuntimeError('Host reported skill errors')
            return [s for g in groups for s in g['skills'] if s.get('enabled')]
        raise RuntimeError('Fresh-host skill discovery timed out')
    finally:
        process.terminate()
        try: process.wait(timeout=10)
        except subprocess.TimeoutExpired: process.kill();process.wait()
        reader.join(timeout=2)


def smoke(cli, root, superpowers=None):
    info = release.validate(root)
    report = {'schema':1, 'scope':'native plugin lifecycle; no model behavior claim',
              'cli_version':subprocess.check_output([str(cli),'--version'],text=True).strip(),
              'platform':platform.system()+' '+platform.machine(), 'version':info['version'], 'checks':[]}
    with tempfile.TemporaryDirectory(prefix='cwk-native-smoke-') as temp:
        base = Path(temp).resolve();home = base/'home';project = base/'project'
        (home/'.codex').mkdir(parents=True);project.mkdir()
        archive = release.build(root, base/'kit.zip')
        candidate = base/'candidate'
        with zipfile.ZipFile(archive) as bundle: bundle.extractall(candidate)
        env = environment(home)
        sentinel = home/'.agents/skills/unrelated-sentinel/SKILL.md'
        sentinel.parent.mkdir(parents=True)
        sentinel.write_text('---\nname: unrelated-sentinel\ndescription: Handle explicit sentinel requests.\n---\nPreserve unrelated work.\n')
        rules = project/'AGENTS.md';rules.write_text('Use the existing project documentation.\n')
        protected = {sentinel:sentinel.read_bytes(),rules:rules.read_bytes()}
        if superpowers:
            run(cli,env,project,['plugin','marketplace','add',str(superpowers)])
            market=json.loads((superpowers/'.agents/plugins/marketplace.json').read_text())['name']
            run(cli,env,project,['plugin','add','superpowers@'+market])
        before = discover(cli,env,project)
        foreign = {s['name'] for s in before}
        if superpowers and not any(s.get('pluginId','').startswith('superpowers@') for s in before if s.get('pluginId')):
            raise AssertionError('Actual Superpowers plugin was not discovered')
        run(cli,env,project,['plugin','marketplace','add',str(candidate)])
        installed=json.loads(run(cli,env,project,['plugin','add','codex-workflow-kit@codex-workflow-kit','--json']))
        skills = discover(cli,env,project)
        kit = [s for s in skills if s.get('pluginId')=='codex-workflow-kit@codex-workflow-kit']
        expected = {'codex-workflow-kit:'+name for name in release.NAMES}
        assert {s['name'] for s in kit} == expected
        assert len({s['name'] for s in skills}) == len(skills), 'Duplicate discovered names'
        assert foreign <= {s['name'] for s in skills}
        cached = Path(installed['installedPath'])
        for name in release.RUNTIME:
            assert (cached/name).read_bytes() == (candidate/release.PLUGIN/name).read_bytes()
        report['checks'].append({'name':'archive-install-and-fresh-discovery','passed':True,'skills':sorted(expected)})
        manifest = candidate/release.PLUGIN/'.codex-plugin/plugin.json'
        updated=json.loads(manifest.read_text());updated['version']=info['version']+'+smoke.1'
        manifest.write_text(json.dumps(updated))
        resource=candidate/release.PLUGIN/'skills/cwk-review/quality-gates.md'
        resource.write_text(resource.read_text()+'\nLifecycle test update.\n')
        new=json.loads(run(cli,env,project,['plugin','add','codex-workflow-kit@codex-workflow-kit','--json']))
        assert new['version']==updated['version']
        assert (Path(new['installedPath'])/'skills/cwk-review/quality-gates.md').read_bytes()==resource.read_bytes()
        assert {s['name'] for s in discover(cli,env,project) if s.get('pluginId')=='codex-workflow-kit@codex-workflow-kit'}==expected
        report['checks'].append({'name':'updated-version-and-resource-visible-in-fresh-host','passed':True})
        run(cli,env,project,['plugin','remove','codex-workflow-kit@codex-workflow-kit'])
        after=discover(cli,env,project)
        assert not any(s.get('pluginId')=='codex-workflow-kit@codex-workflow-kit' for s in after)
        assert foreign <= {s['name'] for s in after}
        run(cli,env,project,['plugin','marketplace','remove','codex-workflow-kit'])
        assert all(p.read_bytes()==raw for p,raw in protected.items())
        assert not (home/'.codex/AGENTS.md').exists()
        report['checks'].append({'name':'uninstall-preserves-other-skills-and-project-rules','passed':True})
        report['superpowers_coexistence']=bool(superpowers)
        if superpowers:
            report['superpowers_revision']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=superpowers,text=True).strip()
        report['archive_sha256']=hashlib.sha256(archive.read_bytes()).hexdigest()
    report['passed']=all(c['passed'] for c in report['checks'])
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cli',required=True,type=Path)
    parser.add_argument('--root',type=Path,default=release.ROOT)
    parser.add_argument('--superpowers',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=smoke(args.cli,args.root.resolve(),args.superpowers.resolve() if args.superpowers else None)
    text=json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open('x') as out:out.write(text)
    print(text)


if __name__=='__main__':main()
