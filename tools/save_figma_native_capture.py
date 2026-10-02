"""Save an explicit read-only native Figma batch; preserve primary reference code."""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import zlib
import urllib.request
import time

from save_figma_capture import ROOT, dump, validate_asset


def descendants(node):
    yield node
    for child in node.get('children', []):
        yield from descendants(child)


def decode_native(result):
    envelopes = [json.loads(c['text']) for c in result['content'] if c['type'] == 'text']
    envelope = envelopes[0]
    assert envelope.get('codec') == 'zlib-utf8-v1', 'Incomplete or unsupported native payload'
    assert len(envelopes) == envelope['chunk_count'], 'Missing native capture chunks'
    assert [e['chunk_index'] for e in envelopes] == list(range(len(envelopes)))
    for e in envelopes:
        assert all(e[key] == envelope[key] for key in (
            'codec','uncompressed_bytes','chunk_count','total_encoded_characters','content_adler32')), 'Native capture drift between chunks'
    encoded = ''.join(e['encoded'] for e in envelopes)
    assert len(encoded) == envelope['total_encoded_characters']
    binary = base64.b64decode(encoded, validate=True)
    output = zlib.decompress(binary)
    assert len(output) == envelope['uncompressed_bytes'], 'Native payload size mismatch'
    data = json.loads(output.decode('utf-8'))
    data['screenshot_node_ids'] = [e['screenshot_node_id'] for e in envelopes if e.get('screenshot_node_id')]
    return data


