"""States 06: thirteen selected pose candidates; no new generation or game-state access."""
from pathlib import Path
import base64, hashlib, json, sys
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'production/tools'))
from movement03_export import matte,clear_floor_plate,register,font
FOLDER='art/01-characters/hulk/state-reviews/v01'
SOURCES={
 'source-power-up.png':dict(sha256='01cfb020dc47f515a478b871f6c6683522b1bc24f82776aab7368a2109f33d9b',size=[2560,1712],scale=.63,cols=3,rows=2,clip='power_up',view='rear',
  roots=[(352,802),(1260,802),(2182,802),(348,1610),(1268,1610),(2183,1610)],
  holes={0:[[231,501],[479,507],[457,447]],1:[[295,429],[514,428]],2:[[367,457],[586,452]],3:[[237,378]],4:[[289,368]],5:[[358,464],[607,469]]}),
 'source-bump.png':dict(sha256='b496eb4c1fc13906c097c78da457f442d6ae4cd3f7775e07bf4216f4ff131757',size=[2912,1248],scale=.49,cols=3,rows=1,clip='hurt',view='rear',
  roots=[(514,1088),(1389,1088),(2406,1088)],holes={}),
 'source-menu-idle.png':dict(sha256='0dbdcfac9f2f203e90ea0797261b57f699dabafbbe6b0543e18acbc1e45689e9',size=[2560,1920],scale=.50,cols=2,rows=2,clip='menu_idle',view='front_three_quarter',
  roots=[(600,866),(1805,866),(600,1818),(1804,1818)],holes={0:[[485,484]],1:[[420,480]],2:[[498,474]],3:[[402,477]]})}
PHASES=['Ready','Gathering power','Compressed anticipation','Rising strength','Peak stance','Settling ready',
 'Surprised lean','Stabilizing step','Balance restored','Calm ready','Gentle inhale','Breath held','Soft exhale']
CLIPS={
 'power_up':dict(label='Power-up · six poses',frames=list(range(6)),fps=12,loop=False,
  note='Grounded body-pose study only; aura stays separate. Foot spacing, shoulders, cape spread and the return to ready need unified motion review.'),
 'hurt':dict(label='Bump recovery · three poses',frames=list(range(6,9)),fps=10,loop=False,
  note='Gentle surprise, a stabilizing step and recovery. Open-glove anatomy, side-to-side weight transfer and three-pose timing remain review items.'),
 'menu_idle':dict(label='Menu idle · four poses',frames=list(range(9,13)),fps=6,loop=True,
  note='Chest and belt J are preserved. This loop is a candidate: face/cape continuity and the fourth-to-first seam still need polish. The front camera is deliberately distinct from rear gameplay.')}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def art_path(root,name):
 p=(root/name).resolve()
 if not p.is_relative_to((root/'art').resolve()):raise ValueError('Path outside art')
 return p

