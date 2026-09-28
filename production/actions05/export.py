"""Action 05: eight Smash and six Thunderclap pose candidates; no game-state access."""
from pathlib import Path
import base64, hashlib, json, sys
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'production/tools'))
from movement03_export import matte,clear_floor_plate,register,font
FOLDER='art/01-characters/hulk/action-reviews/v01'
SOURCES={
 'source-smash.png':dict(sha256='36e645f36a91bf4d358f0c86aa1479d3d9d0d78a84ae92fe4b184fb6d4336692',scale=.62,cols=4,
  roots=[(347,816),(974,816),(1586,816),(2204,816),(343,1590),(982,1590),(1590,1596),(2220,1596)],
  holes={0:[[221,513],[492,525]],5:[[200,658],[484,655]],6:[[438,393],[473,445]],7:[[165,440]]}),
 'source-thunderclap.png':dict(sha256='57df82cb4b5798bdf5f28490d3ed4a6168aaa3688d53ef5d87f41a0ff4812cf8',scale=.60,cols=3,
  roots=[(420,810),(1276,810),(2134,810),(420,1648),(1276,1648),(2134,1648)],holes={})}
PHASES=['Ready','Wind-up','Overhead anticipation','Downward swing','Fists contact','Follow-through','Rising recovery','Returned stance',
 'Ready','Arms wide','Palms approaching','Palms contact','Hands release','Returned stance']
CLIPS={
 'smash':dict(label='Smash · eight poses',frames=list(range(8)),fps=12,loop=False,contactFrame=4,
  note='Both fists read at ground contact. Overhead-to-downswing spacing, cape lift and foot-placement drift still need a shared motion-polish pass.'),
 'thunderclap':dict(label='Thunderclap · six poses',frames=list(range(8,14)),fps=12,loop=False,contactFrame=3,
  note='The rear-three-quarter view keeps the palms visible. Release opens wider than planned; shoulder/view continuity and hand anatomy need final motion review.')}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def art_path(root,name):
 p=(root/name).resolve()
 if not p.is_relative_to((root/'art').resolve()):raise ValueError('Path outside art')
 return p

