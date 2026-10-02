"""Build only synchronous capture exports from pinned upstream fflate, in ignored scratch."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def member(package, version, name):
    meta = json.load(urllib.request.urlopen(f'https://registry.npmjs.org/{package}/{version}'))
    data = urllib.request.urlopen(meta['dist']['tarball']).read()
    assert hashlib.sha1(data).hexdigest() == meta['dist']['shasum']
    with tarfile.open(fileobj=io.BytesIO(data),mode='r:gz') as archive:
        return archive.extractfile(name).read()


def main():
    scratch = ROOT / '.tmp/figma-capture-build'
    scratch.mkdir(parents=True,exist_ok=True)
    executable = scratch / 'esbuild.exe'
    executable.write_bytes(member('@esbuild/win32-x64','0.25.0','package/esbuild.exe'))
    (scratch / 'fflate-browser.js').write_bytes(member('fflate','0.8.2','package/esm/browser.js'))
    entry = scratch / 'entry.js'
    entry.write_text('export {zlibSync,strToU8} from "./fflate-browser.js";\n',encoding='utf-8')
    target = ROOT / 'tools/vendor/fflate/capture.min.js'
    subprocess.run([str(executable),str(entry),'--bundle','--platform=browser','--minify',
                    '--format=iife','--global-name=fflate','--outfile='+str(target)],check=True)
    receipt = ROOT / 'tools/vendor/fflate/PROVENANCE.json'
    data = json.loads(receipt.read_text(encoding='utf-8'))
    data['capture_bundle'] = {'path':'capture.min.js','exports':['zlibSync','strToU8'],
        'build_tool':'esbuild@0.25.0 (Windows x64)',
        'sha256':'sha256:' + hashlib.sha256(target.read_bytes()).hexdigest()}
    receipt.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'capture_bundle_bytes':target.stat().st_size}))


if __name__ == '__main__':
    main()
