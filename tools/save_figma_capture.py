"""Persist one Figma MCP capture, localize URLs and deduplicate bitmap/SVG assets."""
import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import threading
import urllib.request
import struct
import zlib
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
LOCK = threading.Lock()


def validate_asset(content):
    if content.startswith(b'\x89PNG\r\n\x1a\n'):
        offset, pixels, ended = 8, False, False
        while offset + 12 <= len(content):
            size = struct.unpack('>I', content[offset:offset + 4])[0]
            kind = content[offset + 4:offset + 8]
            end = offset + 12 + size
            if end > len(content):
                raise ValueError('Truncated PNG chunk')
            chunk = content[offset + 4:offset + 8 + size]
            crc = struct.unpack('>I', content[offset + 8 + size:end])[0]
            if zlib.crc32(chunk) & 0xffffffff != crc:
                raise ValueError('Invalid PNG checksum')
            pixels |= kind == b'IDAT' and size > 0
            ended |= kind == b'IEND'
            offset = end
        if not pixels or not ended:
            raise ValueError('PNG lacks pixel data or end marker')
    elif content.startswith(b'\xff\xd8'):
        if not content.rstrip().endswith(b'\xff\xd9'):
            raise ValueError('Truncated JPEG')
    elif b'<svg' in content[:1024]:
        if not ET.fromstring(content).tag.endswith('svg'):
            raise ValueError('Invalid SVG root')
    elif content.startswith((b'GIF87a', b'GIF89a')):
        if not content.endswith(b';'):
            raise ValueError('Truncated GIF')
    elif content.startswith(b'RIFF') and content[8:12] == b'WEBP':
        if struct.unpack('<I', content[4:8])[0] + 8 != len(content):
            raise ValueError('Truncated WebP')
    else:
        raise ValueError('Unsupported or invalid image payload')


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def texts(result):
    return '\n\n'.join(c['text'] for c in result.get('content', []) if c['type'] == 'text')


