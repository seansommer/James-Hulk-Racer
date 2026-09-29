"""Export selected idle/bank drawing candidates; no generated in-betweens or game access."""
from pathlib import Path
import base64, hashlib, json, math
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
ROOT=Path(__file__).resolve().parents[2]
FOLDER='art/01-characters/hulk/movement-reviews/v01'
# Populated from the inspected sources. Each source has one uniform scale.
SCALES={'source-sheet.png':.78,'source-opposite-steps.png':.51}
FRAMES=[]
for i,x in enumerate([343,969,1596,2223]):FRAMES.append((f'hulk_idle_rear_{i:03}','source-sheet.png',[i*640,0,(i+1)*640,658],[x-i*640,640],[]))
for i,x in enumerate([328,956]):FRAMES.append((f'hulk_bank_left_{i:03}','source-sheet.png',[i*640,658,(i+1)*640,1240],[x-i*640,568],[]))
for i,x in enumerate([690,1875]):FRAMES.append((f'hulk_bank_left_{i+2:03}','source-opposite-steps.png',[i*1280,0,(i+1)*1280,900],[x-i*1280,866],[]))
for i,x in enumerate([346,992]):FRAMES.append((f'hulk_bank_right_{i:03}','source-sheet.png',[i*640,1240,(i+1)*640,1920],[x-i*640,590],[]))
for i,x in enumerate([650,1874]):FRAMES.append((f'hulk_bank_right_{i+2:03}','source-opposite-steps.png',[i*1280,900,(i+1)*1280,1920],[x-i*1280,920],[]))
CLIPS={
 'rear_idle':dict(label='Rear idle',frames=[0,1,2,3],fps=6,phaseLabels=['Rest','Breath rising','Breath peak','Settling'],note='Subtle idle pose study. Boots, shoulder breathing and cape closure still require final motion review.'),
 'lean_left':dict(label='Bank toward screen left',frames=[4,5,6,7],fps=12,phaseLabels=['Left support A','Left support B','Right support A','Right support B'],note='Two support-foot pairs for a left bank. Four-frame cadence, cape transitions and cross-source proportions remain review items.'),
 'lean_right':dict(label='Bank toward screen right',frames=[8,9,10,11],fps=12,phaseLabels=['Right support A','Right support B','Left support A','Left support B'],note='Separately drawn right bank, not a mirrored left bank. Four-frame cadence and cross-source proportions remain review items.')}

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def art_path(root,name):
    p=(root/name).resolve()
    if not p.is_relative_to((root/'art').resolve()):raise ValueError('Target outside art')
    return p

def matte(image,holes=()):
    image=image.convert('RGB');r,g,b=image.split()
    lo=ImageChops.darker(ImageChops.darker(r,g),b);hi=ImageChops.lighter(ImageChops.lighter(r,g),b)
    mask=ImageChops.multiply(lo.point(lambda x:255 if x>228 else 0),ImageChops.subtract(hi,lo).point(lambda x:255 if x<25 else 0))
    for seed in [(0,0),(image.width-1,0),(0,image.height-1),(image.width-1,image.height-1),*holes]:
        if mask.getpixel(tuple(seed))==255:ImageDraw.floodfill(mask,tuple(seed),128)
        elif seed in holes:raise ValueError('Negative-space annotation does not point at white')
    bg=mask.point(lambda v:255 if v==128 else 0);alpha=ImageChops.invert(bg)
    out=image.convert('RGBA');out.putalpha(alpha)
    outer=bg.filter(ImageFilter.MaxFilter(5));edge=ImageChops.multiply(outer,alpha)
    rgb=image.load();dst=out.load();core=outer.load();w,h=image.size
    offsets=sorted([(x,y) for x in range(-4,5) for y in range(-4,5) if x or y],key=lambda t:t[0]*t[0]+t[1]*t[1])
    for i,v in enumerate(edge.tobytes()):
        if v!=255:continue
        x,y=i%w,i//w;c=rgb[x,y]
        for dx,dy in offsets:
            xx,yy=x+dx,y+dy
            if 0<=xx<w and 0<=yy<h and core[xx,yy]==0:
                f=rgb[xx,yy];denom=sum((255-z)**2 for z in f)
                a=max(.02,min(1,sum((255-p)*(255-z) for p,z in zip(c,f))/max(denom,1)))
                if a<.995:dst[x,y]=(*[round(max(0,min(255,(p-255*(1-a))/a))) for p in c],round(a*255))
                break
    clean=Image.new('RGBA',out.size);clean.paste(out,(0,0),alpha) # binary alpha mask, no second fractional multiplication
    return clean

