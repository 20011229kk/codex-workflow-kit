"""Read-only candidate inspection. Findings are heuristic, not publication clearance."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import unquote

MANIFEST='PUBLICATION_MANIFEST.json'
IGNORE_DIRS={'.git','__pycache__','.venv','node_modules','dist'}
CREDENTIALS=[re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,})\b'),
             re.compile(r'\bsk-[A-Za-z0-9_-]{24,}\b'),
             re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')]
MACHINE_PATH=re.compile('/'+'Users'+r'/[^\s/]+/|/'+'home'+r'/[^\s/]+/')
INTERNAL_HOST=re.compile(r'\b(?:[a-z0-9-]+\.)?private\.'+'easemob'+r'\.com',re.I)


def safe_relative(name):
    return (isinstance(name,str) and bool(name) and '\\' not in name and ':' not in name
            and not PurePosixPath(name).is_absolute()
            and not any(p in ('','..','.') for p in name.split('/')))


def inspect(root):
    root=Path(root).resolve()
    findings=[]
    manifest_path=root/MANIFEST
    if manifest_path.is_symlink():
        return {'files_checked':0,'findings':['manifest: symlink rejected']}
    try:
        data=json.loads(manifest_path.read_text(encoding='utf-8'))
        if data.get('schema')!=1 or not isinstance(data.get('files'),list):
            raise ValueError('invalid schema')
    except (OSError,ValueError,AttributeError):
        return {'files_checked':0,'findings':['manifest missing or invalid']}
    declared={}
    for item in data['files']:
        if not isinstance(item,dict) or not safe_relative(item.get('path')):
            findings.append('manifest: unsafe path');continue
        name=item['path']
        if name==MANIFEST or name in declared:
            findings.append('manifest: duplicate or self-referential path');continue
        declared[name]=item
    actual={}
    for folder,dirs,names in os.walk(root,followlinks=False):
        kept=[]
        for name in dirs:
            p=Path(folder)/name
            if p.is_symlink():findings.append(str(p.relative_to(root))+': symlink rejected')
            elif name not in IGNORE_DIRS:kept.append(name)
        dirs[:]=kept
        for name in names:
            p=Path(folder)/name
            rel=p.relative_to(root).as_posix()
            if rel==MANIFEST or name=='.DS_Store' or name.endswith(('.pyc','.pyo')):continue
            actual[rel]=p
    for name in sorted(set(declared)-set(actual)):findings.append(name+': missing file')
    for name in sorted(set(actual)-set(declared)):findings.append(name+': unlisted file')
    for rel,p in sorted(actual.items()):
        if p.is_symlink():
            findings.append(rel+': symlink rejected');continue
        if p.name in {'.env','auth.json','id_rsa','id_ed25519'} or p.suffix in {'.pem','.key','.sqlite','.log'}:
            findings.append(rel+': prohibited file')
        try:raw=p.read_bytes()
        except OSError:
            findings.append(rel+': unreadable file');continue
        if rel in declared and hashlib.sha256(raw).hexdigest()!=declared[rel].get('sha256'):
            findings.append(rel+': digest mismatch')
        try:text=raw.decode('utf-8')
        except UnicodeDecodeError:
            findings.append(rel+': binary file needs explicit review');continue
        for num,line in enumerate(text.splitlines(),1):
            if any(pattern.search(line) for pattern in CREDENTIALS):
                findings.append(f'{rel}:{num}: possible credential')
            if MACHINE_PATH.search(line):findings.append(f'{rel}:{num}: machine-specific path')
            if INTERNAL_HOST.search(line):findings.append(f'{rel}:{num}: internal host')
        if p.suffix=='.md':
            for link in re.findall(r'\]\(([^)]+)\)',text):
                target=unquote(link.strip('<>').split('#',1)[0])
                if not target or re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:',target):continue
                destination=(p.parent/target).resolve()
                try:destination.relative_to(root)
                except ValueError:
                    findings.append(rel+': local link escapes candidate');continue
                if not destination.exists():findings.append(rel+': broken local link: '+target)
    return {'files_checked':len(actual),'findings':findings,
            'limitations':'Heuristic inspection only; not a legal, secret-free or runtime guarantee.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args()
    result=inspect(args.root)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if result['findings'] else 0


if __name__=='__main__':sys.exit(main())
