"""Deterministic candidate sprite extraction. No generated motion or game/account access.

Only two checksummed sources are read. Writes stay in their fixed review-export
folders. Common scale per sheet, explicit root annotations, no mirrors/warps.
Pillow is the only dependency. These exports are NOT production approval.
"""
from __future__ import annotations
import base64
import hashlib
import html
import json
import math
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
HERO = 'art/01-characters/hulk'
SPECS = [
    {'id': 'poses-v02', 'source': f'{HERO}/pose-reviews/hulk-six-pose-v02-source.png',
     'sha256': 'a88cd96b65d272a646b9300e1edef4ba3388c0d8cdc0a5ea2a41a4439291a47a',
     'out': f'{HERO}/pose-reviews/v02-cutouts', 'scale': .53,
     'holes': [[1118,551],[262,501],[2194,1491],[2297,1601]],
     'status': 'pose_review',
     'frames': [
         ('front_stance', [160,6,846,884], [376,875], 'front'),
         ('rear_stance', [1040,15,1570,884], [1270,875], 'rear'),
         ('rear_run_key', [1785,44,2416,880], [2178,885], 'rear'),
         ('bank_screen_right', [47,889,733,1694], [326,1685], 'rear'),
         ('bank_screen_left', [972,888,1670,1678], [1345,1668], 'rear'),
         ('rear_smash_contact', [1812,984,2495,1673], [2190,1664], 'rear_three_quarter')],
     'note': 'Six cleaned pose studies. Front stance is near frontal, not a verified three-quarter camera. Bank names describe actual screen direction. Source/body construction and final track-camera registration still need review.'},
    {'id':'run-v01', 'source':f'{HERO}/run-reviews/v01/source-sheet.png',
     'sha256':'fe9cb4356404185535e410ff3e60c1cd2ab6b1061a48875ddb6ddd9519f74ef9',
     'out': f'{HERO}/run-reviews/v01/review-export', 'scale':.63,
     'holes':[[966,575]], 'status':'motion_needs_revision',
     'frames':[(f'hulk_run_rear_{i:03d}',[(i%4)*640,(i//4)*856,(i%4+1)*640,(i//4+1)*856],
                [[337,790],[978,790],[1577,790],[2208,790],[334,1614],[977,1614],[1577,1614],[2208,1614]][i], 'rear') for i in range(8)],
     'note':'Source order is intentionally unchanged. Several contact drawings repeat rather than forming the requested contact/down/passing/up stride. Frame 003 is a symmetric airborne pose; cadence, arm swing, head scale and cape continuity need correction. This viewer diagnoses the source, it does not create missing animation.'}
]


def safe_art_path(root: Path, name: str) -> Path:
    result=(root/name).resolve()
    if not result.is_relative_to((root/'art').resolve()):
        raise ValueError('Path is outside the artwork library')
    return result


def remove_white_matte(source: Image.Image, hole_seeds: list[list[int]]) -> Image.Image:
    """Remove exterior white and annotated negative spaces, preserving enclosed J/eyes.

    Source-specific white plate, not a general-purpose segmentation model.
    Boundary pixels are decontaminated against nearby interior colors.
    """
    source=source.convert('RGB')
    r,g,b=source.split()
    low=ImageChops.darker(ImageChops.darker(r,g),b)
    high=ImageChops.lighter(ImageChops.lighter(r,g),b)
    white=ImageChops.multiply(low.point(lambda v:255 if v>230 else 0),
                             ImageChops.subtract(high,low).point(lambda v:255 if v<22 else 0))
    for seed in [[0,0],*hole_seeds]:
        seed=tuple(seed)
        if not (0<=seed[0]<source.width and 0<=seed[1]<source.height):
            raise ValueError('Mask seed outside image')
        if white.getpixel(seed)!=255:
            raise ValueError(f'Mask seed {seed} is not white background; inspect source')
        ImageDraw.floodfill(white,seed,128)
    bg=white.point(lambda v:255 if v==128 else 0)
    silhouette=ImageChops.invert(bg)
    expanded=bg.filter(ImageFilter.MaxFilter(5))
    edge=ImageChops.multiply(expanded,silhouette)
    result=source.convert('RGBA');result.putalpha(silhouette)
    rgb=source.load();out=result.load();core=expanded.load();w,h=source.size
    offsets=sorted([(dx,dy) for dy in range(-4,5) for dx in range(-4,5) if dx or dy],
                   key=lambda d:d[0]*d[0]+d[1]*d[1])
    # Use a narrow foreground boundary only. Never blur the silhouette/lettering.
    for index,value in enumerate(edge.tobytes()):
        if value!=255: continue
        x,y=index%w,index//w
        color=rgb[x,y]
        for dx,dy in offsets:
            xx,yy=x+dx,y+dy
            if 0<=xx<w and 0<=yy<h and core[xx,yy]==0:
                f=rgb[xx,yy];denom=sum((255-v)**2 for v in f)
                a=min(1.,max(.02,sum((255-c)*(255-v) for c,v in zip(color,f))/max(1,denom)))
                # Opaque borders remain unchanged; semi-transparent boundaries unmatte.
                if a<.995:
                    corrected=tuple(round(max(0,min(255,(c-255*(1-a))/a))) for c in color)
                    out[x,y]=(*corrected,round(a*255))
                break
    # Avoid carrying a white RGB plate under fully transparent pixels.
    blank=Image.new('RGBA',source.size)
    blank.paste(result,(0,0),silhouette)
    return blank


def frame_export(sheet: Image.Image, rect: list[int], root: list[int], scale: float) -> Image.Image:
    x0,y0,x1,y1=rect
    if not (0<=x0<x1<=sheet.width and 0<=y0<y1<=sheet.height): raise ValueError('Invalid source rectangle')
    crop=sheet.crop(tuple(rect))
    size=(round(crop.width*scale),round(crop.height*scale))
    crop=crop.resize(size,Image.Resampling.LANCZOS)
    pos=(round(256-(root[0]-x0)*scale),round(576-(root[1]-y0)*scale))
    bb=crop.getchannel('A').getbbox()
    if bb is None: raise ValueError('Blank frame')
    placed=(bb[0]+pos[0],bb[1]+pos[1],bb[2]+pos[0],bb[3]+pos[1])
    if placed[0]<2 or placed[1]<2 or placed[2]>510 or placed[3]>638:
        raise ValueError(f'Frame clips the fixed canvas: {placed}')
    output=Image.new('RGBA',(512,640));output.paste(crop,pos)
    return output


def pack_runtime(frames: list[Image.Image]) -> tuple[Image.Image,list[list[int]]]:
    if not frames: raise ValueError('No frames')
    atlas=Image.new('RGBA',(1056,math.ceil(len(frames)/4)*328));rects=[]
    for i,frame in enumerate(frames):
        if frame.mode!='RGBA' or frame.size!=(256,320):raise ValueError('Expected 256x320 RGBA frame')
        x=(i%4)*264+4;y=(i//4)*328+4
        atlas.paste(frame,(x,y)) # Never apply alpha twice.
        rects.append([x,y,256,320])
    return atlas,rects


def font(size: int):
    path=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    return ImageFont.truetype(str(path),size) if path.exists() else ImageFont.load_default(size=size)


def contact_board(frames: list[Image.Image], names: list[str], title: str) -> Image.Image:
    cols=4 if len(frames)==8 else 3;cellw=290;cellh=357
    out=Image.new('RGB',(cols*cellw,92+2*cellh),(19,42,38));d=ImageDraw.Draw(out)
    d.text((24,18),title,font=font(26),fill=(239,247,232))
    d.text((24,53),'REVIEW CANDIDATE  |  transparent cutouts  |  not a finished animation',font=font(14),fill=(183,208,193))
    for i,frame in enumerate(frames):
        x=i%cols*cellw;y=92+i//cols*cellh
        d.rounded_rectangle((x+8,y+4,x+cellw-8,y+cellh-6),radius=12,fill=(235,238,228))
        mini=frame.resize((256,320),Image.Resampling.LANCZOS)
        out.paste(mini,(x+17,y+8),mini)
        d.text((x+17,y+326),names[i].replace('_',' '),font=font(13),fill=(30,57,47))
    return out


def review_html(atlas: Image.Image, manifest: dict, png: bytes) -> str:
    frames=manifest['frames']; rects=[f['rect'] for f in frames]
    labels=[f['id'] for f in frames]
    data=json.dumps({'rects':rects,'labels':labels,'src':'data:image/png;base64,'+base64.b64encode(png).decode()})
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Hulk Jamesy · Character review</title><style>
    *{box-sizing:border-box}body{margin:0;background:#132a26;color:#f3f8ed;font:16px system-ui;padding:24px}main{max-width:1000px;margin:auto}h1{font-size:clamp(25px,5vw,40px);margin:.4em 0}p{line-height:1.55;color:#c3d6c8}small{color:#beed97}.badge{display:inline-block;padding:7px 12px;background:#583881;border-radius:30px;font-size:12px;letter-spacing:1px}.layout{display:grid;grid-template-columns:minmax(0,1fr) minmax(220px,320px);gap:24px}section,aside{min-width:0}aside{padding:20px;border:1px solid #436355;border-radius:18px}label{display:block;margin:14px 0 6px}button,select{font:inherit;color:inherit;background:#2a5142;border:1px solid #74967b;border-radius:9px;padding:11px;min-height:44px;cursor:pointer}button:focus-visible,select:focus-visible,input:focus-visible{outline:3px solid #d3b4ff;outline-offset:3px}.controls{display:flex;gap:8px;flex-wrap:wrap}input{width:100%;accent-color:#b6ec7a}.stage{background:#f5f2ea;border-radius:18px;min-height:430px;display:grid;place-items:center;overflow:hidden}.stage[data-bg=dark]{background:#111820}.stage[data-bg=checker]{background-color:#e0e3d9;background-image:conic-gradient(#b8bfb4 25%,transparent 0 50%,#b8bfb4 0 75%,transparent 0);background-size:32px 32px}canvas{max-width:100%;height:auto}#frameLabel{color:#b6ec7a;font-variant-numeric:tabular-nums}.note{border-left:3px solid #b68bdd;padding-left:14px}a{color:#b6ec7a}@media(max-width:650px){body{padding:16px}.layout{grid-template-columns:1fr}.stage{min-height:340px}}
    </style></head><body><main><span class="badge">GROUP 1 / CHARACTER ART</span><h1>Hulk Jamesy · '''+html.escape(manifest['id'])+'''</h1><p>Existing drawings played as sprite frames. No generated video, no game connection, no account access. Playback is paused when opened.</p><div class="layout"><section><div class="stage" id="stage" data-bg="dark"><canvas id="canvas" width="512" height="640" aria-label="Selected transparent character frame"></canvas></div><p id="frameLabel" role="status"></p></section><aside><small>REVIEW ONLY · NOT PRODUCTION-READY</small><label for="frame">Frame</label><input id="frame" type="range" min="0" max="'''+str(len(frames)-1)+'''" value="0" step="1"><div class="controls"><button id="previous" aria-label="Previous frame">←</button><button id="play">Play frames</button><button id="next" aria-label="Next frame">→</button></div><label for="speed">Playback speed</label><select id="speed"><option value="6">6 fps · slow review</option><option value="12" selected>12 fps · planned run</option><option value="16">16 fps · fast run study</option></select><label for="background">Background</label><select id="background"><option value="dark">Dark</option><option value="light">Light</option><option value="checker">Checkerboard</option></select><label for="displaySize">Character canvas height</label><select id="displaySize"><option value="320">320 px · detail</option><option value="180">180 px · gameplay study</option><option value="120">120 px · small study</option></select><label><input style="width:auto" type="checkbox" id="anchor" checked> Show proposed ground anchor</label><p class="note">'''+html.escape(manifest['notes'])+'''</p><p>Arrow keys step frames. Space plays or pauses. Source order is unchanged: errors stay visible for review.</p></aside></div></main><script>
    const data='''+data+''';const $=s=>document.getElementById(s),c=$('canvas'),ctx=c.getContext('2d'),image=new Image();let index=0,playing=false,last=0;function draw(){ctx.clearRect(0,0,512,640);const r=data.rects[index];ctx.drawImage(image,...r,0,0,512,640);if($('anchor').checked){ctx.strokeStyle='#b969fa';ctx.lineWidth=2;ctx.setLineDash([7,7]);ctx.beginPath();ctx.moveTo(0,576);ctx.lineTo(512,576);ctx.stroke();ctx.setLineDash([]);ctx.beginPath();ctx.moveTo(242,576);ctx.lineTo(270,576);ctx.moveTo(256,562);ctx.lineTo(256,590);ctx.stroke()}$('frame').value=index;$('frameLabel').textContent=`${index+1} / ${data.rects.length} · ${data.labels[index]}`}function pause(){playing=false;$('play').textContent='Play frames'}function step(n){pause();index=(index+n+data.rects.length)%data.rects.length;draw()}function toggle(){playing=!playing;last=performance.now();$('play').textContent=playing?'Pause':'Play frames'}$('previous').onclick=()=>step(-1);$('next').onclick=()=>step(1);$('play').onclick=toggle;$('frame').oninput=e=>{pause();index=Number(e.target.value);draw()};$('anchor').onchange=draw;$('background').onchange=e=>$('stage').dataset.bg=e.target.value;$('displaySize').onchange=e=>{c.style.height=e.target.value+'px';c.style.width=(Number(e.target.value)*.8)+'px'};$('displaySize').dispatchEvent(new Event('change'));image.onload=()=>{draw();window.__reviewReady=true};image.src=data.src;function tick(t){if(playing&&t-last>=1000/Number($('speed').value)){index=(index+1)%data.rects.length;last=t;draw()}requestAnimationFrame(tick)}requestAnimationFrame(tick);document.addEventListener('visibilitychange',()=>{if(document.hidden)pause()});document.addEventListener('keydown',e=>{if(['INPUT','SELECT','BUTTON'].includes(e.target.tagName))return;if(e.code==='Space'){e.preventDefault();toggle()}if(e.code==='ArrowRight'){e.preventDefault();step(1)}if(e.code==='ArrowLeft'){e.preventDefault();step(-1)}});
    </script></body></html>'''


def build(root: Path = ROOT) -> list[dict]:
    summaries=[]
    for spec in SPECS:
        source=safe_art_path(root,spec['source']);raw=source.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=spec['sha256']:raise ValueError('Unexpected source checksum')
        with Image.open(source) as image:
            if image.size!=(2560,1712) or image.mode!='RGB':raise ValueError('Unexpected source format')
            rgba=remove_white_matte(image,spec['holes'])
        out=safe_art_path(root,spec['out']);(out/'frames-512').mkdir(parents=True,exist_ok=True);(out/'frames-256').mkdir(exist_ok=True)
        master=[];runtime=[];records=[]
        for name,rect,anchor,view in spec['frames']:
            frame=frame_export(rgba,rect,anchor,spec['scale']);small=frame.resize((256,320),Image.Resampling.LANCZOS)
            frame.save(out/'frames-512'/f'{name}.png');small.save(out/'frames-256'/f'{name}.png')
            master.append(frame);runtime.append(small)
            records.append({'id':name,'view':view,'sourceRect':rect,'sourceGroundAnchor':anchor,'commonSheetScale':spec['scale'],'pivot':[.5,.9],'frame512':f'frames-512/{name}.png','frame256':f'frames-256/{name}.png','productionReady':False})
        atlas,rects=pack_runtime(runtime);atlas.save(out/'atlas-review.png')
        for record,rect in zip(records,rects):record['rect']=rect
        manifest={'schemaVersion':1,'id':spec['id'],'status':spec['status'],'productionReady':False,'source':spec['source'],'sourceSha256':spec['sha256'],'sourceFrameSize':[512,640],'runtimeFrameSize':[256,320],'pivot':[.5,.9],'alpha':'straight','atlas':'atlas-review.png','atlasSize':list(atlas.size),'padding':4,'trimmed':False,'rotated':False,'notes':spec['note'],'frames':records}
        (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        (out/'review.html').write_text(review_html(atlas,manifest,(out/'atlas-review.png').read_bytes()))
        contact_board(master,[f['id'] for f in records],'HULK JAMESY / '+spec['id'].upper()).save(out/'contact-review.jpg',quality=92)
        checks=[]
        for record in records:
            for key in ['frame512','frame256']:
                path=out/record[key]
                with Image.open(path) as im:
                    alpha=im.getchannel('A');ext=alpha.getextrema();bbox=alpha.getbbox()
                    if ext!=(0,255) or not bbox or bbox[0]<2 or bbox[1]<2 or bbox[2]>im.width-2 or bbox[3]>im.height-2:raise ValueError(f'Alpha/clipping check failed: {path.name}')
                    checks.append({'path':path.relative_to(root).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'size':list(im.size),'alphaExtrema':list(ext),'bbox':list(bbox)})
        summary={'id':spec['id'],'technicalResult':'PASS','visualStatus':spec['status'],'uniqueReviewDrawings':len(records),'productionReadyFrames':0,'checks':checks,'scope':'File dimensions, alpha range, nonempty silhouette, canvas bounds, source hash. Not approval of motion, likeness, track alignment or physical-device behavior.'}
        (out/'technical-checks.json').write_text(json.dumps(summary,indent=2)+'\n');summaries.append(summary)
        print(f"{spec['id']}: {len(records)} review drawings, alpha/canvas checks PASS; production ready = 0")
    return summaries

if __name__=='__main__':build()