def pack(frames):
 if len(frames)!=14:raise ValueError('Expected fourteen selected drawings')
 out=Image.new('RGBA',(1056,1312));rects=[]
 for i,im in enumerate(frames):
  if im.size!=(256,320) or im.mode!='RGBA':raise ValueError('Expected runtime RGBA')
  x,y=(i%4)*264+4,(i//4)*328+4;out.paste(im,(x,y));rects.append([x,y,256,320])
 return out,rects

def contact_board(frames,indices,cols,title):
 rows=(len(indices)+cols-1)//cols
 out=Image.new('RGB',(cols*290,100+rows*350),'#153c35');d=ImageDraw.Draw(out)
 d.text((24,20),title,font=font(26),fill='#faf7f0')
 d.text((24,61),'CHARACTER GROUP 01 / SELECTED POSE CANDIDATES',font=font(14),fill='#b6ec7a')
 for j,i in enumerate(indices):
  x,y=(j%cols)*290+9,100+(j//cols)*350
  d.rounded_rectangle((x,y,x+272,y+340),radius=12,fill='#fbf8f1')
  out.paste(frames[i],(x+8,y),frames[i])
  d.text((x+12,y+319),f'{j+1:02}  {PHASES[i]}',font=font(13),fill='#153c35')
 return out

def build(root=ROOT):
 folder=art_path(root,FOLDER);meta=json.loads((folder/'sources.json').read_text())
 metadata={Path(e['path']).name:e for e in meta['sources']}
 if set(metadata)!=set(SOURCES):raise ValueError('Unexpected source list')
 out=folder/'review-export';out.mkdir(exist_ok=True)
 for sub in ['frames-512','frames-256']:(out/sub).mkdir(exist_ok=True)
 frames=[];records=[]
 for source,spec in SOURCES.items():
  p=folder/source;e=metadata[source]
  if e['status']!='archived' or e['sha256']!=spec['sha256'] or sha(p)!=spec['sha256']:raise ValueError('Source hash mismatch')
  with Image.open(p) as im:
   if im.format!='PNG' or im.size!=(2560,1712):raise ValueError('Source image changed')
   sheet=im.convert('RGB')
  cols=spec['cols'];clip='smash' if cols==4 else 'thunderclap'
  for j,rootpoint in enumerate(spec['roots']):
   c,r=j%cols,j//cols;rect=[round(c*2560/cols),r*856,round((c+1)*2560/cols),(r+1)*856]
   local=[rootpoint[0]-rect[0],rootpoint[1]-rect[1]];holes=spec['holes'].get(j,[])
   cut=clear_floor_plate(matte(sheet.crop(tuple(rect)),holes),local[1])
   master,offset=register(cut,spec['scale'],local)
   small=master.convert('RGBa').resize((256,320),Image.Resampling.LANCZOS).convert('RGBA')
   name=f'hulk_{clip}_rear_{j:03}';a=f'frames-512/{name}.png';b=f'frames-256/{name}.png'
   master.save(out/a);small.save(out/b);i=len(frames);frames.append(small)
   records.append(dict(id=name,clip=clip,phase=PHASES[i],source=source,sourceCell=j+1,sourceRect=rect,
    provisionalRoot=list(rootpoint),rootInCell=local,commonSourceScale=spec['scale'],placement=offset,pivot=[.5,.9],
    view='rear' if clip=='smash' else 'rear_three_quarter',frame512=a,frame256=b,
    negativeSpaceSeeds=holes,floorPlateCleanup=True,productionReady=False))
 atlas,rects=pack(frames);atlas.save(out/'atlas-review.png')
 for rec,rect in zip(records,rects):rec['rect']=rect
 manifest=dict(schemaVersion=1,id='actions-05',status='motion_review',productionReady=False,approvedByOwner=False,
  sourceHashes={n:s['sha256'] for n,s in SOURCES.items()},sourceFrameSize=[512,640],runtimeFrameSize=[256,320],
  pivot=[.5,.9],alpha='straight',trimmed=False,rotated=False,atlas='atlas-review.png',atlasSize=list(atlas.size),
  padding=4,mipmaps=False,clips=CLIPS,frames=records,
  contactMarkers='Review labels only. These markers never trigger game damage, score receipts, cooldowns or effects.',
  notes='Fourteen pose candidates, source order preserved within each action. One scale per source and explicit ground-root translations. No hidden in-betweens, mirroring, warping or final camera/hitbox approval.')
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 contact_board(frames,range(8),4,'HULK JAMESY / SMASH').save(out/'contact-smash.jpg',quality=92)
 contact_board(frames,range(8,14),3,'HULK JAMESY / THUNDERCLAP').save(out/'contact-thunderclap.jpg',quality=92)
 contact_board(frames,range(14),4,'HULK JAMESY / SMASH + THUNDERCLAP').save(out/'contact-review.jpg',quality=92)
 data=dict(clips=CLIPS,phases=PHASES,pngs=['data:image/png;base64,'+base64.b64encode((out/r['frame256']).read_bytes()).decode() for r in records])
 template=(root/'production/actions05/viewer.html').read_text()
 if template.count('__ASSET_DATA__')!=1:raise ValueError('Invalid review template')
 (out/'review.html').write_text(template.replace('__ASSET_DATA__',json.dumps(data)))
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
 report=dict(result='PASS_FILE_CHECKS',selectedDrawings=14,individualPngExports=28,atlasRegionComparisons=14,
  sourcesPreserved=2,productionReadyFrames=0,checks=checks,
  scope='Checksums, RGBA dimensions, alpha, margins and atlas equality. Not approval of motion, anatomy, camera matching or physical-device performance.')
 (out/'technical-checks.json').write_text(json.dumps(report,indent=2)+'\n')
 print('PASS: 14 poses / 28 PNG exports / 14 atlas comparisons / two preserved sources')
 return manifest
if __name__=='__main__':build()
