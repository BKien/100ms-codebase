"""Validate and freeze an explicit desktop-only Figma dataset."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import re
from save_figma_capture import ROOT, dump, validate_asset

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def finalize(version):
    assert re.fullmatch(r'[A-Za-z0-9._-]+',version)
    dataset = ROOT / 'resource/figma-design-dataset' / version
    manifest_path = dataset / 'manifest.json'
    assert not (dataset/'FROZEN.json').exists()
    assert not (manifest_path.exists() and read(manifest_path).get('frozen'))
    request = read(dataset/'capture-request.json')
    coverage = read(dataset/request['coverage_path'])
    assert request['dataset_version'] == coverage['dataset_version'] == version
    assert request['platforms'] == ['desktop'] and request['excluded_platforms'] == ['mobile']
    review = ROOT/'docs/00-context/FIGMA-LINK-REVIEW.md'
    approved = {a+':'+b for a,b in re.findall(r'node-id=(\d+)-(\d+)',review.read_text(encoding='utf-8'))}
    targets = {n['id']:n for n in request['targets']}
    assert len(targets) == len(request['targets']) == 74 and set(targets).issubset(approved)
    assert all('Desktop' in n['page_name'] or i in {'6045:42131','6073:21769'} for i,n in targets.items())
    checked = {}
    nodes = {}
    for identifier,target in targets.items():
        folder = dataset/'nodes'/identifier.replace(':','-')
        metadata = read(folder/'metadata.json') if (folder/'metadata.json').exists() else {}
        issues = []
        for name in ('design-context.md','metadata.json','screenshot.png','asset-map.json','assets/index.json','native-design.json'):
            if not (folder/name).is_file() or not (folder/name).stat().st_size:
                issues.append('missing:'+name)
        if metadata:
            assert (metadata['dataset_version'],metadata['file_key'],metadata['node_id']) == (version,request['file_key'],identifier)
            assert (metadata['page_id'],metadata['frame_name'],metadata['node_type']) == (target['page_id'],target['name'],target['type'])
            if metadata.get('native_failures') or not metadata.get('truncation_handled'):
                issues.append('native-subtree-or-assets-incomplete')
            if metadata.get('required_download_failures'):
                issues.append('required-reference-assets-missing')
            if identifier in request['primary_nodes']:
                if not metadata.get('context_kind','').startswith('reference-code'):
                    issues.append('primary-reference-code-missing')
            elif metadata.get('screenshot_node_id') != identifier:
                issues.append('unbound-screenshot')
        for name in ('screenshot.png','export.png'):
            if (folder/name).exists():
                try:
                    validate_asset((folder/name).read_bytes())
                except (ValueError,AssertionError):
                    issues.append('invalid:'+name)
        context = (folder/'design-context.md').read_text(encoding='utf-8') if (folder/'design-context.md').exists() else ''
        if 'assets-pending/' in context:
            issues.append('pending-reference-code-asset')
        available = set()
        if (folder/'asset-map.json').exists():
            for asset in read(folder/'asset-map.json')['assets']:
                if asset.get('status') == 'not-downloaded' or not asset.get('local_path'):
                    issues.append('missing-asset:'+asset['identifier'])
                    continue
                path = (folder/asset['local_path']).resolve()
                assert path.is_relative_to(dataset.resolve())
                key = (str(path),asset['sha256'],asset['byte_size'])
                if key not in checked:
                    valid = path.is_file() and path.stat().st_size == asset['byte_size'] and 'sha256:'+sha(path) == asset['sha256']
                    if valid:
                        try:
                            validate_asset(path.read_bytes())
                        except (ValueError,AssertionError):
                            valid = False
                    checked[key] = valid
                if not checked[key]:
                    issues.append('invalid-asset:'+asset['identifier'])
                else:
                    available.add(asset['identifier'])
        if (folder/'native-design.json').exists():
            native = read(folder/'native-design.json')
            assert native['node_id'] == native['tree']['id'] == identifier
            assert native['file_key'] == request['file_key'] and native['page_id'] == target['page_id']
            if native['failures'] or not set(native['asset_identifiers']).issubset(available):
                issues.append('native-assets-incomplete')
        for local in set(re.findall(r'\.\./\.\./assets/[A-Za-z0-9._-]+',context)):
            if not (folder/local).is_file():
                issues.append('broken-local-reference:'+local)
        nodes[identifier] = {
            'file_key':request['file_key'],'frame_name':target['name'],'node_type':target['type'],
            'page_id':target['page_id'],'page_name':target['page_name'],
            'status':'partial-content' if issues else 'complete','snapshot_dir':folder.relative_to(dataset).as_posix(),
            'missing_reasons':issues,'context_kind':metadata.get('context_kind'),
            'truncation':metadata.get('truncation',{}),'truncation_handled':metadata.get('truncation_handled',False),
            'captured_files':sorted(p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file())}
    use_cases = {}
    assert len(coverage['use_cases']) == 18
    for uc_id,entry in coverage['use_cases'].items():
        assert 'sha256:'+sha(ROOT/entry['source_uc']) == entry['source_uc_sha256']
        required = entry['required_node_ids']
        assert entry['primary_node_id'] in required and set(required).issubset(nodes)
        use_cases[uc_id] = {
            'node_id':entry['primary_node_id'],'required_node_ids':required,
            'supplementary_node_ids':[i for i in required if i != entry['primary_node_id']],
            'status':'complete' if all(nodes[i]['status']=='complete' for i in required) else 'partial-content',
            'platforms':['desktop'],'excluded_platforms':['mobile'],
            'source_uc':entry['source_uc'],'source_uc_sha256':entry['source_uc_sha256'],
            'design_limitations':entry['design_limitations']}
    assert set(targets) == {i for e in use_cases.values() for i in e['required_node_ids']}
    complete = sum(n['status']=='complete' for n in nodes.values())
    ready = complete == len(nodes) and all(e['status']=='complete' for e in use_cases.values())
    for path in dataset.rglob('*'):
        if path.is_file() and path.suffix in {'.md','.json'}:
            assert 'https://www.figma.com/api/mcp/asset/' not in path.read_text(encoding='utf-8'), 'Temporary URL in saved artifact'
    manifest = {
        'dataset_id':version,'dataset_version':version,'project_id':'100ms-video-conferencing',
        'created_at':datetime.now(timezone.utc).isoformat(),'derived_from_dataset':request['derived_from_dataset'],
        'overall_status':'complete' if ready else 'partial-content','frozen':ready,
        'scope':request['scope'],'platforms':['desktop'],'excluded_platforms':['mobile'],
        'coverage_path':request['coverage_path'],'mapping_authority_path':'docs/00-context/FIGMA-LINK-REVIEW.md',
        'mapping_authority_sha256':'sha256:'+sha(review),
        'page_inventory_path':'docs/00-context/sources/100ms-figma-page-inventory.json',
        'page_count':len({n['page_id'] for n in targets.values()}),'discovery_page_count':69,
        'discovery_target_count':request['discovery_target_count'],'excluded_target_count':request['excluded_target_count'],
        'complete_nodes':complete,'pending_nodes':len(nodes)-complete,'payload_nodes':len(nodes),
        'retained_nonrequired_node_count':len([d for d in (dataset/'nodes').iterdir() if d.is_dir() and d.name.replace('-',':') not in targets]),
        'retention_note':'Nonrequired captures, including earlier mobile evidence, are historical only and never returned by desktop UC resolution.',
        'export_policy':'Existing export.png retained; native captures require one whole-node screenshot without redundant PNG export.',
        'blocker':None if ready else 'See required node missing_reasons','use_cases':use_cases,'nodes':nodes}
    dump(manifest_path,manifest)
    ledger = dataset/'checksums.sha256'
    files = sorted(p for p in dataset.rglob('*') if p.is_file() and p != ledger)
    ledger.write_text('\n'.join(f'{sha(p)}  {p.relative_to(dataset).as_posix()}' for p in files)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'dataset_version':version,'status':manifest['overall_status'],'complete_nodes':complete,
        'pending_nodes':len(nodes)-complete,'complete_use_cases':sum(e['status']=='complete' for e in use_cases.values()),
        'files':len(files),'verified_asset_records':len(checked),'manifest_sha256':'sha256:'+sha(manifest_path),
        'issues':{i:n['missing_reasons'] for i,n in nodes.items() if n['missing_reasons']}}))
    return 0 if ready else 3

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset-version',required=True)
    raise SystemExit(finalize(parser.parse_args().dataset_version))