def clear_floor_plate(cut,ground_y):
    # Neutral shadows just below the sole are background, not sprite geometry.
    r,g,b,a=cut.split();lo=ImageChops.darker(ImageChops.darker(r,g),b);hi=ImageChops.lighter(ImageChops.lighter(r,g),b)
    neutral=ImageChops.multiply(lo.point(lambda x:255 if x>55 else 0),ImageChops.subtract(hi,lo).point(lambda x:255 if x<28 else 0))
    band=Image.new('L',cut.size);ImageDraw.Draw(band).rectangle((0,ground_y-6,cut.width,cut.height),fill=255)
    erase=ImageChops.multiply(neutral,band);cut.putalpha(ImageChops.subtract(a,erase))
    return cut

def register(image,scale,root):
    image=image.convert('RGBa').resize((round(image.width*scale),round(image.height*scale)),Image.Resampling.LANCZOS).convert('RGBA')
    x,y=round(256-root[0]*scale),round(576-root[1]*scale)
    b=image.getchannel('A').getbbox()
    if b is None:raise ValueError('Empty drawing')
    target=(b[0]+x,b[1]+y,b[2]+x,b[3]+y)
    if target[0]<3 or target[1]<3 or target[2]>509 or target[3]>637:raise ValueError('Clipped drawing: '+str(target))
    frame=Image.new('RGBA',(512,640));frame.paste(image,(x,y));return frame,[x,y]

