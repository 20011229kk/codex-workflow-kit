"""Validate and package the complete Codex Workflow Kit marketplace (stdlib only)."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = Path('plugins/codex-workflow-kit')
NAMES = ('cwk-route', 'cwk-design', 'cwk-plan', 'cwk-execute',
         'cwk-tdd', 'cwk-debug', 'cwk-review', 'cwk-verify')
RUNTIME = {'.codex-plugin/plugin.json', 'LICENSE', 'THIRD_PARTY_NOTICES.md',
           'licenses/Superpowers-MIT.txt', 'skills/cwk-tdd/writing-good-tests.md',
           'skills/cwk-review/code-reviewer.md', 'skills/cwk-review/quality-gates.md'}
RUNTIME.update('skills/'+name+'/SKILL.md' for name in NAMES)
TOP = {'.agents/plugins/marketplace.json', 'VERSION', 'INSTALL.md'}
UPSTREAM_LICENSE_SHA256 = 'a37e0e9697144819e1d965176ac4ae5bc3fa02d11e7812036bbcadf6dafe2400'


def validate(root):
    root = Path(root).resolve()
    plugin = root/PLUGIN
    if any(p.is_symlink() for p in plugin.rglob('*')) or plugin.is_symlink():
        raise ValueError('Runtime symlinks are not distributable')
    actual = {p.relative_to(plugin).as_posix() for p in plugin.rglob('*') if p.is_file()}
    if actual != RUNTIME:
        raise ValueError('Runtime file set differs: '+str(sorted(actual ^ RUNTIME)))
    files = sorted(TOP | {(PLUGIN/name).as_posix() for name in RUNTIME})
    for name in files:
        path = root/name
        if not path.is_file() or any(p.is_symlink() for p in [path, *path.parents] if p != root):
            raise ValueError('Missing or symlinked distribution file: '+name)
    if hashlib.sha256((plugin/'licenses/Superpowers-MIT.txt').read_bytes()).hexdigest() != UPSTREAM_LICENSE_SHA256:
        raise ValueError('Upstream license must retain the verified complete notice')
    manifest = json.loads((plugin/'.codex-plugin/plugin.json').read_text())
    version = (root/'VERSION').read_text().strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?', version):
        raise ValueError('Invalid release version')
    if manifest.get('name') != 'codex-workflow-kit' or manifest.get('version') != version:
        raise ValueError('Plugin identity/version differs from release')
    if manifest.get('skills') != './skills/' or manifest.get('license') != 'MIT':
        raise ValueError('Unexpected skill path or license')
    market = json.loads((root/'.agents/plugins/marketplace.json').read_text())
    entries = market.get('plugins', [])
    if (market.get('name') != 'codex-workflow-kit' or len(entries) != 1
            or entries[0].get('name') != manifest['name']
            or entries[0].get('source') != {'source': 'local', 'path': './plugins/codex-workflow-kit'}):
        raise ValueError('Marketplace must resolve the complete local plugin')
    for name in NAMES:
        text = (plugin/'skills'/name/'SKILL.md').read_text()
        header = text.split('---', 2)
        if len(header) != 3 or header[0].strip():
            raise ValueError('Invalid skill frontmatter: '+name)
        if not re.search(r'^name: '+re.escape(name)+r'$', header[1], re.M):
            raise ValueError('Skill name does not match its namespace: '+name)
        if not re.search(r'^description: .+', header[1], re.M):
            raise ValueError('Missing skill description: '+name)
    for file in sorted(plugin.rglob('*.md')):
        for link in re.findall(r'\]\(([^)]+)\)', file.read_text()):
            target = unquote(link.strip('<>').split('#', 1)[0])
            if not target or re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target):
                continue
            destination = (file.parent/target).resolve()
            try: destination.relative_to(plugin)
            except ValueError: raise ValueError('Reference escapes plugin: '+target)
            if not destination.is_file():
                raise ValueError('Missing referenced resource: '+target)
    return {'version': version, 'skills': list(NAMES), 'files': files}


def build(root, output):
    root, output = Path(root).resolve(), Path(output)
    info = validate(root)
    payload = {name: (root/name).read_bytes() for name in info['files']}
    snapshot = {'schema': 1, 'package': 'codex-workflow-kit', 'version': info['version'],
                'files': {name: hashlib.sha256(raw).hexdigest() for name, raw in payload.items()}}
    payload['BUNDLE.json'] = (json.dumps(snapshot, sort_keys=True, indent=2)+'\n').encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation preserves existing user artifacts, including symlink targets.
    with output.open('xb') as stream:
        with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_STORED) as archive:
            for name, raw in sorted(payload.items()):
                entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                entry.create_system = 3
                entry.external_attr = 0o100644 << 16
                archive.writestr(entry, raw)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['check', 'build'])
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        result = validate(args.root)
        if args.action == 'build':
            output = args.output or args.root/'dist'/('codex-workflow-kit-'+result['version']+'.zip')
            path = build(args.root, output)
            result = {'archive': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                      'version': result['version']}
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print('Distribution check failed: '+str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__': sys.exit(main())