def save(payload_path):
    payload_path = payload_path.resolve()
    assert payload_path.is_relative_to((ROOT / '.tmp').resolve())
    payload = json.loads(payload_path.read_text(encoding='utf-8'))
    version = payload['dataset_version']
    assert re.fullmatch(r'[A-Za-z0-9._-]+', version)
    dataset = ROOT / 'resource/figma-design-dataset' / version
    assert not (dataset / 'FROZEN.json').exists()
    if (dataset / 'manifest.json').exists():
        assert not json.loads((dataset / 'manifest.json').read_text(encoding='utf-8')).get('frozen')
    result = payload['result']
    assert not result.get('isError'), 'Native connector rejected capture'
    data = decode_native(result)
    images = iter(c for c in result['content'] if c['type'] == 'image')
    assert [n['id'] for n in data['nodes']] == [n['id'] for n in payload['targets']]
    expected_shots = [n['id'] for n in data['nodes'] if n['screenshot_requested']]
    assert data['screenshot_node_ids'] == expected_shots, 'Screenshot/node binding mismatch'
    assert sum(c['type'] == 'image' for c in result['content']) == len(expected_shots), 'Missing native renders'
    saved_assets = {}
    asset_failures = {}
    for asset in data['assets']:
        try:
            if asset.get('cached_sha256'):
                assert re.fullmatch(r'[0-9a-f]{64}',asset['cached_sha256'])
                matches = list((dataset / 'assets').glob(asset['cached_sha256'] + '.*'))
                assert len(matches) == 1, 'Cache asset missing or ambiguous'
                content = matches[0].read_bytes()
            else:
                content = asset['svg'].encode('utf-8') if 'svg' in asset else base64.b64decode(asset['data'], validate=True)
            validate_asset(content)
            assert not re.search(rb'(?:href|src)=[\"\x27]https?://', content), 'External dependency in SVG'
            digest = hashlib.sha256(content).hexdigest()
            assert digest == asset.get('native_sha256',digest), 'Native asset fingerprint mismatch'
            if b'<svg' in content[:1024]:
                extension, mime = '.svg', 'image/svg+xml'
            elif content.startswith(b'\x89PNG'):
                extension, mime = '.png', 'image/png'
            elif content.startswith(b'\xff\xd8'):
                extension, mime = '.jpg', 'image/jpeg'
            elif content.startswith(b'RIFF'):
                extension, mime = '.webp', 'image/webp'
            else:
                extension, mime = '.gif', 'image/gif'
            path = dataset / 'assets' / (digest + extension)
            path.parent.mkdir(exist_ok=True)
            if not path.exists():
                path.write_bytes(content)
            saved_assets[asset['identifier']] = {
                'identifier':asset['identifier'], 'origin':'native-plugin-api', 'kind':asset['kind'],
                'reused_local_cache':bool(asset.get('cached_sha256')),
                'local_path':'../../assets/' + path.name, 'mime_type':mime,
                'byte_size':len(content), 'sha256':'sha256:' + digest}
        except (ValueError, AssertionError) as error:
            asset_failures[asset['identifier']] = str(error)
    outcomes = []
    for observed, target in zip(data['nodes'], payload['targets']):
        tree = observed['tree']
        assert tree['id'] == target['id'] and tree['name'] == target['name'] and tree['type'] == target['type']
        assert abs(tree['width'] - target['width']) < .01 and abs(tree['height'] - target['height']) < .01
        folder = dataset / 'nodes' / target['id'].replace(':','-')
        folder.mkdir(parents=True, exist_ok=True)
        meta_path = folder / 'metadata.json'
        metadata = json.loads(meta_path.read_text(encoding='utf-8')) if meta_path.exists() else {}
        context_path = folder / 'design-context.md'
        context = context_path.read_text(encoding='utf-8') if context_path.exists() else ''
        has_code = metadata.get('context_kind','').startswith('reference-code') and bool(context)
        required_ids = set()
        for item in descendants(tree):
            if item['type'] in ('VECTOR','BOOLEAN_OPERATION','LINE','ELLIPSE','POLYGON','STAR'):
                if item.get('geometry_kind'):
                    if item['type'] == 'VECTOR':
                        assert item.get('vectorPaths'), 'Missing native vector geometry'
                    if item['type'] == 'BOOLEAN_OPERATION':
                        assert item.get('booleanOperation') and item.get('children'), 'Missing native boolean geometry'
                else:
                    required_ids.add(item.get('geometry_asset_identifier', item['id']))
            for field in ('fills','strokes'):
                for paint in item.get(field, []) if isinstance(item.get(field), list) else []:
                    if paint.get('type') == 'IMAGE' and paint.get('imageHash'):
                        required_ids.add(paint['imageHash'])
                        if paint['imageHash'] in saved_assets:
                            paint['local_asset_path'] = saved_assets[paint['imageHash']]['local_path']
        mapping_path = folder / 'asset-map.json'
        mapping = json.loads(mapping_path.read_text(encoding='utf-8')) if mapping_path.exists() else {'assets':[]}
        previous_assets = mapping['assets']
        excluded = list(mapping.get('excluded_unused_inventory_assets', []))
        required_assets = []
        for asset in previous_assets:
            referenced = bool(asset.get('local_path') and asset['local_path'] in context)
            if asset.get('status') == 'not-downloaded' and not referenced:
                excluded.append({**asset, 'required':False,
                    'exclusion_reason':'Not referenced by saved reference code or complete native subtree; download inventory only'})
            else:
                required_assets.append(asset)
        required_assets.extend(saved_assets[i] for i in sorted(required_ids) if i in saved_assets)
        required_assets = list({(a['identifier'], a.get('local_path')): a for a in required_assets}.values())
        missing = sorted(required_ids - saved_assets.keys())
        failures = observed['failures'] + [
            {'identifier':i,'reason':asset_failures.get(i, 'missing-native-asset')} for i in missing]
        if observed['screenshot_requested']:
            image = next(images)
            content = base64.b64decode(image['data'], validate=True)
            validate_asset(content)
            (folder / 'screenshot.png').write_bytes(content)
            metadata['screenshot_method'] = 'native-node-screenshot'
            metadata['screenshot_scale'] = 1
            metadata['screenshot_node_id'] = target['id']
        elif target['id'] in payload.get('screenshots', {}):
            response = payload['screenshots'][target['id']]
            assert not response.get('isError'), 'Screenshot connector rejected capture'
            render = json.loads(next(c['text'] for c in response['content'] if c['type'] == 'text'))
            assert abs(render['original_width'] - target['width']) < .01
            assert abs(render['original_height'] - target['height']) < .01
            assert render['image_url'].startswith('https://www.figma.com/api/mcp/asset/')
            for attempt in range(12):
                request = urllib.request.Request(render['image_url'], headers={'User-Agent':'curl/8.0'})
                with urllib.request.urlopen(request, timeout=30) as response:
                    content = response.read()
                    pending = response.status == 202
                if not pending:
                    break
                time.sleep(2)
            assert content and not pending, 'Screenshot render still pending'
            validate_asset(content)
            (folder / 'screenshot.png').write_bytes(content)
            metadata['screenshot_method'] = 'get_screenshot-url-download'
            metadata['screenshot_scale'] = render['width'] / target['width']
            metadata['screenshot_node_id'] = target['id']
        assert (folder / 'screenshot.png').is_file()
        dump(folder / 'native-design.json', {
            'schema':'figma-native-subtree-v1','file_key':payload['file_key'],
            'node_id':target['id'],'page_id':target['page_id'],
            'captured_at':datetime.now(timezone.utc).isoformat(), 'tree':tree,
            'descendant_count':sum(1 for _ in descendants(tree)),
            'asset_identifiers':sorted(required_ids), 'failures':failures})
        if not has_code:
            context_path.write_text(
                '# Native Figma design evidence\n\n'
                'Read-only Plugin API capture of this exact approved node. This is design data, not generated reference code.\n\n'
                '- Full descendant hierarchy, dimensions, transforms, auto-layout, paints, effects, text runs and component properties: `native-design.json`.\n'
                '- Whole-node render at natural scale: `screenshot.png`.\n'
                '- Every referenced image paint and vector SVG: `asset-map.json`, with local checksum-addressed files.\n',
                encoding='utf-8', newline='\n')
        metadata.update({
            'capture_schema_version':2,'dataset_version':version,'file_key':payload['file_key'],
            'node_id':target['id'],'frame_name':target['name'],'node_type':target['type'],
            'natural_width':tree['width'],'natural_height':tree['height'],'page_id':target['page_id'],
            'native_captured_at':datetime.now(timezone.utc).isoformat(),
            'context_kind':'reference-code-and-native-subtree' if has_code else 'native-subtree',
            'code_connect_status':metadata.get('code_connect_status','not-requested; native supplemental evidence'),
            'truncation_handled':not failures,
            'truncation_resolution':{'method':'complete-native-subtree-and-referenced-assets',
                'native_asset_count':len(required_ids),'excluded_unused_download_assets':len(excluded)},
            'required_download_failures':sum(a.get('status') == 'not-downloaded' for a in required_assets),
            'native_failures':failures,'status':'partial-content' if failures else 'complete'})
        dump(meta_path, metadata)
        dump(mapping_path, {'assets':required_assets,'excluded_unused_inventory_assets':excluded,
             'truncation':metadata.get('truncation',{}),'native_assets_complete':not failures})
        dump(folder / 'assets/index.json', {'canonical_asset_directory':'../../assets','count':len(required_assets)})
        outcomes.append({'node_id':target['id'],'native_nodes':sum(1 for _ in descendants(tree)),
                         'native_assets':len(required_ids),'status':metadata['status']})
    assert next(images, None) is None, 'Unexpected unmapped screenshots'
    payload_path.unlink()
    print(json.dumps({'saved':outcomes,'asset_failures':len(asset_failures),'batch_failures':len(data['failures'])}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('payload', type=Path)
    save(parser.parse_args().payload)
