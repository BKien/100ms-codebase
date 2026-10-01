"""Researcher-authorized one-time repository preparation; no DB/runtime mutation."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(r'D:\figma_spec\100ms Video Conferencing and Live Streaming')
ARCHIVE = ROOT / 'archive/financial-management/pre-100ms-2026-10-01'
SNAPSHOT = ROOT / 'resource/specification-sources/100ms-2026-10-01-001'
STAMP = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def digest(path):
    return 'sha256:' + hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path):
    return path.relative_to(ROOT).as_posix()


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8', newline='\n')


def dump(path, value):
    write(path, json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def checked(path):
    path = path.resolve()
    if not path.is_relative_to(ROOT.resolve()) or path == ROOT.resolve():
        raise ValueError('Operation outside exact repository scope')
    return path


def archive(path, move=True):
    path = checked(path)
    if not path.exists():
        return
    destination = checked(ARCHIVE / relative(path))
    if destination.exists():
        raise ValueError(f'Archive already exists: {relative(destination)}')
    files = [path] if path.is_file() else sorted(p for p in path.rglob('*') if p.is_file())
    for p in files:
        if p.name == '.env':
            raise ValueError('Secret-bearing env must not be archived')
        archive_entries.append({'original_path': relative(p), 'sha256': digest(p),
                                'archive_path': relative(ARCHIVE / relative(p))})
    destination.parent.mkdir(parents=True, exist_ok=True)
    if move:
        shutil.move(str(path), str(destination))
    elif path.is_dir():
        shutil.copytree(path, destination)
    else:
        shutil.copy2(path, destination)


def project(source_path, destination, artifact_type):
    original = source_path.read_text(encoding='utf-8-sig').replace('\r\n', '\n')
    match = re.match(r'^---\n(.*?)\n---\n', original, re.S)
    body = original[match.end():] if match else original
    old_fields = match.group(1).splitlines() if match else []
    identity = [line for line in old_fields if re.match(r'(uc_id|uc_name|api_id|related_uc_ids?):', line)]
    header = [f'artifact_type: {artifact_type}', 'status: Frozen', *identity,
              'source_type: local-markdown',
              'source_path: ' + json.dumps(str(SOURCE / source_path.relative_to(SNAPSHOT)), ensure_ascii=False),
              'source_snapshot_path: ' + relative(source_path),
              'source_sha256: ' + digest(source_path),
              'source_range: "Markdown: complete document"',
              'retrieved_at: ' + STAMP]
    # Every UC carries the supplied shared vocabulary in its UML section.
    if artifact_type == 'business-use-case-specification':
        marker = 'Classifiers and helper semantics are imported from the [shared domain model](shared-domain-model.md).'
        if marker not in body:
            raise ValueError(f'Unrecognized shared-model reference: {source_path.name}')
        body = body.replace(marker, marker + '\n\n### Frozen Shared Domain Model\n\n' + shared_model + '\n\n### Use-Case Operations')
    if artifact_type == 'ocl-utility-definitions':
        body = re.sub(r'> The spreadsheet row supplies[^\n]*',
                      '> Frozen projection of the researcher-provided 100ms Markdown utility document. The Financial spreadsheet reference in the source header describes its historical format; current authoritative provenance is the local source and checksum above.', body)
    body = body.replace('../../ASSUMPTIONS.md', '../ASSUMPTIONS.md')
    # The supplied source copy remains byte-exact in SNAPSHOT.
    # Explicit researcher instruction replaces copy-file provenance downstream.
    body = body.replace('ANYtlDoAyDRNwH6AByKGKK', 'lCvn1rB7IdRchqAuEatJJp')
    write(destination, '---\n' + '\n'.join(header) + '\n---\n' + body)
    projections.append({'source_snapshot_path': relative(source_path), 'source_sha256': digest(source_path),
                        'projection_path': relative(destination), 'projection_sha256': digest(destination),
                        'transformations': ['local-source provenance', 'Frozen status', 'relative-link relocation'] +
                        (['inline supplied shared UML vocabulary'] if artifact_type == 'business-use-case-specification' else [])})
    # Projection never alters or loses any local frozen OCL rule ID/text.
    source_ocl = re.findall(r'~~~ocl\n(.*?)\n~~~', original, re.S)
    target_ocl = re.findall(r'~~~ocl\n(.*?)\n~~~', body, re.S)
    if source_ocl != target_ocl:
        raise ValueError(f'OCL changed during import: {source_path.name}')


if __name__ == '__main__':
    if ARCHIVE.exists() or SNAPSHOT.exists():
        raise SystemExit('One-time setup already has an archive/snapshot; inspect the receipt instead of rerunning.')
    uc_files = sorted((SOURCE / '01-inception/uc').glob('uc-*.md'))
    api_files = sorted((SOURCE / '01-inception/api').glob('api-*.md'))
    if len(uc_files) != 18 or len(api_files) != 15:
        raise SystemExit('Source inventory differs from actual 18 UC / 15 API files (source README count is stale).')
    archive_entries, projections = [], []
    # Cold copies of all supplied Markdown and DB evidence; no probe/test scripts.
    source_entries = []
    for path in sorted(SOURCE.rglob('*')):
        if path.is_file() and path.suffix.lower() in {'.md', '.dbml', '.sql'}:
            dst = SNAPSHOT / path.relative_to(SOURCE)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dst)
            source_entries.append({'original_path': str(path), 'snapshot_path': relative(dst), 'sha256': digest(dst)})
    for path in ['PROJECT_PROFILE.json', 'docs/00-context/FIGMA-LINK-REVIEW.md',
                 'docs/00-context/sources/CONNECTED-SOURCES.md', 'PROJECT_CONTEXT.md']:
        archive(ROOT / path, move=False)
    for path in ['docs/01-inception/use-cases', 'docs/01-inception/api-contracts',
                 'finalsource/be/src', 'finalsource/fe/src', 'docs/00-context/engineering/schema.dbml',
                 '.codex/skills/restore-source-baseline/assets/source-baseline.zip',
                 'resource/VC-AWG-Demo_FinalCode-main']:
        archive(ROOT / path)
    for path in sorted((ROOT / 'resource/figma-design-dataset').iterdir()):
        if path.is_dir():
            archive(path)
    shared_model = (SNAPSHOT / '01-inception/uc/shared-domain-model.md').read_text(encoding='utf-8-sig')
    for path in uc_files:
        project(SNAPSHOT / path.relative_to(SOURCE), ROOT / 'docs/01-inception/use-cases' / path.name,
                'business-use-case-specification')
    project(SNAPSHOT / '01-inception/uc/shared-domain-model.md', ROOT / 'docs/01-inception/use-cases/shared-domain-model.md',
            'shared-domain-model')
    project(SNAPSHOT / 'OCL-UTILITY-DEFINITIONS.md', ROOT / 'docs/01-inception/use-cases/OCL-UTILITY-DEFINITIONS.md',
            'ocl-utility-definitions')
    for path in api_files:
        raw = path.read_text(encoding='utf-8-sig')
        api_id = re.search(r'^api_id: (.+)$', raw, re.M).group(1).strip()
        project(SNAPSHOT / path.relative_to(SOURCE), ROOT / 'docs/01-inception/api-contracts' / path.name,
                'api-contract')
    project(SNAPSHOT / '01-inception/api/common-contract.md', ROOT / 'docs/01-inception/api-contracts/common-contract.md',
            'common-api-contract')
    for name in ['ASSUMPTIONS.md', 'CONTEXT.md', 'FIGMA.md', 'coverage-report.md']:
        project(SNAPSHOT / name, ROOT / 'docs/01-inception' / name, 'specification-support')
    receipt = {'artifact_type': '100ms-source-retrieval', 'project_id': '100ms-video-conferencing',
               'retrieved_at': STAMP, 'source_type': 'local-markdown', 'source_root': str(SOURCE),
               'source_snapshot_root': relative(SNAPSHOT), 'sources': source_entries, 'projections': projections,
               'database_status': 'deferred-by-researcher',
               'database_note': 'DBML/SQL retained only in source snapshot; no active schema, migrations or runtime pins prepared.'}
    dump(ROOT / 'docs/00-context/sources/100ms-source-retrieval.json', receipt)
    dump(ARCHIVE / 'archive-manifest.json', {'archived_at': STAMP, 'repository_revision': 'ad24d09',
                                          'purpose': 'Cold Financial evidence; excluded from active 100ms inputs.', 'files': archive_entries})
    print(json.dumps({'status': 'imported', 'uc_count': 18, 'api_count': 15, 'projection_count': len(projections),
                      'archive_file_count': len(archive_entries), 'database': 'deferred'}, indent=2))
