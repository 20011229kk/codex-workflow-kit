import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('check_public',Path(__file__).resolve().parents[1]/'scripts/check_public.py')
checker=importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

class PublicTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        (self.root/'README.md').write_text('Public candidate\n')
        self.freeze()

    def freeze(self):
        paths=[p for p in self.root.rglob('*') if p.is_file() and p.name!='PUBLICATION_MANIFEST.json']
        data={'schema':1,'files':[{'path':str(p.relative_to(self.root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'role':'test'} for p in paths]}
        (self.root/'PUBLICATION_MANIFEST.json').write_text(json.dumps(data))

    def findings(self):return checker.inspect(self.root)['findings']

    def test_valid_tree(self):self.assertEqual(self.findings(),[])
    def test_tampered(self):
        (self.root/'README.md').write_text('Changed\n')
        self.assertTrue(any('digest mismatch' in s for s in self.findings()))
    def test_extra(self):
        (self.root/'unreviewed.txt').write_text('Extra')
        self.assertTrue(any('unlisted' in s for s in self.findings()))
    def test_missing(self):
        (self.root/'README.md').unlink()
        self.assertTrue(any('missing' in s for s in self.findings()))
    def test_broken_and_external_links(self):
        (self.root/'README.md').write_text('[remote](https://example.com) [missing](docs/missing.md)')
        self.freeze()
        self.assertTrue(any('broken local link' in s for s in self.findings()))
    def test_valid_relative_link(self):
        (self.root/'guide.md').write_text('Guide')
        (self.root/'README.md').write_text('[guide](guide.md#heading)')
        self.freeze()
        self.assertEqual(self.findings(),[])
    def test_symlink_not_followed(self):
        try:(self.root/'outside').symlink_to(self.root.parent,target_is_directory=True)
        except OSError:self.skipTest('Symlinks unavailable')
        self.assertTrue(any('symlink' in s for s in self.findings()))
    def test_secret_redaction(self):
        token='ghp_'+'a'*30
        (self.root/'sample.txt').write_text(token)
        self.freeze()
        result=self.findings()
        self.assertTrue(any('possible credential' in s for s in result))
        self.assertNotIn(token,str(result))
    def test_unsafe_manifest_and_duplicates(self):
        path=self.root/'PUBLICATION_MANIFEST.json'
        data=json.loads(path.read_text())
        data['files'].append(data['files'][0])
        path.write_text(json.dumps(data))
        self.assertTrue(any('duplicate' in s for s in self.findings()))
        data['files'][0]['path']='../outside'
        path.write_text(json.dumps(data))
        self.assertTrue(any('unsafe' in s for s in self.findings()))
    def test_prohibited_file_even_if_listed(self):
        (self.root/'.env').write_text('EXAMPLE=value')
        self.freeze()
        self.assertTrue(any('prohibited file' in s for s in self.findings()))
    def test_scan_is_readonly(self):
        before={str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.findings()
        self.assertEqual(before,{str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

if __name__=='__main__':unittest.main()
