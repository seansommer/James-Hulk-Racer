"""Archive one explicitly authorized still image. No video, app or account access."""
from pathlib import Path
import hashlib, io, json, urllib.parse, urllib.request
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
DEST='art/01-characters/hulk/jump-reviews/v01'
TASK='0f1a94b3-5a0c-456f-a6e7-e5a4a758bc14'
SIZE=5494363
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):
        raise ValueError('Unexpected artwork redirect')
def recover():
    path=ROOT/DEST/'sources.json';doc=json.loads(path.read_text())
    if doc.get('schemaVersion')!=1 or len(doc.get('sources',[]))!=1:raise ValueError('Invalid source manifest')
    e=doc['sources'][0]
    if e['taskId']!=TASK or e['path']!=DEST+'/source-sheet.png' or e['dimensions']!=[2560,2560] or e['expectedBytes']!=SIZE:raise ValueError('Source contract changed')
    target=ROOT/e['path']
    if not target.resolve().is_relative_to((ROOT/DEST).resolve()):raise ValueError('Target escaped artwork directory')
    if target.exists():
        if not e.get('sha256'):raise ValueError('Existing source missing checksum')
        data=target.read_bytes()
    else:
        if e['status']!='pending':raise ValueError('Archived source missing')
        u=urllib.parse.urlsplit(e['url'])
        if u.scheme!='https' or u.hostname!='dnznrvs05pmza.cloudfront.net' or u.username or u.password or u.port not in (None,443) or not u.path.startswith('/gpt_image_2_5_sunburst/'+TASK+'/') or not u.path.endswith('.png'):raise ValueError('Unapproved artwork URL')
        try:
            with urllib.request.build_opener(NoRedirect).open(e['url'],timeout=90) as r:data=r.read(SIZE+1)
        except Exception:raise ValueError('Artwork transfer failed; refresh this media URL without printing it') from None
    digest=hashlib.sha256(data).hexdigest()
    if len(data)!=SIZE or (e.get('sha256') and e['sha256']!=digest):raise ValueError('Artwork size/checksum mismatch')
    with Image.open(io.BytesIO(data)) as im:
        if im.size!=(2560,2560) or im.format!='PNG':raise ValueError('Unexpected image')
        im.verify()
    target.parent.mkdir(parents=True,exist_ok=True)
    if not target.exists():target.write_bytes(data)
    e.update(status='archived',sha256=digest);e.pop('url',None)
    doc['status']='source_archived';path.write_text(json.dumps(doc,indent=2)+'\n')
    print('Archived jump/landing source:',len(data),'bytes; SHA256',digest)
if __name__=='__main__':recover()
