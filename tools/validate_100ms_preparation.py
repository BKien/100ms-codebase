"""Read-only structural/checksum validation of prepared 100ms research inputs."""
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return 'sha256:' + hashlib.sha256(path.read_bytes()).hexdigest()


def metadata(text):
    match = re.match(r'^---\n(.*?)\n---\n', text.replace('\r\n', '\n'), re.S)
    assert match, 'Front matter missing'
    return dict(re.findall(r'^([a-z_]+):\s*(.+)$', match.group(1), re.M))


def section(text, heading):
    match = re.search(r'^### ' + re.escape(heading) + r'\s*\n(.*?)(?=^###? |\Z)', text, re.M | re.S)
    return match.group(1).strip() if match else ''


def validate():
    archive = json.loads((ROOT / 'archive/financial-management/pre-100ms-2026-10-01/archive-manifest.json').read_text(encoding='utf-8'))
    for item in archive['files']:
        assert sha(ROOT / item['archive_path']) == item['sha256'], 'Archived evidence checksum mismatch'
    profile = json.loads((ROOT / 'PROJECT_PROFILE.json').read_text(encoding='utf-8'))
    receipt_path = profile['authoritative_sources']['use_case_specification']['retrieval_receipt']
    receipt = json.loads((ROOT / receipt_path).read_text(encoding='utf-8'))
    for item in receipt['sources']:
        assert sha(ROOT / item['snapshot_path']) == item['sha256'], item['snapshot_path']
    inventory = []
    all_api_ids = set()
    for item in receipt['projections']:
        path = ROOT / item['projection_path']
        assert sha(path) == item['projection_sha256'], item['projection_path']
        text = path.read_text(encoding='utf-8')
        fields = metadata(text)
        assert fields['status'] == 'Frozen'
        assert fields['source_type'] == 'local-markdown'
        assert 'source_spreadsheet_id' not in fields
        original = (ROOT / item['source_snapshot_path']).read_text(encoding='utf-8-sig').replace('\r\n', '\n')
        if 'uc_id' in fields:
            assert re.findall(r'~~~ocl\n(.*?)\n~~~', text, re.S) == re.findall(r'~~~ocl\n(.*?)\n~~~', original, re.S)
            for heading in ['Basic Flow', 'Alternative Flow', 'Exception Flow', 'Related API IDs', 'Related UI']:
                assert section(text, heading) == section(original, heading), (path.name, heading)
            ids = re.findall(r'^-- (BR-[A-Z0-9-]+)\s*$', text, re.M)
            assert len(ids) == len(set(ids)), path.name
            assert len(re.findall(r'^```plantuml$', text, re.M)) == 1
            assert 'shared-domain-model' not in text
            api_ids = list(dict.fromkeys(re.findall(r'\bAPI-[A-Z0-9]+(?:-[A-Z0-9]+)*\b', section(text, 'Related API IDs'))))
            inventory.append({'uc_id': fields['uc_id'], 'path': item['projection_path'], 'sha256': sha(path),
                              'ordered_rule_ids': ids, 'ordered_api_ids': api_ids,
                              'flow_sections': {'basic': bool(section(text, 'Basic Flow')),
                                               'alternative_ids': re.findall(r'(?m)^AF-\d+:', section(text, 'Alternative Flow')),
                                               'exception_ids': re.findall(r'(?m)^EF-\d+:', section(text, 'Exception Flow'))}})
        if 'api_id' in fields:
            assert fields['api_id'] not in all_api_ids
            all_api_ids.add(fields['api_id'])
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if '://' in target or target.startswith('#'):
                continue
            relative_target = target.split('#')[0]
            if relative_target:
                assert (path.parent / relative_target).exists(), f'{path.name}: missing link {relative_target}'
    assert len(inventory) == 18 and len(all_api_ids) == 15
    for item in inventory:
        assert set(item['ordered_api_ids']).issubset(all_api_ids), item['uc_id']
    uc_paths = {item['path'] for item in inventory}
    actual_uc_paths = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'docs/01-inception/use-cases').glob('uc-*.md')}
    assert uc_paths == actual_uc_paths
    baseline = ROOT / '.codex/skills/restore-source-baseline/assets/source-baseline.zip'
    assert sha(baseline) == profile['clean_source_baseline_sha256']
    with zipfile.ZipFile(baseline) as saved:
        files = {name: saved.read(name) for name in saved.namelist() if not name.endswith('/')}
        expected = {'baseline/' + p.relative_to(ROOT / 'finalsource').as_posix(): p.read_bytes()
                    for part in ('be', 'fe') for p in (ROOT / 'finalsource' / part / 'src').rglob('*') if p.is_file()}
        assert files == expected
        assert all(name.startswith(('baseline/be/src/', 'baseline/fe/src/')) for name in files)
    pages = json.loads((ROOT / 'docs/00-context/sources/100ms-figma-page-inventory.json').read_text(encoding='utf-8'))
    assert pages['page_count'] == len(pages['pages']) == 69
    root_ids = {n['id'] for p in pages['pages'] for n in p['rootFrames'] if re.fullmatch(r'\d+:\d+', n['id'])}
    for url in profile['authoritative_sources']['figma']['root_node_urls']:
        identifier = re.search(r'node-id=(\d+)-(\d+)', url)
        assert identifier and ':'.join(identifier.groups()) in root_ids
    database = profile['database_preparation']
    if database['status'] == 'prepared':
        prepared = json.loads((ROOT / database['baseline_receipt']).read_text(encoding='utf-8'))
        assert prepared['database_baseline'] == database['database_baseline']
        assert prepared['validation']['status'] == 'PASS'
        assert sha(ROOT / 'docs/00-context/engineering/schema.dbml') == prepared['database_baseline']['dbml_sha256']
        adaptation = json.loads((ROOT / prepared['source_adaptation_path']).read_text(encoding='utf-8'))
        assert sha(ROOT / adaptation['migration_path']) == adaptation['migration_sha256']
        assert adaptation['migration_head'] == prepared['database_baseline']['migration_head']
    else:
        assert database['status'] in {'deferred-by-researcher', 'prepared-not-applied'}
        if database['status'] == 'deferred-by-researcher':
            assert not (ROOT / 'docs/00-context/engineering/schema.dbml').exists(), 'Deferred database must not expose Financial schema'
    print(json.dumps({'status': 'structural-validation-pass', 'uc_count': 18, 'api_count': 15,
                      'business_rule_count': sum(len(i['ordered_rule_ids']) for i in inventory),
                      'source_documents': len(receipt['sources']), 'projection_count': len(receipt['projections']),
                      'figma_pages': 69, 'baseline_files': len(files), 'archive_files_verified': len(archive['files']),
                      'database': database['status'],
                      'generation_ready': False}, indent=2))
    return inventory


if __name__ == '__main__':
    validate()
