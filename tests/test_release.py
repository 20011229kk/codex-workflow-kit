"""Distribution contracts exercised on complete temporary plugin fixtures."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('release', ROOT/'scripts/release.py')
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)/'repo'
        self.root.mkdir()
        for name in ('.agents', 'plugins'):
            shutil.copytree(ROOT/name, self.root/name)
        for name in ('VERSION', 'INSTALL.md'):
            shutil.copyfile(ROOT/name, self.root/name)
        self.plugin = self.root/'plugins/codex-workflow-kit'

    def test_complete_bundle_is_installable(self):
        info = release.validate(self.root)
        self.assertEqual(info['version'], (self.root/'VERSION').read_text().strip())
        self.assertEqual(len(info['skills']), 8)
        archive = release.build(self.root, self.root.parent/'release.zip')
        with zipfile.ZipFile(archive) as bundle:
            snapshot = json.loads(bundle.read('BUNDLE.json'))
            self.assertIn('.agents/plugins/marketplace.json', snapshot['files'])
            for name, digest in snapshot['files'].items():
                self.assertEqual(hashlib.sha256(bundle.read(name)).hexdigest(), digest)
            self.assertEqual(set(bundle.namelist()), set(snapshot['files']) | {'BUNDLE.json'})

    def test_archives_are_byte_identical(self):
        a = release.build(self.root, self.root.parent/'a.zip')
        b = release.build(self.root, self.root.parent/'b.zip')
        self.assertEqual(a.read_bytes(), b.read_bytes())

    def test_missing_license_rejected(self):
        (self.plugin/'licenses/Superpowers-MIT.txt').unlink()
        with self.assertRaises(ValueError): release.validate(self.root)

    def test_modified_upstream_license_rejected(self):
        (self.plugin/'licenses/Superpowers-MIT.txt').write_text('MIT license without the required notice')
        with self.assertRaises(ValueError): release.validate(self.root)

    def test_unlisted_runtime_file_rejected(self):
        (self.plugin/'private.txt').write_text('Unreviewed')
        with self.assertRaises(ValueError): release.validate(self.root)

    def test_symlink_rejected(self):
        path = self.plugin/'licenses/Superpowers-MIT.txt'
        path.unlink()
        path.symlink_to(ROOT/'LICENSE')
        with self.assertRaises(ValueError): release.validate(self.root)

    def test_foreign_skill_name_rejected(self):
        p = self.plugin/'skills/cwk-tdd/SKILL.md'
        p.write_text(p.read_text().replace('name: cwk-tdd', 'name: test-driven-development'))
        with self.assertRaises(ValueError): release.validate(self.root)

    def test_missing_referenced_resource_rejected(self):
        p = self.plugin/'skills/cwk-review/quality-gates.md'
        p.unlink()
        with self.assertRaises(ValueError): release.validate(self.root)

    def test_reference_cannot_escape_plugin(self):
        p = self.plugin/'skills/cwk-review/SKILL.md'
        p.write_text(p.read_text()+'\n[external](../../../../INSTALL.md)\n')
        with self.assertRaises(ValueError): release.validate(self.root)

    def test_version_disagreement_rejected(self):
        (self.root/'VERSION').write_text('0.2.0\n')
        with self.assertRaises(ValueError): release.validate(self.root)

    def test_marketplace_wrong_target_rejected(self):
        p = self.root/'.agents/plugins/marketplace.json'
        data = json.loads(p.read_text())
        data['plugins'][0]['source']['path'] = './plugins/other'
        p.write_text(json.dumps(data))
        with self.assertRaises(ValueError): release.validate(self.root)

    def test_existing_output_preserved(self):
        out = self.root.parent/'existing.zip'
        out.write_bytes(b'User-owned file')
        with self.assertRaises(FileExistsError): release.build(self.root, out)
        self.assertEqual(out.read_bytes(), b'User-owned file')


if __name__ == '__main__': unittest.main()
