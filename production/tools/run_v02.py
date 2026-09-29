"""Export the new rear-run drawing study. Art-only; never reads game/account state.

Source PNGs are immutable. One common scale, explicit source anchors and a declared
playback permutation are used; no mirrored art, limb warping or hidden in-betweens.
Phase names are review targets, not a biomechanics certification.
"""
from pathlib import Path
import hashlib,json,base64,io
from PIL import Image,ImageChops,ImageDraw,ImageFilter

def remove_white(source, seeds=()):
    source=source.convert('RGB');r,g,b=source.split()
    low=ImageChops.darker(ImageChops.darker(r,g),b);hi=ImageChops.lighter(ImageChops.lighter(r,g),b)
    white=ImageChops.multiply(low.point(lambda v:255 if v>230 else 0),ImageChops.subtract(hi,low).point(lambda v:255 if v<22 else 0))
    for seed in [(0,0),*seeds]:
        if white.getpixel(seed)==255:ImageDraw.floodfill(white,seed,128)
    bg=white.point(lambda v:255 if v==128 else 0); alpha=ImageChops.invert(bg)
    outer=bg.filter(ImageFilter.MaxFilter(5));edge=ImageChops.multiply(outer,alpha)
    out=source.convert('RGBA');out.putalpha(alpha)
    rgb=source.load();dest=out.load();inside=outer.load();w,h=source.size
    offs=sorted([(dx,dy) for dy in range(-4,5) for dx in range(-4,5) if dx or dy],key=lambda d:d[0]**2+d[1]**2)
    for k,v in enumerate(edge.tobytes()):
        if v!=255:continue
        x,y=k%w,k//w;c=rgb[x,y]
        for dx,dy in offs:
            xx,yy=x+dx,y+dy
            if 0<=xx<w and 0<=yy<h and inside[xx,yy]==0:
                f=rgb[xx,yy];denom=sum((255-v)**2 for v in f)
                a=min(1,max(.02,sum((255-cv)*(255-fv) for cv,fv in zip(c,f))/max(1,denom)))
                if a<.995:dest[x,y]=(*[round(max(0,min(255,(cv-255*(1-a))/a))) for cv in c],round(a*255))
                break
    blank=Image.new('RGBA',out.size);blank.paste(out,(0,0),alpha)
    return blank

ROOT=Path(__file__).resolve().parents[2]
REL='art/01-characters/hulk/run-reviews/v02'
SOURCE_SHA='a15c2083fd81d46076cd8cb24e2bc0ccdd602cb58b9f637c5517736d7c86d9aa'
SOURCE_ORDER=[4,5,2,3,0,1,6,7]
LABELS=['Left contact','Left compression','Left toe-off','Flight to right','Right contact','Right compression','Right toe-off','Flight to left']
ANCHORS_X=[358,338,299,273,364,334,294,273]
HOLES={2:[(216,513)],4:[(269,294)],5:[(457,389),(487,438),(237,289)],7:[(170,284)]}
SCALE=.59

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def safe_path(root,relative):
    p=(root/relative).resolve()
    if not p.is_relative_to((root/'art').resolve()):raise ValueError('Write must stay in artwork folder')
    return p

def resized(im,size):
    return im.convert('RGBa').resize(size,Image.Resampling.LANCZOS).convert('RGBA')

def register(cell,source_cell,flight=False):
    alpha=remove_white(cell,HOLES.get(source_cell,()))
    ground=828 if source_cell<4 else 781
    # Remove the small neutral-gray plate shadow at the ground, not colored boot pixels.
    px=alpha.load()
    for y in range(ground-10,cell.height):
        for x in range(cell.width):
            r,g,b,a=px[x,y]
            if a and min(r,g,b)>115 and max(r,g,b)-min(r,g,b)<26:px[x,y]=(0,0,0,0)
    part=resized(alpha,(round(640*SCALE),round(856*SCALE)))
    shift=-12 if flight else 0
    offset=(round(256-ANCHORS_X[source_cell]*SCALE),round(576-ground*SCALE)+shift)
    bounds=part.getchannel('A').getbbox()
    if not bounds:raise ValueError('Blank drawing')
    placed=[bounds[0]+offset[0],bounds[1]+offset[1],bounds[2]+offset[0],bounds[3]+offset[1]]
    if placed[0]<2 or placed[1]<2 or placed[2]>510 or placed[3]>638:raise ValueError('Drawing would be clipped')
    out=Image.new('RGBA',(512,640));out.paste(part,offset)
    return out,offset,shift

