"""Check actual Victory 07 files. No image-generation service or game access."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
from PIL import Image
root=Path(sys.argv[1]);out=root/'review-export'
m=json.loads((out/'manifest.json').read_text());checks=[]
def check(condition,name):
    if not condition:raise AssertionError(name)
    checks.append(name)
source=root/'sources/hulk-victory-v01-source.png'
check(hashlib.sha256(source.read_bytes()).hexdigest()==m['sourceSha256'],'Original-source checksum')
check(len(m['frames'])==8,'Exactly eight selected drawings')
check([f['sourceIndex'] for f in m['frames']]==list(range(8)),'Original reading order retained')
check(m['productionReady'] is False,'No implicit production approval')
check(m['registration']['perPoseFit'] is False,'No per-pose fitting')
atlas=Image.open(out/m['atlas']['file'])
for i,f in enumerate(m['frames']):
    for label,size,key in [('master',(512,640),'masterSha256'),('runtime',(256,320),'runtimeSha256')]:
        path=out/f[label]
        with Image.open(path) as im:
            check(im.mode=='RGBA' and im.size==size,f'{i:02} {label}: RGBA dimensions')
            a=np.asarray(im.getchannel('A'))
            check(a.min()==0 and a.max()==255 and np.any((a>0)&(a<255)),f'{i:02} {label}: transparent + opaque + partial alpha')
            check(not(a[0].any() or a[-1].any() or a[:,0].any() or a[:,-1].any()),f'{i:02} {label}: clear edges')
            check(hashlib.sha256(path.read_bytes()).hexdigest()==f[key],f'{i:02} {label}: file checksum')
    x,y,w,h=f['atlasRect']
    check(np.array_equal(np.asarray(atlas.crop((x,y,x+w,y+h))),np.asarray(Image.open(out/f['runtime']))),f'{i:02}: atlas pixel equality')
check(m['clips'][0]['loop'] is False and m['clips'][0]['fps']==10,'One-shot metadata')
report={'result':'PASS','checkCount':len(checks),'checks':checks,'sourceSha256':m['sourceSha256'],'scope':'File integrity only; not motion approval, browser testing or game testing.'}
(root/'qa').mkdir(exist_ok=True);(root/'qa/file-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'PASS: {len(checks)} file checks')
