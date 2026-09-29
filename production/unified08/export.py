"""Assemble existing Hulk review exports; no generation, rescaling or account IO."""
from __future__ import annotations
import argparse, base64, hashlib, json, os, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

CLIPS = [
 ('rear_idle','Rear idle','movement-reviews/v01',list(range(4)),6,True,'rear'),
 ('run','Run','run-reviews/v02',list(range(8)),12,True,'rear'),
 ('lean_left','Bank left','movement-reviews/v01',list(range(4,8)),12,True,'rear'),
 ('lean_right','Bank right','movement-reviews/v01',list(range(8,12)),12,True,'rear'),
 ('jump','Jump','jump-reviews/v01',list(range(6)),8,False,'rear'),
 ('land','Landing','jump-reviews/v01',list(range(6,9)),12,False,'rear'),
 ('smash','Smash','action-reviews/v01',list(range(8)),12,False,'rear'),
 ('thunderclap','Thunderclap','action-reviews/v01',list(range(8,14)),12,False,'rear three-quarter'),
 ('power_up','Power-up','state-reviews/v01',list(range(6)),12,False,'rear'),
 ('hurt','Bump recovery','state-reviews/v01',list(range(6,9)),10,False,'rear'),
 ('victory','Victory','victory-reviews/v01',list(range(8)),10,False,'front three-quarter'),
 ('menu_idle','Menu idle','state-reviews/v01',list(range(9,13)),6,True,'front three-quarter')]
NOTES = {
 'rear_idle':'Use this as the rear-view scale reference. Review breathing and cape loop closure.',
 'run':'Review foot-contact cadence, hair size, cape motion and the last-to-first seam. No new timing is applied.',
 'lean_left':'Keep the bank direction and support-foot sequence distinct. Compare shoulder width and root with the run.',
 'lean_right':'Separately drawn, not mirrored. Compare body scale and support cadence with the opposite bank.',
 'jump':'Body poses only: simulation must supply jump height. Compare takeoff, landing and the return to run.',
 'land':'Review contact, compression and recovery spacing. Do not score or replay a jump from animation frames.',
 'smash':'Review overhead-to-contact spacing, planted boots, cape lift and return to the running camera.',
 'thunderclap':'Rear-three-quarter view differs from the run. Review the camera switch, wide release and hand anatomy.',
 'power_up':'Compare planted feet, shoulder width, cape spread and first/last pose. Aura remains a separate asset.',
 'hurt':'Review the stabilizing step and open-glove anatomy. It is a gentle reaction, not a lasting injury.',
 'victory':'Owner likes the visual direction. Review frame 4 to 5 and compare face, feet and scale with menu idle.',
 'menu_idle':'Compare face and costume with victory at equal canvas scale. Review frame 4 to 1 and cape continuity.'}

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def font(size,bold=False):
 return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if bold else '')+'.ttf',size)
def validate(im):
 if im.size!=(256,320) or im.mode!='RGBA': raise ValueError('Expected 256x320 RGBA candidate')
 a=im.getchannel('A');lo,hi=a.getextrema()
 if not lo<hi:raise ValueError('No distinct foreground and transparency')
 return a.point(lambda v:255 if v>=16 else 0).getbbox()

