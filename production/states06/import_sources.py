"""Archive three already-generated Jamesy still sheets, without new generation or game access."""
from pathlib import Path
import hashlib, io, json, urllib.parse, urllib.request
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
DEST='art/01-characters/hulk/state-reviews/v01'
CONTRACT={
 '71920b12-6569-4165-b144-6ed8ff4eb5db':('source-power-up.png',3263089,[2560,1712]),
 '681bd6a4-4d25-4b58-8752-85786c824378':('source-bump.png',2779604,[2912,1248]),
 '7f8efcb6-d7c7-4bc0-ae79-4412fb7d6eb5':('source-menu-idle.png',3398619,[2560,1920])
}
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):raise ValueError('Unexpected artwork redirect')
def recover(root=ROOT):
 path=root/DEST/'sources.json';document=json.loads(path.read_text());entries=document.get('sources',[])
 if document.get('schemaVersion')!=1 or len(entries)!=3:raise ValueError('Invalid source manifest')
 staged=[];seen=set()
 for e in entries:
  task=e['taskId']
  if task not in CONTRACT or task in seen:raise ValueError('Unknown or duplicate source')
  seen.add(task);name,size,dims=CONTRACT[task]
  if e['path']!=DEST+'/'+name or e['dimensions']!=dims or e['expectedBytes']!=size:raise ValueError('Source contract changed')
  target=root/e['path']
  if not target.resolve().is_relative_to((root/DEST).resolve()):raise ValueError('Escaped artwork destination')
  if target.exists():
   if not e.get('sha256'):raise ValueError('Existing source missing checksum')
   data=target.read_bytes()
  else:
   if e['status']!='pending':raise ValueError('Archived source missing')
   u=urllib.parse.urlsplit(e['url'])
   if u.scheme!='https' or u.hostname!='dnznrvs05pmza.cloudfront.net' or u.username or u.password or u.port not in (None,443) or not u.path.startswith('/gpt_image_2_5_flare/'+task+'/') or not u.path.endswith('.png'):raise ValueError('Unapproved artwork URL')
   try:
    with urllib.request.build_opener(NoRedirect).open(e['url'],timeout=90) as r:data=r.read(size+1)
   except Exception:raise ValueError('Artwork transfer failed; refresh media URL without printing it') from None
  digest=hashlib.sha256(data).hexdigest()
  if len(data)!=size or (e.get('sha256') and e['sha256']!=digest):raise ValueError('Source size/checksum mismatch')
  with Image.open(io.BytesIO(data)) as im:
   if list(im.size)!=dims or im.format!='PNG':raise ValueError('Unexpected source image')
   im.verify()
  staged.append((e,target,data,digest))
 for e,target,data,digest in staged:
  target.parent.mkdir(parents=True,exist_ok=True)
  if not target.exists():target.write_bytes(data)
  e.update(status='archived',sha256=digest);e.pop('url',None)
  print('Archived',target.name,len(data),'bytes; SHA256',digest)
 document['status']='sources_archived';path.write_text(json.dumps(document,indent=2)+'\n')
if __name__=='__main__':recover()
