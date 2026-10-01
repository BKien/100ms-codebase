"""Finalize source baseline and preserve an honestly incomplete Figma capture."""
from datetime import datetime, timezone
import base64
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = '100ms-2026-10-01-001'
DATASET = ROOT / 'resource/figma-design-dataset' / VERSION
STAMP = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def sha(path):
    return 'sha256:' + hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path):
    return path.relative_to(ROOT).as_posix()


def retain_partial_payloads():
    for path in sorted((ROOT / '.tmp').glob('figma-*.json')):
        payload = json.loads(path.read_text(encoding='utf-8'))
        node = payload['node']
        folder = DATASET / 'nodes' / node['id'].replace(':', '-')
        folder.mkdir(parents=True, exist_ok=True)
        context = payload.get('context', {})
        code = '\n\n'.join(c['text'] for c in context.get('content', []) if c['type'] == 'text')
        # Missing assets remain explicit; never fabricate files or local proof.
        urls = sorted(set(re.findall(r'https://www\.figma\.com/api/mcp/asset/[^\s"`<>]+', code)))
        missing = []
        for url in urls:
            identifier = hashlib.sha256(url.encode()).hexdigest()
            code = code.replace(url, 'assets-pending/' + identifier)
            missing.append({'url_sha256': identifier, 'status': 'not-downloaded'})
        (folder / 'design-context.md').write_text(code + '\n', encoding='utf-8', newline='\n')
        images = [c for c in context.get('content', []) if c['type'] == 'image']
        if images:
            (folder / 'screenshot.png').write_bytes(base64.b64decode(images[0]['data']))
        if not (folder / 'metadata.json').exists():
            dump(folder / 'metadata.json', {'capture_schema_version': 1, 'dataset_version': VERSION,
                 'file_key': payload['file_key'], 'node_id': node['id'], 'frame_name': node['name'],
                 'node_type': node['type'], 'natural_width': node['width'], 'natural_height': node['height'],
                 'page_id': node['page_id'], 'captured_at': STAMP, 'status': 'partial-content',
                 'context_kind': 'sparse-metadata', 'truncation_handled': False,
                 'missing_reason': 'HTTP asset download or screenshot unavailable; MCP quota blocks further capture'})
        dump(folder / 'pending-assets.json', {'status': 'not-downloaded', 'assets': missing})
        path.unlink()  # exact ignored scratch file, never a recursive deletion


def finalize_manifest():
    request = json.loads((DATASET / 'capture-request.json').read_text(encoding='utf-8'))
    nodes = {}
    for node in request['targets']:
        folder = DATASET / 'nodes' / node['id'].replace(':', '-')
        metadata = json.loads((folder / 'metadata.json').read_text(encoding='utf-8')) if (folder / 'metadata.json').exists() else None
        present = sorted(p.name for p in folder.iterdir() if p.is_file()) if folder.exists() else []
        nodes[node['id']] = {'file_key': request['file_key'], 'frame_name': node['name'], 'node_type': node['type'],
                            'page_id': node['page_id'], 'status': 'pending-rate-limit',
                            'snapshot_dir': folder.relative_to(DATASET).as_posix() if folder.exists() else None,
                            'captured_files': present, 'missing_reason': request['blocker'],
                            'truncation': metadata.get('truncation') if metadata else None,
                            'truncation_handled': metadata.get('truncation_handled', False) if metadata else False}
    use_cases = {}
    for index, node_id in enumerate(request['primary_nodes']):
        use_cases[f'UC-{index+1:03d}'] = {'node_id': node_id, 'status': 'pending-rate-limit',
            'source_uc': 'docs/01-inception/use-cases/' + request['uc_files'][index],
            'supplementary_node_ids': [n['id'] for n in request['targets'] if n['id'] != node_id]}
    manifest = {'dataset_id': VERSION, 'dataset_version': VERSION, 'project_id': '100ms-video-conferencing',
                'created_at': STAMP, 'overall_status': 'pending-rate-limit', 'frozen': False,
                'page_inventory_path': 'docs/00-context/sources/100ms-figma-page-inventory.json',
                'page_count': 69, 'complete_nodes': 0, 'pending_nodes': len(nodes),
                'payload_nodes': sum(bool(n['captured_files']) for n in nodes.values()),
                'blocker': request['blocker'], 'use_cases': use_cases, 'nodes': nodes}
    dump(DATASET / 'manifest.json', manifest)
    files = sorted(p for p in DATASET.rglob('*') if p.is_file() and p.name != 'checksums.sha256')
    (DATASET / 'checksums.sha256').write_text('\n'.join(
        f'{sha(p)[7:]}  {p.relative_to(DATASET).as_posix()}' for p in files) + '\n', encoding='utf-8', newline='\n')
    return manifest


def source_baseline():
    archive = ROOT / '.codex/skills/restore-source-baseline/assets/source-baseline.zip'
    if archive.exists():
        raise ValueError('Source ZIP already exists; do not overwrite a pinned baseline')
    files = sorted(p for part in ('be', 'fe') for p in (ROOT / 'finalsource' / part / 'src').rglob('*') if p.is_file())
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as output:
        for folder in ['baseline/', 'baseline/be/', 'baseline/be/src/', 'baseline/fe/', 'baseline/fe/src/']:
            output.writestr(zipfile.ZipInfo(folder, (1980, 1, 1, 0, 0, 0)), b'')
        for path in files:
            name = 'baseline/' + path.relative_to(ROOT / 'finalsource').as_posix()
            entry = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            output.writestr(entry, path.read_bytes())
    with zipfile.ZipFile(archive) as saved:
        entries = {name for name in saved.namelist() if not name.endswith('/')}
        expected = {'baseline/' + p.relative_to(ROOT / 'finalsource').as_posix() for p in files}
        assert entries == expected
        for path in files:
            name = 'baseline/' + path.relative_to(ROOT / 'finalsource').as_posix()
            assert saved.read(name) == path.read_bytes()
    dump(ROOT / 'docs/00-context/sources/100ms-source-baseline.json', {
        'artifact_type': 'clean-source-baseline', 'project_id': '100ms-video-conferencing', 'created_at': STAMP,
        'zip_path': relative(archive), 'zip_sha256': sha(archive), 'database_status': 'deferred-by-researcher',
        'files': [{'path': relative(p), 'archive_entry': 'baseline/' + p.relative_to(ROOT / 'finalsource').as_posix(),
                   'sha256': sha(p)} for p in files]})
    return sha(archive), len(files)


if __name__ == '__main__':
    retain_partial_payloads()
    manifest = finalize_manifest()
    checksum, file_count = source_baseline()
    profile_path = ROOT / 'PROJECT_PROFILE.json'
    profile = json.loads(profile_path.read_text(encoding='utf-8'))
    profile['clean_source_baseline_sha256'] = checksum
    profile['setup_status'] = 'figma-blocked; database-deferred'
    profile['design_dataset_preparation'] = {'dataset_version': VERSION, 'status': 'pending-rate-limit',
        'manifest_path': relative(DATASET / 'manifest.json'), 'manifest_sha256': sha(DATASET / 'manifest.json')}
    dump(profile_path, profile)
    for name in ['docs/00-context/FIGMA-LINK-REVIEW.md', 'docs/00-context/sources/CONNECTED-SOURCES.md']:
        p = ROOT / name
        p.write_text(p.read_text(encoding='utf-8').rstrip() + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({'baseline_sha256': checksum, 'baseline_files': file_count,
                      'figma_payload_nodes': manifest['payload_nodes'], 'figma_status': manifest['overall_status']}))
