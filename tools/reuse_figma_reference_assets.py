"""Recover identical cached reference assets for one explicitly selected dataset pair."""
import hashlib
import json
from pathlib import Path
import re
from save_figma_capture import ROOT, dump, validate_asset


def normalized(context, mapping):
    for asset in mapping['assets']:
        context = context.replace(asset.get('local_path','UNUSED'), 'ASSET:' + asset['identifier'])
    return context


def main():
    parent = ROOT / 'resource/figma-design-dataset'
    old, new = parent / '100ms-2026-10-01-001', parent / '100ms-2026-10-02-001'
    assert not (new / 'FROZEN.json').exists()
    if (new / 'manifest.json').exists():
        assert not json.loads((new / 'manifest.json').read_text(encoding='utf-8')).get('frozen')
    request = json.loads((new / 'capture-request.json').read_text(encoding='utf-8'))
    recovered = []
    for identifier in request['primary_nodes']:
        folder = new / 'nodes' / identifier.replace(':','-')
        source = old / 'nodes' / identifier.replace(':','-')
        mapping = json.loads((folder / 'asset-map.json').read_text(encoding='utf-8'))
        context = (folder / 'design-context.md').read_text(encoding='utf-8')
        previous = json.loads((source / 'asset-map.json').read_text(encoding='utf-8'))
        previous_code = (source / 'design-context.md').read_text(encoding='utf-8')
        # Identical code/asset identities is mandatory, not visual similarity.
        if normalized(context,mapping) != normalized(previous_code,previous):
            continue
        lookup = {a['identifier']:a for a in previous['assets'] if not a.get('status')}
        count = 0
        for index, asset in enumerate(mapping['assets']):
            if asset.get('status') != 'not-downloaded' or asset['identifier'] not in lookup:
                continue
            cached = lookup[asset['identifier']]
            path = (source / cached['local_path']).resolve()
            assert path.is_relative_to(old.resolve())
            content = path.read_bytes()
            digest = hashlib.sha256(content).hexdigest()
            assert cached['sha256'] == 'sha256:' + digest and len(content) == cached['byte_size']
            try:
                validate_asset(content)
            except ValueError:
                continue
            target = new / 'assets' / path.name
            if not target.exists():
                target.write_bytes(content)
            context = context.replace(asset['local_path'],cached['local_path'])
            mapping['assets'][index] = {**cached,'reuse_origin_dataset':old.name,
                'reuse_proof':'identical normalized reference code and asset identifier; source bytes verified by SHA-256',
                'current_failed_request_url_sha256':asset.get('url_sha256')}
            count += 1
        if count:
            dump(folder / 'asset-map.json',mapping)
            (folder / 'design-context.md').write_text(context,encoding='utf-8',newline='\n')
            metadata = json.loads((folder / 'metadata.json').read_text(encoding='utf-8'))
            metadata['cached_asset_recovery'] = {'source_dataset':old.name,'assets':count,
                'proof':'identical normalized reference code; exact identifier and checksum-verified source bytes'}
            dump(folder / 'metadata.json',metadata)
            recovered.append({'node_id':identifier,'assets':count})
    print(json.dumps({'recovered':recovered}))


if __name__ == '__main__':
    main()