def pack(frames):
 if len(frames)!=13:raise ValueError('Expected thirteen selected drawings')
 out=Image.new('RGBA',(1056,1312));rects=[]
 for i,im in enumerate(frames):
  if im.size!=(256,320) or im.mode!='RGBA':raise ValueError('Expected runtime RGBA')
  x,y=(i%4)*264+4,(i//4)*328+4
  out.paste(im,(x,y));rects.append([x,y,256,320])
 return out,rects

def contact_board(frames,indices,cols,title):
 indices=list(indices);rows=(len(indices)+cols-1)//cols
 out=Image.new('RGB',(cols*290,100+rows*350),'#153c35');d=ImageDraw.Draw(out)
 d.text((24,20),title,font=font(23),fill='#faf7f0')
 d.text((24,61),'CHARACTER GROUP 01 / POSE CANDIDATES / STATES 06',font=font(12),fill='#b6ec7a')
 for j,i in enumerate(indices):
  x,y=(j%cols)*290+9,100+(j//cols)*350
  d.rounded_rectangle((x,y,x+272,y+340),radius=12,fill='#fbf8f1')
  out.paste(frames[i],(x+8,y),frames[i])
  d.text((x+12,y+319),f'{j+1:02}  {PHASES[i]}',font=font(12),fill='#153c35')
 return out

def build(root=ROOT):
 folder=art_path(root,FOLDER);meta=json.loads((folder/'sources.json').read_text())
 metadata={Path(e['path']).name:e for e in meta['sources']}
 if set(metadata)!=set(SOURCES):raise ValueError('Unexpected source list')
 # Verify every source before producing any derived export.
 sheets={}
 for source,spec in SOURCES.items():
  p=folder/source;e=metadata[source]
  if e['status']!='archived' or e['sha256']!=spec['sha256'] or sha(p)!=spec['sha256']:raise ValueError('Source hash mismatch')
  with Image.open(p) as im:
   if im.format!='PNG' or list(im.size)!=spec['size']:raise ValueError('Source image changed')
   sheets[source]=im.convert('RGB')
 out=folder/'review-export';out.mkdir(exist_ok=True)
 for sub in ['frames-512','frames-256']:(out/sub).mkdir(exist_ok=True)
 frames=[];records=[]
 for source,spec in SOURCES.items():
  sheet=sheets[source];w,h=spec['size'];cols=spec['cols'];rows=spec['rows'];clip=spec['clip']
  for j,rootpoint in enumerate(spec['roots']):
   c,r=j%cols,j//cols;rect=[round(c*w/cols),round(r*h/rows),round((c+1)*w/cols),round((r+1)*h/rows)]
   local=[rootpoint[0]-rect[0],rootpoint[1]-rect[1]];holes=spec['holes'].get(j,[])
   cut=clear_floor_plate(matte(sheet.crop(tuple(rect)),holes),local[1])
   master,offset=register(cut,spec['scale'],local)
   small=master.convert('RGBa').resize((256,320),Image.Resampling.LANCZOS).convert('RGBA')
   view='front' if clip=='menu_idle' else 'rear';name=f'hulk_{clip}_{view}_{j:03}'
   a=f'frames-512/{name}.png';b=f'frames-256/{name}.png';master.save(out/a);small.save(out/b)
   i=len(frames);frames.append(small)
   records.append(dict(id=name,clip=clip,phase=PHASES[i],source=source,sourceCell=j+1,sourceRect=rect,
    provisionalRoot=list(rootpoint),rootInCell=local,commonSourceScale=spec['scale'],placement=offset,pivot=[.5,.9],
    view=spec['view'],frame512=a,frame256=b,negativeSpaceSeeds=holes,floorPlateCleanup=True,productionReady=False))
 atlas,rects=pack(frames);atlas.save(out/'atlas-review.png')
 for rec,rect in zip(records,rects):rec['rect']=rect
 manifest=dict(schemaVersion=1,id='states-06',status='motion_review',productionReady=False,approvedByOwner=False,
  sourceHashes={n:s['sha256'] for n,s in SOURCES.items()},sourceFrameSize=[512,640],runtimeFrameSize=[256,320],
  pivot=[.5,.9],alpha='straight',trimmed=False,rotated=False,atlas='atlas-review.png',atlasSize=list(atlas.size),
  padding=4,mipmaps=False,clips=CLIPS,frames=records,
  notes='13 selected candidates in original source order. One scale per sheet, explicit provisional ground-root translations, no per-pose fit, mirror, warp or in-betweens. Menu/front scale differs from gameplay/rear for cape clearance. Final likeness, motion, camera and hitbox registration remain unapproved. No game-state events.')
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 for clip,cols,title in [('power_up',3,'HULK JAMESY / POWER-UP'),('hurt',3,'HULK JAMESY / BUMP RECOVERY'),('menu_idle',2,'HULK JAMESY / MENU IDLE')]:
  contact_board(frames,CLIPS[clip]['frames'],cols,title).save(out/f'contact-{clip}.jpg',quality=92)
 contact_board(frames,range(13),4,'HULK JAMESY / POWER · RECOVERY · IDLE').save(out/'contact-review.jpg',quality=92)
 data=dict(clips=CLIPS,phases=PHASES,views=[r['view'] for r in records],pngs=['data:image/png;base64,'+base64.b64encode((out/r['frame256']).read_bytes()).decode() for r in records])
 template=(root/'production/states06/viewer.html').read_text()
 if template.count('__ASSET_DATA__')!=1:raise ValueError('Invalid review template')
 (out/'review.html').write_text(template.replace('__ASSET_DATA__',json.dumps(data).replace('<','\\u003c')))
 checks=[]
 for rec,frame in zip(records,frames):
  for k,size in [('frame512',(512,640)),('frame256',(256,320))]:
   p=out/rec[k]
   with Image.open(p) as im:
    alpha=im.getchannel('A');b=alpha.getbbox()
    if im.size!=size or im.mode!='RGBA' or alpha.getextrema()!=(0,255) or not b or b[0]<2 or b[1]<2 or b[2]>im.width-2 or b[3]>im.height-2:raise ValueError('Canvas/alpha/clipping error: '+p.name)
    checks.append(dict(file=rec[k],sha256=sha(p),dimensions=list(size),alpha=[0,255],bounds=list(b)))
  x,y,w,h=rec['rect']
  if atlas.crop((x,y,x+w,y+h)).tobytes()!=frame.tobytes():raise ValueError('Atlas differs from runtime pixels')
 for source,spec in SOURCES.items():
  if sha(folder/source)!=spec['sha256']:raise ValueError('Source unexpectedly changed')
 report=dict(result='PASS_FILE_CHECKS',selectedDrawings=13,individualPngExports=26,atlasRegionComparisons=13,
  sourcesPreserved=3,productionReadyFrames=0,checks=checks,
  scope='Checksums, RGBA dimensions, alpha, margins and atlas equality. Not approval of motion, anatomy, camera matching or physical-device performance.')
 (out/'technical-checks.json').write_text(json.dumps(report,indent=2)+'\n')
 print('PASS: 13 poses / 26 PNG exports / 13 atlas comparisons / three preserved sources')
 return manifest
if __name__=='__main__':build()