def pack(frames):
    if len(frames)!=8 or any(im.mode!='RGBA' or im.size!=(256,320) for im in frames):raise ValueError('Expected eight RGBA runtime frames')
    atlas=Image.new('RGBA',(1056,656));rects=[]
    for i,im in enumerate(frames):
        x=(i%4)*264+4;y=(i//4)*328+4
        atlas.paste(im,(x,y));rects.append([x,y,256,320])
    return atlas,rects

def font(size):
    from PIL import ImageFont
    p=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    return ImageFont.truetype(str(p),size) if p.exists() else ImageFont.load_default(size=size)

def contact(frames):
    out=Image.new('RGB',(1168,864),'#183b32');d=ImageDraw.Draw(out)
    d.text((24,16),'HULK JAMESY / REAR RUN 02',font=font(28),fill='#f9f6eb')
    d.text((24,59),'8 new drawing candidates • phase-ordered review • not yet production-approved',font=font(16),fill='#c0dbad')
    for i,im in enumerate(frames):
        x=(i%4)*292+18;y=104+(i//4)*370
        plate=Image.new('RGBA',(256,320),'#17342d');plate.alpha_composite(im)
        out.paste(plate.convert('RGB'),(x,y))
        d.text((x,y+327),f'{i+1:02} / {LABELS[i]}',font=font(15),fill='#f5f4ed')
        d.text((x,y+350),f'Source cell {SOURCE_ORDER[i]+1} • no mirroring',font=font(12),fill='#a8c2b4')
    return out

def flipbook(frames,path):
    plates=[]
    for i,im in enumerate(frames):
        p=Image.new('RGBA',(620,412),'#173a31');d=ImageDraw.Draw(p)
        d.text((20,12),'HULK JAMESY / RUN 02',font=font(20),fill='#f8f5ec')
        for x,color in [(20,'#112820'),(336,'#faf7f0')]:
            tile=Image.new('RGBA',(256,320),color);tile.alpha_composite(im);p.alpha_composite(tile,(x,56))
        d.text((20,384),f'{i+1:02}/08  {LABELS[i]}  •  Review candidate',font=font(15),fill='#c3dcb1')
        plates.append(p.convert('RGB'))
    plates[0].save(path,save_all=True,append_images=plates[1:],duration=[80,90,80,80,90,80,80,90],loop=0,disposal=2)

def viewer(atlas_bytes,old_bytes,rects):
    data={'new':'data:image/png;base64,'+base64.b64encode(atlas_bytes).decode(),'old':'data:image/png;base64,'+base64.b64encode(old_bytes).decode(),'rects':rects,'labels':LABELS,'sourceOrder':SOURCE_ORDER}
    template=ROOT/'production/tools/run_review_v02.html'
    return template.read_text().replace('/* EMBED_DATA */',json.dumps(data))

def build(root=ROOT):
    global ROOT
    ROOT=root
    folder=safe_path(root,REL);source=folder/'source-sheet.png'
    if digest(source)!=SOURCE_SHA:raise ValueError('Unexpected revision source')
    before=digest(source)
    old_atlas=root/'art/01-characters/hulk/run-reviews/v01/review-export/atlas-review.png'
    old_before=digest(old_atlas)
    with Image.open(source) as im:
        if im.mode!='RGB' or im.size!=(2560,1712):raise ValueError('Unexpected source format')
        sheet=im.copy()
    out=folder/'review-export'
    for sub in ['frames-512','frames-256']: (out/sub).mkdir(parents=True,exist_ok=True)
    frames=[];records=[]
    for frame_id,cell_id in enumerate(SOURCE_ORDER):
        x=(cell_id%4)*640;y=(cell_id//4)*856;rect=[x,y,x+640,y+856]
        master,offset,shift=register(sheet.crop(tuple(rect)),cell_id,frame_id in (3,7))
        small=resized(master,(256,320));frames.append(small)
        name=f'hulk_run_rear_{frame_id:03}'
        master.save(out/'frames-512'/f'{name}.png');small.save(out/'frames-256'/f'{name}.png')
        records.append({'id':name,'sourceCell':cell_id,'sourceRect':rect,'phaseTarget':LABELS[frame_id],
            'sourceGroundAnchor':[ANCHORS_X[cell_id],828 if cell_id<4 else 781], 'commonSheetScale':SCALE,
            'offset':list(offset),'presentationFlightOffsetY':shift,'pivot':[.5,.9],
            'frame512':f'frames-512/{name}.png','frame256':f'frames-256/{name}.png',
            'sha256':digest(out/'frames-256'/f'{name}.png'),'productionReady':False})
    atlas,rects=pack(frames);atlas.save(out/'atlas-review.png')
    for r,rect in zip(records,rects):r['rect']=rect
    manifest={'schemaVersion':1,'id':'run-v02','status':'motion_review','productionReady':False,
        'source':f'{REL}/source-sheet.png','sourceSha256':SOURCE_SHA,'sourceFrameSize':[512,640],'runtimeFrameSize':[256,320],
        'originalSheetSize':[2560,1712],'pivot':[.5,.9],'atlas':'atlas-review.png','atlasSize':[1056,656],'padding':4,
        'alpha':'straight','trimmed':False,'rotated':False,'mipmaps':False,'frames':records,
        'playbackSourceCells':SOURCE_ORDER,'previewFps':12,'uniqueDrawingCount':8,
        'notes':'Newly generated toe-off and tucked-leg drawings are phase-ordered as source cells 5,6,3,4,1,2,7,8 (one-based). This is not a relabel of v01. Two flight frames have a declared -12 master-pixel presentation offset. No mirrored artwork, limb warping, head replacement or interpolated frames. Cape timing, proportional continuity and final camera alignment still need approval.'}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    contact(frames).save(out/'contact-review.jpg',quality=92)
    flipbook(frames,out/'run-proof.gif')
    (out/'review.html').write_text(viewer((out/'atlas-review.png').read_bytes(),old_atlas.read_bytes(),rects))
    checks=[]
    assert sorted(SOURCE_ORDER)==list(range(8));checks.append('Eight unique source cells used exactly once')
    assert before==digest(source) and old_before==digest(old_atlas);checks.append('Original source and v01 atlas remain unchanged')
    for r in records:
        for key,size in [('frame512',(512,640)),('frame256',(256,320))]:
            with Image.open(out/r[key]) as im:
                assert im.mode=='RGBA' and im.size==size
                alpha=im.getchannel('A');bounds=alpha.getbbox()
                assert alpha.getextrema()==(0,255) and bounds and min(bounds[:2])>=2 and bounds[2]<=size[0]-2 and bounds[3]<=size[1]-2
    checks.extend(['All 16 individual PNG exports have the stated fixed canvas','All exports have transparent and opaque pixels','All silhouettes remain within the canvas'])
    for frame,r in zip(frames,records):
        x,y,w,h=r['rect'];assert atlas.crop((x,y,x+w,y+h)).tobytes()==frame.tobytes()
        assert digest(out/r['frame256'])==r['sha256']
    checks.extend(['Atlas copies preserve straight-alpha pixels','Runtime checksums match manifest'])
    assert len({r['commonSheetScale'] for r in records})==1;checks.append('One common scale across the new sheet')
    assert all(r['presentationFlightOffsetY']==(-12 if i in(3,7) else 0) for i,r in enumerate(records));checks.append('Two cosmetic flight offsets are explicitly recorded')
    assert not manifest['productionReady'];checks.append('Production approval is not inferred from file generation')
    with Image.open(out/'run-proof.gif') as gif:assert gif.n_frames==8
    checks.append('Flipbook contains all eight frames')
    report={'result':'PASS_TECHNICAL_ONLY','checks':checks,'checkCount':len(checks),'uniqueNewDrawingCandidates':8,'individualPngExports':16,'productionApprovedFrames':0,'motionApproval':'pending','scope':'File and export checks only; no claim of final animation quality, physical iPhone behavior or gameplay testing.'}
    (out/'technical-checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2));return manifest,report

if __name__=='__main__':build()
