"""Jump 04: source-preserving pose review. Simulation, accounts and live app untouched."""
from pathlib import Path
import base64, hashlib, json, sys
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'production/tools'))
from movement03_export import matte,clear_floor_plate,register,font
FOLDER='art/01-characters/hulk/jump-reviews/v01'
SOURCE_SHA='3f3f2427774acb47d651294ab8af964904463383588bdfe49339e44263f71996'
SCALE=.60
PHASES=['Preparation','Early lift','Rising tuck','Apex tuck','Legs extending','Landing reach','First contact','Absorption','Recovered stance']
CLIPS={
 'jump':dict(label='Jump · six poses',frames=list(range(6)),fps=8,loop=False),
 'land':dict(label='Landing · three poses',frames=[6,7,8],fps=12,loop=False),
 'full':dict(label='Jump → landing',frames=list(range(9)),fps=8,loop=False)}
YS=[0,830,1615,2560];XS=[0,853,1706,2560]
ANCHORS=[(424,798),(1273,800),(2124,800),(424,1590),(1273,1590),(2125,1590),(424,2384),(1273,2384),(2125,2384)]
GROUNDED={0,6,7,8}
# Visually checked white negative spaces; specular armor highlights are deliberately not included.
HOLES={0:[[555,498],[593,548]],1:[[355,245],[488,245]],2:[[448,262]],7:[[568,587],[328,515],[280,588]],8:[[260,475]]}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def art_path(root,name):
 p=(root/name).resolve()
 if not p.is_relative_to((root/'art').resolve()):raise ValueError('Path outside art')
 return p

def pack(frames):
 if len(frames)!=9:raise ValueError('Expected nine selected drawings')
 out=Image.new('RGBA',(792,984));rects=[]
 for i,im in enumerate(frames):
  if im.size!=(256,320) or im.mode!='RGBA':raise ValueError('Expected runtime RGBA')
  x,y=(i%3)*264+4,(i//3)*328+4;out.paste(im,(x,y));rects.append([x,y,256,320])
 return out,rects

def contact_board(frames):
 out=Image.new('RGB',(900,1146),'#153c35');d=ImageDraw.Draw(out)
 d.text((26,20),'HULK JAMESY / JUMP + LAND',font=font(28),fill='#faf7f0')
 d.text((26,60),'9 SELECTED POSE CANDIDATES  /  CHARACTER GROUP 01',font=font(14),fill='#b6ec7a')
 for i,im in enumerate(frames):
  x,y=(i%3)*300+10,92+(i//3)*348
  d.rounded_rectangle((x,y,x+280,y+338),radius=12,fill='#fbf8f1')
  out.paste(im,(x+12,y+2),im)
  d.text((x+14,y+316),f'{i+1:02}  {PHASES[i]}',font=font(14),fill='#153c35')
 return out

def build(root=ROOT):
 folder=art_path(root,FOLDER);source=folder/'source-sheet.png'
 metadata=json.loads((folder/'sources.json').read_text())['sources'][0]
 if metadata['status']!='archived' or metadata['sha256']!=SOURCE_SHA or sha(source)!=SOURCE_SHA:raise ValueError('Source checksum not established')
 with Image.open(source) as im:
  if im.format!='PNG' or im.size!=(2560,2560):raise ValueError('Unexpected source format')
  sheet=im.convert('RGB')
 out=folder/'review-export';out.mkdir(exist_ok=True)
 for sub in ['frames-512','frames-256']:(out/sub).mkdir(exist_ok=True)
 frames=[];records=[]
 for i,anchor in enumerate(ANCHORS):
  c,r=i%3,i//3;rect=[XS[c],YS[r],XS[c+1],YS[r+1]]
  local=[anchor[0]-rect[0],anchor[1]-rect[1]]
  cut=matte(sheet.crop(tuple(rect)),HOLES.get(i,[]))
  if i in GROUNDED:cut=clear_floor_plate(cut,local[1])
  master,offset=register(cut,SCALE,local)
  small=master.convert('RGBa').resize((256,320),Image.Resampling.LANCZOS).convert('RGBA')
  clip='jump' if i<6 else 'land';idx=i if i<6 else i-6;name=f'hulk_{clip}_rear_{idx:03}'
  a=f'frames-512/{name}.png';b=f'frames-256/{name}.png'
  master.save(out/a);small.save(out/b);frames.append(small)
  records.append(dict(id=name,phase=PHASES[i],sourceCell=i+1,sourceRect=rect,provisionalRoot=list(anchor),
    rootInCell=local,commonSourceScale=SCALE,placement=offset,pivot=[.5,.9],frame512=a,frame256=b,
    negativeSpaceSeeds=HOLES.get(i,[]),floorPlateCleanup=i in GROUNDED,productionReady=False))
 atlas,rects=pack(frames);atlas.save(out/'atlas-review.png')
 for rec,rect in zip(records,rects):rec['rect']=rect
 manifest=dict(schemaVersion=1,id='jump-land-04',status='motion_review',productionReady=False,approvedByOwner=False,
  source='source-sheet.png',sourceSha256=SOURCE_SHA,sourceFrameSize=[512,640],runtimeFrameSize=[256,320],
  pivot=[.5,.9],alpha='straight',trimmed=False,rotated=False,commonScale=SCALE,atlas='atlas-review.png',
  atlasSize=list(atlas.size),padding=4,mipmaps=False,clips=CLIPS,frames=records,
  binding='Pose-only samples. The game simulation must supply jump height; no world trajectory is baked into this exporter.',
  notes='Nine selected source-order drawings, not production approval. Pose 2 is early lift, not toe-contact push-off. Root annotations are provisional; head/limb consistency, cape transitions and game-camera alignment remain review items.')
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 contact_board(frames).save(out/'contact-review.jpg',quality=92)
 data=dict(clips=CLIPS,phases=PHASES,pngs=['data:image/png;base64,'+base64.b64encode((out/r['frame256']).read_bytes()).decode() for r in records])
 template=(root/'production/jump04/viewer.html').read_text()
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
 if sha(source)!=SOURCE_SHA:raise ValueError('Source unexpectedly changed')
 report=dict(result='PASS_FILE_CHECKS',selectedDrawings=9,individualPngExports=18,atlasRegionComparisons=9,
   sourcePreserved=True,productionReadyFrames=0,checks=checks,
   scope='Checksums, RGBA dimensions, alpha, margins and atlas equality; not approval of anatomy, motion, real game alignment or physical-phone performance.')
 (out/'technical-checks.json').write_text(json.dumps(report,indent=2)+'\n')
 print('PASS: nine selected poses, 18 PNG exports and nine atlas-region comparisons')
 return manifest
if __name__=='__main__':build()
