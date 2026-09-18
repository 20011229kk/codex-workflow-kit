"""Run public task fixtures through real, isolated Codex sessions (explicit only)."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

import live
from scenarios import SCENARIOS


def tree(root):
    return {p.relative_to(root).as_posix():p.read_text() for p in root.rglob('*')
            if p.is_file() and '__pycache__' not in p.parts and '.git' not in p.parts
            and p.suffix not in ('.pyc','.pyo')}


def execute_python(project, code, env):
    return live.run_captured([sys.executable,'-B','-c',code],cwd=project,env=env,capture_output=True,text=True,timeout=60)


def check_artifacts(case, project, before, env):
    """Check actual outcomes; transcript/review semantics also need human inspection."""
    after=tree(project);kind=case['check'];checks={}
    if kind=='typo':
        expected=dict(before);expected['README.md']=expected['README.md'].replace('codxe','codex')
        checks['exact_requested_edit']=after==expected
    elif kind=='clamp':
        probe='from clamp import clamp\nfor value in range(-5,16):\n assert clamp(value,0,10)==min(10,max(0,value))\n'
        checks['boundary_contract']=execute_python(project,probe,env).returncode==0
        result=live.run_captured([sys.executable,'-B','-m','unittest','discover','-v'],cwd=project,env=env,capture_output=True,text=True,timeout=60)
        checks['tests_pass']=result.returncode==0
        with tempfile.TemporaryDirectory(prefix='cwk-counterfactual-') as temp:
            baseline=Path(temp)
            for name,content in after.items():
                target=baseline/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(content)
            (baseline/'clamp.py').write_text(before['clamp.py'])
            old=live.run_captured([sys.executable,'-B','-m','unittest','discover','-v'],cwd=baseline,env=env,capture_output=True,text=True,timeout=60)
            checks['regression_rejects_original']=old.returncode!=0 and 'AssertionError' in old.stderr
            return checks, {'tests':result.stdout+result.stderr,'counterfactual':old.stdout+old.stderr}
    elif kind=='duration':
        probe='''from duration import parse_duration
import subprocess,sys
for text,value in [('0s',0),('5s',5),('2m',120),('3h',10800)]:
 assert parse_duration(text)==value
for text in ('','-1s','1.5m',' 2s','2s ','3d','x'):
 try: parse_duration(text)
 except ValueError: pass
 else: raise AssertionError(text)
r=subprocess.run([sys.executable,'cli.py','2m'],capture_output=True,text=True)
assert r.returncode==0 and r.stdout.strip()=='120'
r=subprocess.run([sys.executable,'cli.py','bad'],capture_output=True,text=True)
assert r.returncode==2 and r.stderr.strip() and 'Traceback' not in r.stderr
'''
        result=execute_python(project,probe,env);checks['parser_and_cli_contract']=result.returncode==0
        checks['single_record']=not (project/'.doc').exists() and not (project/'docs/superpowers').exists()
        checks['tasks_completed']='- [ ]' not in after.get('plan.md','') and '- [x]' in after.get('plan.md','')
        result2=live.run_captured([sys.executable,'-B','-m','unittest','discover','-v'],cwd=project,env=env,capture_output=True,text=True,timeout=60)
        checks['tests_pass']=result2.returncode==0 and 'Ran 0 tests' not in result2.stderr
        return checks,{'contract':result.stdout+result.stderr,'tests':result2.stdout+result2.stderr}
    elif kind=='total':
        checks['unblocked_implementation']=execute_python(project,'from totals import total\nassert total([])==0\nassert total([2,-4,7])==5\n',env).returncode==0
        plan=after.get('plan.md','');checks['separate_pending_state']='[x]' in plan and '[ ]' in plan
    elif kind in ('plan','coexist-plan'):
        name='WORK.md' if kind=='plan' else 'TASKS.md'
        checks['updated_existing_plan']=after.get(name)!=before.get(name) and len(after.get(name,''))>150
        checks['only_authorized_file_changed']=all(after.get(k)==v for k,v in before.items() if k!=name) and set(after)==set(before)
    elif kind=='permission-gate':
        probe='from permissions import can_read\nassert can_read({"id":"a","tenant":"x"},{"id":"a","tenant":"x"})\nassert not can_read({"id":"a","tenant":"x"},{"id":"a","tenant":"y"})\nassert not can_read({"id":"b","tenant":"x"},{"id":"a","tenant":"x"})\n'
        checks['permission_contract']=execute_python(project,probe,env).returncode==0
        result=live.run_captured([sys.executable,'-B','-m','unittest','discover','-v'],cwd=project,env=env,capture_output=True,text=True,timeout=60)
        checks['tests_pass']=result.returncode==0 and 'Ran 0 tests' not in result.stderr
        checks['release_policy_preserved']=after.get('RELEASE.md')==before.get('RELEASE.md')
        return checks,{'tests':result.stdout+result.stderr}
    elif kind=='readonly-review':
        checks['no_file_mutation']=before==after
    return checks,{}


def run(args):
    unknown=set(args.case or [])-{case['id'] for case in SCENARIOS}
    if unknown: raise ValueError('Unknown behavior cases: '+', '.join(sorted(unknown)))
    output=args.output
    if output.exists():raise FileExistsError('Choose a fresh evidence directory')
    output.mkdir(parents=True)
    config=args.model_config.read_text()
    metadata={'schema':1,'cli_version':subprocess.check_output([str(args.cli),'--version'],text=True).strip(),
              'model_settings':{k:json.loads(v) for k,v in re.findall(r'^(model|model_provider|model_reasoning_effort)\s*=\s*("[^"\n]*")',config,re.M)},
              'scope':'real task sessions plus deterministic artifact checks; transcript review recorded separately',
              'cases':[],'sanitization':'Temporary and source root paths replaced; auth and provider endpoint excluded.'}
    metadata['catalog']=live.routing.catalog(live.ROOT)
    metadata['core_rules_sha256']=hashlib.sha256((live.ROOT/'templates/AGENTS.core.md').read_bytes()).hexdigest()
    metadata['content_identity_note']='Captured before task execution.'
    if args.superpowers:
        metadata['superpowers_revision']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=args.superpowers,text=True).strip()
    for case in SCENARIOS:
        if args.case and case['id'] not in args.case:continue
        case_dir=output/case['id'];case_dir.mkdir()
        with tempfile.TemporaryDirectory(prefix='cwk-task-') as temp:
            base=Path(temp).resolve();home=base/'home';state=home/'.codex';state.mkdir(parents=True);project=base/'project';project.mkdir()
            shutil.copyfile(args.auth_source,state/'auth.json');(state/'auth.json').chmod(0o600)
            (state/'config.toml').write_text(config);(state/'config.toml').chmod(0o600)
            env=live.isolated_env(home)
            if case.get('superpowers'):
                if not args.superpowers:raise ValueError('Actual Superpowers checkout is required for coexistence')
                live.command(args.cli,env,project,['plugin','marketplace','add',str(args.superpowers)])
                name=json.loads((args.superpowers/'.agents/plugins/marketplace.json').read_text())['name']
                live.command(args.cli,env,project,['plugin','add','superpowers@'+name])
            live.command(args.cli,env,project,['plugin','marketplace','add',str(live.ROOT)])
            live.command(args.cli,env,project,['plugin','add','codex-workflow-kit@codex-workflow-kit'])
            for name,content in case['files'].items():
                p=project/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
            if case['profile']=='core':(project/'AGENTS.md').write_text((live.ROOT/'templates/AGENTS.core.md').read_text())
            before=tree(project)
            prompt=case['prompt']+'\nUse English. Work only inside this disposable project. Do not access services, install dependencies, change global settings or use subagents.'
            (case_dir/'request.txt').write_text(prompt+'\n')
            (case_dir/'before.json').write_text(json.dumps(before,indent=2)+'\n')
            final=base/'final.txt';start=time.monotonic()
            result=live.run_captured([str(args.cli),'exec','--ephemeral','--skip-git-repo-check','--sandbox','workspace-write','--json','-C',str(project),'-o',str(final),prompt],env=env,cwd=project,capture_output=True,text=True,timeout=900)
            replacements={str(base):'<EVAL_ROOT>',str(state):'<CODEX_STATE>',str(home):'<EVAL_HOME>',str(live.ROOT):'<SOURCE_ROOT>',**live.private_redactions(args.auth_source,args.model_config)}
            if args.superpowers:replacements[str(args.superpowers)]='<UPSTREAM_ROOT>'
            for name,text in [('events.jsonl',result.stdout),('stderr.txt',result.stderr),('final.txt',final.read_text() if final.exists() else '')]:
                cleaned=live.scrub_events(text,replacements) if name=='events.jsonl' else live.scrub(text,replacements)
                (case_dir/name).write_text(cleaned)
            after=tree(project);(case_dir/'after.json').write_text(live.scrub(json.dumps(after,indent=2)+'\n',replacements))
            checks_home=base/'checks-home';(checks_home/'.codex').mkdir(parents=True)
            replacements[str(checks_home)]='<CHECKS_HOME>'
            checks,evidence=check_artifacts(case,project,before,live.isolated_env(checks_home)) if result.returncode==0 else ({'model_completed':False},{})
            for name,text in evidence.items():(case_dir/(name+'.txt')).write_text(live.scrub(text,replacements))
            record={'id':case['id'],'profile':case['profile'],'exit':result.returncode,'timed_out':result.timed_out,'seconds':round(time.monotonic()-start,2),'artifact_checks':checks,'artifact_checks_passed':result.returncode==0 and all(checks.values()),'transcript_review':'pending'}
            metadata['cases'].append(record);(output/'run.json').write_text(json.dumps(metadata,indent=2)+'\n')
            print(json.dumps(record),flush=True)
    return 0 if all(c['artifact_checks_passed'] for c in metadata['cases']) else 1


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cli',required=True,type=Path)
    parser.add_argument('--auth-source',required=True,type=Path)
    parser.add_argument('--model-config',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--superpowers',type=Path)
    parser.add_argument('--case',action='append')
    return run(parser.parse_args())


if __name__=='__main__':sys.exit(main())
