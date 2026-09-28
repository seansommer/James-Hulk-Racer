"""Archive only the three explicitly requested idle/bank PNG sources.

First import validates the provider's task path, byte count and dimensions,
then records SHA-256. Later runs require the recorded hash. No game access.
"""
from pathlib import Path
import hashlib, io, json, urllib.parse, urllib.request
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
FOLDER='art/01-characters/hulk/movement-reviews/v01'
TASKS={
    'b9de1615-acfc-405c-86bc-187461c291d7':'source-intermediate.png',
    '7408e01c-9848-4947-bf86-32a07027228b':'source-sheet.png',
    'a84e9f5e-7e1d-4a61-b91e-f1274619cd97':'source-opposite-steps.png',
}
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):
        raise ValueError('Unexpected redirect; artwork transfer stopped')

def validate(entry,data):
    if entry['taskId'] not in TASKS or entry['file'] != TASKS[entry['taskId']]:
        raise ValueError('Unexpected artwork task or destination')
    if not 0 < len(data) == entry['expectedBytes'] <= 20*1024*1024:
        raise ValueError('Provider byte count does not match')
    digest=hashlib.sha256(data).hexdigest()
    if entry.get('sha256') and digest != entry['sha256']:
        raise ValueError('Stored source hash changed')
    with Image.open(io.BytesIO(data)) as im:
        if im.format!='PNG' or list(im.size)!=entry['dimensions'] or im.size!=(2560,1920):
            raise ValueError('Source must be the expected 2560x1920 PNG')
        im.verify()
    return digest

def archive():
    root=(ROOT/FOLDER).resolve()
    if not root.is_relative_to((ROOT/'art').resolve()):raise ValueError('Invalid art root')
    manifest_path=root/'sources.json'
    manifest=json.loads(manifest_path.read_text())
    entries=manifest.get('sources',[])
    if manifest.get('schemaVersion')!=1 or len(entries)!=3 or {x['taskId'] for x in entries}!=set(TASKS):
        raise ValueError('Unexpected source manifest')
    staged=[];opener=urllib.request.build_opener(NoRedirect)
    for e in entries:
        if e['file'] != TASKS[e['taskId']]:raise ValueError('Wrong target')
        target=root/e['file']
        if target.exists():
            if not e.get('sha256'):raise ValueError('Existing file has no recorded hash')
            data=target.read_bytes()
        else:
            if e.get('status')!='pending':raise ValueError('Archived source missing')
            u=urllib.parse.urlsplit(e['url'])
            if (u.scheme!='https' or u.hostname!='dnznrvs05pmza.cloudfront.net' or u.username or u.password
                or u.port not in (None,443) or not u.path.startswith('/gpt_image_2_5_sunburst/'+e['taskId']+'/')
                or not u.path.endswith('.png')):raise ValueError('Unexpected media URL')
            try:
                with opener.open(e['url'],timeout=90) as r:data=r.read(e['expectedBytes']+1)
            except Exception:raise ValueError('Media transfer failed; refresh this artwork link without logging it') from None
        digest=validate(e,data);staged.append((e,target,data,digest))
    for e,target,data,digest in staged:
        if not target.exists():target.write_bytes(data)
        e.update(status='archived',sha256=digest);e.pop('url',None)
        print('Archived',e['file'],len(data),'bytes',digest)
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':archive()