def downloaded_json(result):
    for item in result.get('content', []):
        if item['type'] == 'text':
            try:
                value = json.loads(item['text'])
                if isinstance(value, dict) and 'export' in value:
                    return value
            except json.JSONDecodeError:
                pass
    raise ValueError('Download response missing structured asset inventory')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('payload')
    parser.add_argument('--asset-only', action='store_true')
    args = parser.parse_args()
    payload_path = Path(args.payload).resolve()
    if not payload_path.is_relative_to((ROOT / '.tmp').resolve()):
        raise ValueError('Payload must be an ignored scratch file inside this repository')
    payload = json.loads(payload_path.read_text(encoding='utf-8'))
    version = payload['dataset_version']
    if not re.fullmatch(r'[A-Za-z0-9._-]+', version):
        raise ValueError('Unsafe version')
    dataset = ROOT / 'resource/figma-design-dataset' / version
    manifest = dataset / 'manifest.json'
    if (dataset / 'FROZEN.json').exists() or (manifest.exists() and json.loads(manifest.read_text(encoding='utf-8')).get('frozen')):
        raise ValueError('Cannot mutate frozen dataset')
    node = payload['node']
    slug = hashlib.sha256(node['id'].encode()).hexdigest()[:16] if not re.fullmatch(r'\d+:\d+', node['id']) else node['id'].replace(':', '-')
    folder = dataset / ('asset-captures' if args.asset_only else 'nodes') / slug
    folder.mkdir(parents=True, exist_ok=True)
    assets = downloaded_json(payload['download'])
    code = texts(payload.get('context', {}))
    sparse = code.lstrip().startswith(('<section ', '<frame ', '<group ', '<component', '<instance ', '<canvas '))
    prefix = re.search(r'const assetPathPrefix = "([^"\n]+)";', code)
    urls = {}
    if prefix:
        for name in re.findall(r'\$\{assetPathPrefix\}/([A-Za-z0-9._-]+\.(?:svg|png|jpe?g|webp|gif))', code):
            urls[prefix.group(1) + '/' + name] = name
    for url in re.findall(r'https://www\.figma\.com/api/mcp/asset/[^\s"`<>]+', code):
        if not prefix or url != prefix.group(1):
            urls[url] = url.rsplit('/', 1)[-1]
    for item in assets.get('rawImages', []) + assets.get('svgAssets', []):
        urls[item['url']] = hashlib.sha256(item['url'].encode()).hexdigest()

    def fetch(url):
        if not url.startswith('https://www.figma.com/api/mcp/asset/'):
            raise ValueError('Unexpected download origin')
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(request, timeout=90) as response:
            content = response.read()
            mime = response.headers.get_content_type()
        if not content:
            raise ValueError('Empty asset')
        validate_asset(content)
        return content, mime

    def save_asset(url):
        content, mime = fetch(url)
        digest = hashlib.sha256(content).hexdigest()
        extension = {'image/png': '.png', 'image/jpeg': '.jpg', 'image/svg+xml': '.svg',
                     'image/webp': '.webp', 'image/gif': '.gif'}.get(mime, '.bin')
        if content.startswith(b'\x89PNG'): extension = '.png'
        elif content.startswith(b'\xff\xd8'): extension = '.jpg'
        elif b'<svg' in content[:1024]: extension = '.svg'
        target = dataset / 'assets' / (digest + extension)
        with LOCK:
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists(): target.write_bytes(content)
        return url, {'identifier': urls[url], 'url_sha256': hashlib.sha256(url.encode()).hexdigest(),
                     'local_path': '../../assets/' + target.name, 'mime_type': mime,
                     'byte_size': len(content), 'sha256': 'sha256:' + digest}

    failures = []
    mapping = {}
    def capture_asset(url):
        try:
            return save_asset(url)
        except Exception as error:
            reason = str(error) if isinstance(error, ValueError) else 'sanitized download failure'
            return url, {'identifier': urls[url], 'url_sha256': hashlib.sha256(url.encode()).hexdigest(),
                         'status': 'not-downloaded', 'error_type': type(error).__name__, 'reason': reason}
    with ThreadPoolExecutor(max_workers=12) as pool:
        for url, info in pool.map(capture_asset, urls):
            mapping[url] = info
            if info.get('status') == 'not-downloaded':
                failures.append(info)
    try:
        export, _ = fetch(assets['export']['url'])
        if not export.startswith(b'\x89PNG'):
            raise ValueError('Node export is not PNG')
        (folder / 'export.png').write_bytes(export)
    except Exception as error:
        failures.append({'identifier': 'node-export', 'status': 'not-downloaded',
                         'error_type': type(error).__name__, 'reason': str(error) if isinstance(error, ValueError) else 'sanitized download failure'})
    if not args.asset_only:
        images = [c for c in payload['context'].get('content', []) if c['type'] == 'image']
        if images:
            screenshot = base64.b64decode(images[0]['data'])
        elif payload.get('screenshot'):
            screenshot_data = json.loads(payload['screenshot']['content'][0]['text'])
            screenshot, _ = fetch(screenshot_data['image_url'])
        else:
            screenshot = None
            failures.append({'identifier': 'screenshot', 'status': 'not-downloaded', 'reason': 'Design context has no screenshot'})
        if screenshot:
            validate_asset(screenshot)
            (folder / 'screenshot.png').write_bytes(screenshot)
        for info in mapping.values():
            if 'local_path' not in info:
                info['local_path'] = 'assets-pending/' + info['url_sha256']
        if prefix:
            code = re.sub(r'`\$\{assetPathPrefix\}/([A-Za-z0-9._-]+\.(?:svg|png|jpe?g|webp|gif))`',
                          lambda m: json.dumps(mapping[prefix.group(1) + '/' + m.group(1)]['local_path']), code)
            code = code.replace(prefix.group(1), '../../assets')
        for url, info in mapping.items():
            code = code.replace(url, info['local_path'])
        if 'https://www.figma.com/api/mcp/asset/' in code:
            raise ValueError('Unlocalized temporary asset reference')
        (folder / 'design-context.md').write_text(code + '\n', encoding='utf-8', newline='\n')
    flags = {'rawImagesTruncated': assets.get('rawImagesTruncated', False),
             'svgAssetsTruncated': assets.get('svgAssetsTruncated', False)}
    metadata = {'capture_schema_version': 1, 'dataset_version': version,
                'file_key': payload['file_key'], 'node_id': node['id'], 'frame_name': node['name'],
                'node_type': node['type'], 'natural_width': node['width'], 'natural_height': node['height'],
                'page_id': node['page_id'], 'captured_at': datetime.now(timezone.utc).isoformat(),
                'client_frameworks': 'react', 'client_languages': 'typescript,html,css',
                'code_connect_status': 'default-tool-request; no mapping status supplied',
                'context_kind': 'sparse-metadata' if sparse else 'reference-code-and-instructions',
                'context_characters': len(code),
                'truncation': flags, 'truncation_handled': not any(flags.values()),
                'status': 'partial-content' if any(flags.values()) or failures or sparse else 'complete',
                'download_failures': len(failures),
                'raw_image_count': len(assets.get('rawImages', [])), 'svg_asset_count': len(assets.get('svgAssets', []))}
    dump(folder / 'metadata.json', metadata)
    dump(folder / 'asset-map.json', {'assets': list(mapping.values()), 'truncation': flags})
    if failures:
        dump(folder / 'pending-assets.json', {'status': 'not-downloaded', 'assets': failures})
    dump(folder / 'assets/index.json', {'canonical_asset_directory': '../../assets', 'count': len(mapping)})
    payload_path.unlink()
    print(json.dumps({'node_id': node['id'], 'status': metadata['status'], 'assets': len(mapping),
                      'snapshot_dir': folder.relative_to(dataset).as_posix(), 'truncation': flags}))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        # Network exceptions can contain short-lived URLs; never print them.
        print(json.dumps({'status': 'capture-save-failed', 'error_type': type(error).__name__,
                          'reason': str(error) if isinstance(error, ValueError) else 'sanitized download/write failure'}))
        raise SystemExit(1)
