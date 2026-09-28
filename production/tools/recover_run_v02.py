"""Archive only the two explicitly authorized rear-run v02 image tasks."""
import hashlib, io, json, urllib.parse, urllib.request
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
DEST='art/01-characters/hulk/run-reviews/v02/'
TASKS={'f0922c65-0d68-4583-b181-ca969c7733ed':'source-intermediate.png','bb55a169-e01f-4908-99f8-73bf70a64025':'source-sheet.png'}
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):raise ValueError('Unexpected source redirect')
def recover():
    path=ROOT/'art/run-revision-02.json';data=json.loads(path.read_text())
    entries=data.get('sources',[])
    if data.get('schemaVersion')!=1 or not 1<=len(entries)<=2:raise ValueError('Unexpected manifest')
    queue_path=ROOT/'art/import-queue.json';queue=json.loads(queue_path.read_text())
    if queue.get('schemaVersion')!=1:raise ValueError('Unexpected archive queue')
    staged=[];seen=set()
    for e in entries:
        task=e.get('taskId')
        if task not in TASKS or task in seen or e.get('path')!=DEST+TASKS[task]:raise ValueError('Unexpected task or target')
        seen.add(task);target=(ROOT/e['path']).resolve()
        if not target.is_relative_to((ROOT/DEST).resolve()):raise ValueError('Target escaped artwork folder')
        size=e['expectedBytes']
        if type(size)!=int or not 0<size<=25*1024*1024 or e['dimensions']!=[2560,1712]:raise ValueError('Unexpected source contract')
        if target.exists():
            if not e.get('sha256'):raise ValueError('Existing source lacks checksum')
            raw=target.read_bytes()
        else:
            if e.get('status')!='pending':raise ValueError('Archived source missing')
            u=urllib.parse.urlsplit(e['url'])
            if u.scheme!='https' or u.hostname!='dnznrvs05pmza.cloudfront.net' or u.username or u.password or u.port not in (None,443) or not u.path.startswith('/gpt_image_2_5_sunburst/'+task+'/') or not u.path.endswith('.png'):raise ValueError('Unexpected image URL')
            try:
                with urllib.request.build_opener(NoRedirect).open(e['url'],timeout=90) as r:raw=r.read(size+1)
            except Exception:raise ValueError('Artwork download failed; refresh its media transfer URL') from None
        digest=hashlib.sha256(raw).hexdigest()
        if len(raw)!=size or (e.get('sha256') and digest!=e['sha256']):raise ValueError('Source size or checksum mismatch')
        with Image.open(io.BytesIO(raw)) as im:
            if im.format!='PNG' or im.size!=(2560,1712):raise ValueError('Unexpected image dimensions or format')
            im.verify()
        old=next((v for v in queue['imports'] if v['path']==e['path']),None)
        if old and old.get('sha256')!=digest:raise ValueError('Conflicting archive entry')
        staged.append((e,target,raw,digest,old))
    for e,target,raw,digest,old in staged:
        target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists():target.write_bytes(raw)
        e.update(status='archived',sha256=digest);e.pop('url',None)
        record=dict(path=e['path'],status='archived',reviewStatus=e['reviewStatus'],sha256=digest,bytes=len(raw),width=2560,height=1712,notes=e['notes'])
        if old:old.update(record)
        else:queue['imports'].append(record)
        print('Archived',e['path'],len(raw),'bytes',digest)
    path.write_text(json.dumps(data,indent=2)+'\n');queue_path.write_text(json.dumps(queue,indent=2)+'\n')
if __name__=='__main__':recover()
