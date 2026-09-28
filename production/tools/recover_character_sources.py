"""Recover two explicitly requested existing character sources. No generation or live app access."""
import hashlib
import io
import json
import urllib.parse
import urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
HOST = 'dnznrvs05pmza.cloudfront.net'
EXPECTED = {
    '35c32e2d-2a1d-4f88-9463-c3dc75e2076d': ('art/01-characters/hulk/pose-reviews/hulk-six-pose-v02-source.png',3454219),
    '70752a33-bd71-4481-b558-3f01c87c1a6e': ('art/01-characters/hulk/run-reviews/v01/source-sheet.png',3600366),
}
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise ValueError('Unexpected media redirect; source recovery stopped')

def recover():
    manifest_path = ROOT/'art/character-batch-02.json'
    manifest = json.loads(manifest_path.read_text())
    entries = manifest.get('sources', [])
    if manifest.get('schemaVersion') != 1 or len(entries) != len(EXPECTED):
        raise ValueError('Unexpected source manifest')
    queue_path = ROOT/'art/import-queue.json'
    queue = json.loads(queue_path.read_text())
    if queue.get('schemaVersion') != 1:
        raise ValueError('Unexpected archive queue')
    staged = []
    seen = set()
    opener = urllib.request.build_opener(NoRedirect)
    for entry in entries:
        task = entry['taskId']
        if task not in EXPECTED or task in seen:
            raise ValueError('Unexpected or duplicate task')
        seen.add(task)
        relative, size = EXPECTED[task]
        if entry['path'] != relative or entry['expectedBytes'] != size or entry['dimensions'] != [2560,1712]:
            raise ValueError('Source contract changed')
        target = ROOT/relative
        if not target.resolve().is_relative_to((ROOT/'art').resolve()):
            raise ValueError('Source target escaped art')
        if target.exists():
            data = target.read_bytes()
            if not entry.get('sha256'):
                raise ValueError('Existing source must have a recorded checksum')
        else:
            if entry.get('status') != 'pending':
                raise ValueError('Archived source missing')
            parsed = urllib.parse.urlsplit(entry['url'])
            if (parsed.scheme != 'https' or parsed.hostname != HOST or parsed.username or parsed.password
                or parsed.port not in (None,443) or not parsed.path.startswith('/gpt_image_2_5_flare/'+task+'/')
                or not parsed.path.endswith('.png')):
                raise ValueError('Unexpected source URL')
            try:
                with opener.open(entry['url'], timeout=60) as response:
                    data = response.read(size+1)
            except Exception:
                raise ValueError('Source transfer failed; refresh the media URL, without logging it') from None
        if len(data) != size:
            raise ValueError('Provider byte count does not match')
        digest = hashlib.sha256(data).hexdigest()
        if entry.get('sha256') and entry['sha256'] != digest:
            raise ValueError('Archived checksum mismatch')
        with Image.open(io.BytesIO(data)) as image:
            if image.format != 'PNG' or image.size != (2560,1712):
                raise ValueError('Unexpected image format or dimensions')
            image.verify()
        staged.append((entry,target,data,digest))
    for entry,target,data,digest in staged:
        target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists():
            target.write_bytes(data)
        entry.update(status='archived',sha256=digest)
        entry.pop('url',None)
        old = next((x for x in queue['imports'] if x['path']==entry['path']),None)
        metadata = dict(path=entry['path'],status='archived',reviewStatus=entry['reviewStatus'],
                        sha256=digest,bytes=len(data),width=2560,height=1712,notes=entry['notes'])
        if old is None:
            queue['imports'].append(metadata)
        elif old.get('sha256') != digest:
            raise ValueError('Archive contains a conflicting image revision')
        print('Recovered',entry['path'],len(data),'bytes',digest)
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    queue_path.write_text(json.dumps(queue,indent=2)+'\n')

if __name__ == '__main__':
    recover()