def pack(frames):
    if len(frames)!=12:raise ValueError('This atlas requires 12 review frames')
    atlas=Image.new('RGBA',(1056,984));rects=[]
    for i,f in enumerate(frames):
        if f.size!=(256,320) or f.mode!='RGBA':raise ValueError('Expected 256x320 RGBA')
        x,y=(i%4)*264+4,(i//4)*328+4;atlas.paste(f,(x,y));rects.append([x,y,256,320])
    return atlas,rects

def font(n):
    p=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    return ImageFont.truetype(str(p),n) if p.exists() else ImageFont.load_default(size=n)

def board(frames):
    out=Image.new('RGB',(1160,1170),'#132e28');d=ImageDraw.Draw(out)
    d.text((25,20),'HULK JAMESY / IDLE + BANKING',font=font(27),fill='#eff5e9')
    d.text((25,60),'12 SELECTED DRAWINGS  /  REVIEW CANDIDATE',font=font(15),fill='#b2d491')
    labels=['REAR IDLE','BANK SCREEN LEFT','BANK SCREEN RIGHT']
    for i,f in enumerate(frames):
        col,row=i%4,i//4;x=col*290;y=95+row*352
        d.rounded_rectangle((x+8,y+4,x+282,y+345),radius=12,fill='#f9f6ef')
        out.paste(f,(x+17,y+5),f)
        d.text((x+18,y+325),labels[row]+' / '+str(col+1),font=font(12),fill='#264538')
    return out

def build(root=ROOT):
    folder=art_path(root,FOLDER);out=folder/'review-export';out.mkdir(exist_ok=True)
    sources=json.loads((folder/'sources.json').read_text())['sources'];source_map={s['file']:s for s in sources}
    sheets={}
    for name in SCALES:
        e=source_map[name];p=folder/name
        if e['status']!='archived' or digest(p)!=e['sha256']:raise ValueError('Source hash mismatch')
        with Image.open(p) as im:sheets[name]=im.convert('RGB')
    masters=[];runtime=[];records=[]
    for sub in ['frames-512','frames-256']:(out/sub).mkdir(exist_ok=True)
    for name,source,rect,anchor,holes in FRAMES:
        crop=sheets[source].crop(tuple(rect));cut=clear_floor_plate(matte(crop,holes),anchor[1])
        master,offset=register(cut,SCALES[source],anchor)
        small=master.convert('RGBa').resize((256,320),Image.Resampling.LANCZOS).convert('RGBA')
        for path,image in [(out/'frames-512'/f'{name}.png',master),(out/'frames-256'/f'{name}.png',small)]:image.save(path)
        masters.append(master);runtime.append(small)
        records.append(dict(id=name,source=source,sourceRect=rect,rootInCell=anchor,negativeSpaceSeeds=holes,
          commonSourceScale=SCALES[source],placement=offset,pivot=[.5,.9],frame512=f'frames-512/{name}.png',frame256=f'frames-256/{name}.png',productionReady=False))
    atlas,rects=pack(runtime);atlas.save(out/'atlas-review.png')
    for r,b in zip(records,rects):r['rect']=b
    manifest=dict(schemaVersion=1,id='movement-03',status='motion_review',productionReady=False,approvedByOwner=False,
      sourceFrameSize=[512,640],runtimeFrameSize=[256,320],pivot=[.5,.9],alpha='straight',trimmed=False,rotated=False,
      atlas='atlas-review.png',atlasSize=list(atlas.size),padding=4,mipmaps=False,clips=CLIPS,frames=records,
      sourceHashes={n:source_map[n]['sha256'] for n in SCALES},
      notes='12 selected review drawings from two sources, plus a preserved intermediate sheet. One scale per source and explicit placement; no mirroring, limb warping, physics or score changes. Final motion and camera approval pending.')
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    board(runtime).save(out/'contact-review.jpg',quality=92)
    data=dict(clips=CLIPS,pngs=['data:image/png;base64,'+base64.b64encode((out/r['frame256']).read_bytes()).decode() for r in records])
    template=(root/'production/tools/movement03_viewer.html').read_text()
    if template.count('__ASSET_DATA__')!=1:raise ValueError('Unexpected viewer template')
    (out/'review.html').write_text(template.replace('__ASSET_DATA__',json.dumps(data)))
    checks=[]
    for r in records:
        for key,expected in [('frame512',(512,640)),('frame256',(256,320))]:
            p=out/r[key]
            with Image.open(p) as im:
                a=im.getchannel('A');b=a.getbbox()
                assert im.mode=='RGBA' and im.size==expected and a.getextrema()==(0,255)
                assert b and b[0]>=2 and b[1]>=2 and b[2]<=im.width-2 and b[3]<=im.height-2
                checks.append(dict(file=r[key],sha256=digest(p),dimensions=list(im.size),alpha=[0,255],bounds=list(b)))
        x,y,w,h=r['rect'];f=Image.open(out/r['frame256']);assert atlas.crop((x,y,x+w,y+h)).tobytes()==f.tobytes()
    assert len(records)==12 and sum(len(c['frames']) for c in CLIPS.values())==12
    report=dict(result='PASS_FILE_CHECKS',individualPngExports=24,uniqueSelectedDrawings=12,atlasFrameChecks=12,
      productionReadyFrames=0,checks=checks,scope='Dimensions, alpha, no clipping, source hashes, atlas equality. Not a motion/likeness or physical-device approval.')
    (out/'technical-checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS:',len(records),'selected drawings;',len(checks),'PNG exports checked')
    return manifest
if __name__=='__main__':build()