def board(data,out):
 sheet=Image.new('RGB',(1440,1676),'#faf7f0');d=ImageDraw.Draw(sheet)
 d.rectangle((0,0,1440,142),fill='#153c35')
 d.text((32,28),'HULK JAMESY  /  COMPLETE POSE LIBRARY',font=font(31,True),fill='white')
 d.text((32,80),f'{data["availableFrames"]} existing drawings  |  12 planned clips  |  Consistency review, not game integration',font=font(18),fill='#c4dfc9')
 for k,clip in enumerate(data['clips']):
  x=24+(k%4)*354;y=164+(k//4)*492
  d.rounded_rectangle((x,y,x+336,y+474),radius=18,fill='white',outline='#d3dbd5',width=2)
  d.text((x+18,y+18),clip['label'],font=font(22,True),fill='#153c35')
  d.text((x+18,y+52),f'{len(clip["frames"])}/{clip["planned"]} drawings · '+clip['view'],font=font(14),fill='#527062')
  pick={'smash':4,'thunderclap':3,'jump':2,'victory':3}.get(clip['id'],0)
  if clip['frames']:
   frame=clip['frames'][min(pick,len(clip['frames'])-1)]
   with Image.open(out/frame['file']) as im:sheet.paste(im,(x+40,y+86),im)
  else:d.text((x+28,y+220),'Source upload pending',font=font(18),fill='#7542b4')
  d.line((x+30,y+374,x+306,y+374),fill='#dfc895',width=1)
  d.text((x+18,y+421),'Loop' if clip['loop'] else 'One-shot / hold',font=font(15),fill='#7542b4')
  d.text((x+18,y+445),f'{clip["fps"]} fps preview · Shared canvas / ground guide',font=font(12),fill='#527062')
 d.text((32,1640),'Same 256 x 320 canvas • Originals unchanged • Green/purple identity and permanent J emblems',font=font(16),fill='#153c35')
 sheet.save(out/'Hulk-Jamesy-All-Clips.jpg',quality=92)
 film=Image.new('RGB',(2040,12*314+132),'#faf7f0');dr=ImageDraw.Draw(film)
 dr.rectangle((0,0,2040,116),fill='#153c35');dr.text((28,25),'HULK JAMESY / ALL SELECTED DRAWINGS',font=font(33,True),fill='white')
 dr.text((28,75),'Source order and previously selected sequences retained. These are review candidates.',font=font(18),fill='#c4dfc9')
 for k,c in enumerate(data['clips']):
  y=132+k*314;dr.text((24,y+8),c['label'],font=font(19,True),fill='#153c35')
  dr.text((24,y+40),f'{len(c["frames"])}/{c["planned"]}',font=font(16),fill='#7542b4')
  for i,f in enumerate(c['frames']):
   x=198+i*228;dr.rounded_rectangle((x,y,x+216,y+298),radius=10,fill='white',outline='#d3dbd5')
   with Image.open(out/f['file']) as im:
    thumb=im.resize((192,240),Image.Resampling.LANCZOS);film.paste(thumb,(x+12,y+15),thumb)
   dr.line((x+8,y+231,x+208,y+231),fill='#dfc895')
   dr.text((x+14,y+266),f'{i+1:02d}  /  {f["phase"][:23]}',font=font(11),fill='#153c35')
 film.save(out/'Hulk-Jamesy-All-Drawings.jpg',quality=92)

def assemble(root:Path,out:Path,template:Path,victory:Path|None=None,link_existing:bool=False):
 root=root.resolve();out=out.resolve();out.mkdir(parents=True,exist_ok=True)
 data={'schemaVersion':1,'title':'Hulk Jamesy · Unified Review 08','productionReady':False,'ownerFeedback':{'scope':'Victory 07 visual direction','text':'Looks good let’s continue','notEquivalentTo':'64-frame production or motion approval'},'plannedFrames':64,'pivot':[.5,.9],'canvas':[256,320],'clips':[],'sourceSnapshot':((root/'review-snapshot-commit.txt').read_text().strip() if (root/'review-snapshot-commit.txt').exists() else os.environ.get('GITHUB_SHA'))}
 records=[];warnings=[]
 for cid,label,group,indices,fps,loop,view in CLIPS:
  folder=root/'art/01-characters/hulk'/group/'review-export';local=False
  if cid=='victory' and victory is not None:folder=victory.resolve();local=True
  mp=folder/'manifest.json';clip=dict(id=cid,label=label,planned=len(indices),fps=fps,loop=loop,view=view,note=NOTES[cid],frames=[],sourceManifest=mp.relative_to(root).as_posix() if mp.is_relative_to(root) else 'conversation:Victory07/review-export/manifest.json',archive='conversation_only' if local else 'github_art_branch')
  if not mp.exists():
   if cid!='victory':raise FileNotFoundError(mp)
   clip['archive']='pending_source_upload';clip['note']='Victory source still awaits direct GitHub upload. The conversation package contains these eight drawings.'
   data['clips'].append(clip);warnings.append('Victory is missing from the GitHub checkout; not counted as archived.');continue
  manifest=json.loads(mp.read_text());clip['sourceManifestSha256']=digest(mp)
  for j,index in enumerate(indices):
   frame=manifest['frames'][index];src=folder/(frame.get('frame256') or frame['runtime']);target=out/f'frames/{cid}_{j:03}.png';target.parent.mkdir(exist_ok=True)
   with Image.open(src) as im:bbox=validate(im)
   if not link_existing:
    shutil.copy2(src,target)
    if digest(src)!=digest(target):raise ValueError('Copy differs from selected export')
   else:target=src
   phase=frame.get('phase') or frame.get('phaseTarget') or str(j+1)
   spec={'file':Path(os.path.relpath(target,out)).as_posix(),'phase':phase,'sha256':digest(src),'visibleBounds':bbox,'sourceId':frame['id'],'sourcePath':src.relative_to(root).as_posix() if src.is_relative_to(root) else 'conversation:Victory07/'+src.name}
   clip['frames'].append(spec);records.append(spec)
  data['clips'].append(clip)
 data['availableFrames']=sum(len(c['frames']) for c in data['clips']);data['githubArchivedFrames']=sum(len(c['frames']) for c in data['clips'] if c['archive']=='github_art_branch')
 if data['availableFrames'] not in (56,64):raise ValueError('Unexpected candidate count')
 (out/'manifest.json').write_text(json.dumps(data,indent=2)+'\n')
 (out/'manifest.js').write_text('window.REVIEW_DATA = '+json.dumps(data)+';\n')
 text=template.read_text();(out/'review.html').write_text(text)
 single=json.loads(json.dumps(data))
 for c in single['clips']:
  for f in c['frames']:f['file']='data:image/png;base64,'+base64.b64encode((out/f['file']).read_bytes()).decode()
 standalone=text.replace('<script src="manifest.js"></script>','<script>window.REVIEW_DATA = '+json.dumps(single).replace('</','<\\/')+';</script>')
 (out/'Hulk-Jamesy-Review.html').write_text(standalone)
 board(data,out)
 report={'result':'PASS','checkedFrames':len(records),'unchangedCopies':0 if link_existing else len(records),'referencedOriginals':len(records) if link_existing else 0,'dimension':[256,320],'alpha':'All frames are RGBA with distinct foreground and transparency','notTested':['Animation approval','Camera / hitbox alignment','Physical iPhone Safari'],'warnings':warnings,'localSupplement':'Victory07' if victory else None}
 (out/'file-checks.json').write_text(json.dumps(report,indent=2)+'\n')
 return data

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--template',type=Path,required=True);ap.add_argument('--victory-export',type=Path);ap.add_argument('--link-existing',action='store_true')
 a=ap.parse_args();d=assemble(a.root,a.out,a.template,a.victory_export,a.link_existing);print(f'Assembled {d["availableFrames"]} selected drawings; {d["githubArchivedFrames"]} confirmed in GitHub input.')
