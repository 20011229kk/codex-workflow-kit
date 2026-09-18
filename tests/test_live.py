"""Privacy and isolation contracts for opt-in model evaluation tools."""
import json
import os
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'evals/behavior'))
import live


class LivePrivacyTests(unittest.TestCase):
    def test_provider_literal_and_indented_urls_are_redacted(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);auth=root/'auth.json';auth.write_text('{}')
            config=root/'model.toml';address='https://synthetic-private-provider.example/v1'
            for line in ['  base_url = "'+address+'"',"base_url = '"+address+"'"]:
                with self.subTest(line=line):
                    config.write_text('[model_providers.example]\n'+line+'\n')
                    cleaned=live.scrub('Connection failed: '+address,live.private_redactions(auth,config))
                    self.assertNotIn('synthetic-private-provider.example',cleaned)

    def test_fixture_probe_uses_explicit_isolated_environment(self):
        import tasks
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);home=root/'home';home.mkdir()
            with patch.dict(os.environ,{'HOME':'/synthetic/ambient-home','CODEX_HOME':'/synthetic/ambient-state','OPENAI_API_KEY':'synthetic-ambient-key'},clear=True):
                env=live.isolated_env(home)
                result=tasks.execute_python(root,'import json,os;print(json.dumps({k:os.environ.get(k) for k in ("HOME","CODEX_HOME","OPENAI_API_KEY")}))',env)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(json.loads(result.stdout),{'HOME':str(home),'CODEX_HOME':str(home/'.codex'),'OPENAI_API_KEY':None})

    def exercise_timeout(self, kind):
        import tasks
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);auth=root/'auth.json';secret='synthetic-sensitive-auth'
            auth.write_text(json.dumps({'OPENAI_API_KEY':secret}))
            config=root/'model.toml';config.write_text('model = "example"\n')
            output=root/'output'
            def simulate(cmd,**kwargs):
                if 'exec' in cmd:
                    raise subprocess.TimeoutExpired(cmd,1,output=json.dumps({'message':secret}).encode()+b'\n',stderr=secret.encode())
                return subprocess.CompletedProcess(cmd,0,'{"version":"0.1.0-beta"}','')
            with patch.object(live.subprocess,'run',side_effect=simulate),patch.object(live.subprocess,'check_output',return_value='codex test'):
                if kind=='routing':
                    with self.assertRaises(RuntimeError):live.run_routing(Path('/synthetic/codex'),auth,config,output,'skills-only')
                    case='01'
                else:
                    args=SimpleNamespace(case=['small-edit'],output=output,model_config=config,auth_source=auth,cli=Path('/synthetic/codex'),superpowers=None)
                    self.assertEqual(tasks.run(args),1)
                    case='small-edit'
                    self.assertTrue((output/case/'after.json').exists())
            metadata=json.loads((output/'run.json').read_text())
            self.assertEqual(metadata['cases'][0]['exit'],124)
            self.assertTrue(metadata['cases'][0]['timed_out'])
            for name in ('events.jsonl','stderr.txt'):
                text=(output/case/name).read_text()
                self.assertNotIn(secret,text)
                self.assertIn('<AUTH_REDACTED>',text)

    def test_routing_timeout_preserves_sanitized_partial_evidence(self):
        self.exercise_timeout('routing')

    def test_task_timeout_preserves_sanitized_partial_evidence(self):
        self.exercise_timeout('task')

    def test_sensitive_auth_and_endpoint_are_redacted(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            secret='sk-'+'x'*30
            auth=root/'auth.json';auth.write_text(json.dumps({'OPENAI_API_KEY':secret,'tokens':{'refresh_token':'refresh-sensitive-value'}}))
            config=root/'model.toml';config.write_text('model = "example-model"\n[model_providers.example]\nbase_url = "https://private-provider.example/v1"\n')
            mapping=live.private_redactions(auth,config)
            original='Authorization: Bearer '+secret+' refresh-sensitive-value POST https://private-provider.example/v1/responses model=example-model'
            cleaned=live.scrub(original,mapping)
            self.assertNotIn(secret,cleaned)
            self.assertNotIn('refresh-sensitive-value',cleaned)
            self.assertNotIn('private-provider.example',cleaned)
            self.assertIn('model=example-model',cleaned)

    def test_environment_does_not_inherit_personal_agent_state(self):
        with patch.dict(os.environ,{'CODEX_THREAD_ID':'private-thread','OPENAI_API_KEY':'private-key','PATH':'/usr/bin'},clear=True):
            env=live.isolated_env(Path('/temporary/evaluation/home'))
        self.assertNotIn('CODEX_THREAD_ID',env)
        self.assertNotIn('OPENAI_API_KEY',env)
        self.assertEqual(env['HOME'],'/temporary/evaluation/home')
        self.assertEqual(env['CODEX_HOME'],'/temporary/evaluation/home/.codex')

    def test_unknown_task_cannot_report_empty_success(self):
        import tasks
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);config=root/'model.toml';config.write_text('model = "example"\n')
            args=SimpleNamespace(case=['unknown-case'],output=root/'output',model_config=config,cli=Path(sys.executable))
            with self.assertRaises(ValueError): tasks.run(args)

    def test_longer_path_redacted_before_parent(self):
        self.assertEqual(live.scrub('/tmp/run/project/a',{'/tmp/run':'<ROOT>','/tmp/run/project':'<PROJECT>'}),'<PROJECT>/a')

    def test_event_redaction_handles_json_escaped_values(self):
        secret='sensitive-quote-"-and-newline-\n-value'
        event={'message':secret,'items':['keep this',secret]}
        encoded=json.dumps(event)+'\n'
        cleaned=live.scrub_events(encoded,{secret:'<AUTH_REDACTED>'})
        decoded=json.loads(cleaned)
        self.assertEqual(decoded,{'message':'<AUTH_REDACTED>','items':['keep this','<AUTH_REDACTED>']})
        self.assertNotIn(secret,cleaned)


if __name__=='__main__':unittest.main()
