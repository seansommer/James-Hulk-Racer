"""Archive two explicitly authorized still images. No video or live application access."""
from pathlib import Path
import hashlib, io, json, urllib.parse, urllib.request
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
DEST='art/01-characters/hulk/action-reviews/v01'
CONTRACT={
 'e0e48694-5d96-4263-97c1-da7827fcc8fa':('source-smash.png',4510898),
 '578ccb07-6c15-4897-995d-1566db00f7ab':('source-thunderclap.png',4389518)
}
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):raise ValueError('Unexpected artwork redirect')
def recover():
    path=ROOT/DEST/'sources.json';doc=json.loads(path.read_text());entries=doc.get('sources',[])
    if doc.get('schemaVersion')!=1 or len(entries)!=2:raise ValueError('Invalid source manifest')
    staged=[];seen=set()
    for e in entries:
        task=e['taskId']
        if task not in CONTRACT or task in seen:raise ValueError('Unknown or duplicate source')
        seen.add(task);name,size=CONTRACT[task]
        if e['path']!=DEST+'/'+name or e['dimensions']!=[2560,1712] or e['expectedBytes']!=size:raise ValueError('Source contract changed')
        target=ROOT/e['path']
        if not target.resolve().is_relative_to((ROOT/DEST).resolve()):raise ValueError('Target escaped artwork directory')
        if target.exists():
            if not e.get('sha256'):raise ValueError('Existing source missing checksum')
            data=target.read_bytes()
        else:
            if e['status']!='pending':raise ValueError('Archived source missing')
            u=urllib.parse.urlsplit(e['url'])
            if u.scheme!='https' or u.hostname!='dnznrvs05pmza.cloudfront.net' or u.username or u.password or u.port not in (None,443) or not u.path.startswith('/gpt_image_2_5_sunburst/'+task+'/') or not u.path.endswith('.png'):raise ValueError('Unapproved artwork URL')
            try:
                with urllib.request.build_opener(NoRedirect).open(e['url'],timeout=90) as r:data=r.read(size+1)
            except Exception:raise ValueError('Artwork transfer failed; refresh media URL without printing it') from None
        digest=hashlib.sha256(data).hexdigest()
        if len(data)!=size or (e.get('sha256') and e['sha256']!=digest):raise ValueError('Size/checksum mismatch')
        with Image.open(io.BytesIO(data)) as im:
            if im.size!=(2560,1712) or im.format!='PNG':raise ValueError('Unexpected image')
            im.verify()
        staged.append((e,target,data,digest))
    for e,target,data,digest in staged:
        target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists():target.write_bytes(data)
        e.update(status='archived',sha256=digest);e.pop('url',None)
        print('Archived',target.name,len(data),'bytes; SHA256',digest)
    doc['status']='sources_archived';path.write_text(json.dumps(doc,indent=2)+'\n')
if __name__=='__main__':recover()
