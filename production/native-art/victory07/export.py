"""Process an explicitly uploaded Victory 07 source. No image service or game access.

Requires Pillow, numpy and scipy. This is candidate matte/export processing only.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi

SOURCE_SIZE=(1536,1024)
SOURCE_HASH='3f2921e57c786f94ab0ef52db946fd123ea5204b39ac6bcdf95aad9c0d326226'
ROOT=(166.0,475.0)
PIVOT=(256,576)
SCALE=1.1
PHASES=['Ready','Anticipate','Fist rises','Celebrate','Peak hold','Lower fist','Recover','Ready again']

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def isolate_white(image):
    rgb=np.asarray(image.convert('RGB'),dtype=np.float64)
    neutral=(rgb.min(axis=2)>=235)&((rgb.max(axis=2)-rgb.min(axis=2))<=20)
    seeds=np.zeros(neutral.shape,dtype=bool)
    seeds[0,:]=neutral[0,:];seeds[-1,:]=neutral[-1,:]
    seeds[:,0]=neutral[:,0];seeds[:,-1]=neutral[:,-1]
    background=ndi.binary_propagation(seeds,mask=neutral)
    fg=~background
    labels,n=ndi.label(fg)
    if n:
        areas=np.bincount(labels.ravel());good=areas>=20;good[0]=False;fg=good[labels]
    if not fg.any():raise ValueError('No figure detected')
    core=ndi.binary_erosion(fg,iterations=2)
    if not core.any():raise ValueError('No reliable foreground interior')
    expanded=ndi.binary_dilation(fg,iterations=2);edge=expanded&~core
    nearest=ndi.distance_transform_edt(~core,return_distances=False,return_indices=True)
    interior=rgb[nearest[0],nearest[1]];delta=interior-255.0
    denom=np.sum(delta*delta,axis=2)
    coverage=np.clip(np.sum((rgb-255.0)*delta,axis=2)/np.maximum(denom,1),0,1)
    alpha=np.where(core,1.0,np.where(edge,coverage,0.0));alpha[alpha<.025]=0
    color=rgb.copy();partial=edge&(alpha>0)&(alpha<1)
    color[partial]=(rgb[partial]-255.0*(1-alpha[partial,None]))/alpha[partial,None]
    color[alpha==0]=0
    rgba=np.concatenate([np.clip(color,0,255),(alpha*255)[...,None]],axis=2)
    return Image.fromarray(np.round(rgba).astype('uint8'))

def register(image):
    size=(round(image.width*SCALE),round(image.height*SCALE))
    resized=image.resize(size,Image.Resampling.LANCZOS)
    position=(round(PIVOT[0]-ROOT[0]*SCALE),round(PIVOT[1]-ROOT[1]*SCALE))
    result=Image.new('RGBA',(512,640));result.paste(resized,position)
    return result

def font(size,bold=False):
    for base in ['/usr/share/fonts/truetype/dejavu','/usr/share/fonts/truetype/liberation2']:
        name='DejaVuSans' if 'dejavu' in base else 'LiberationSans'
        path=Path(base)/(name+('-Bold' if bold else '')+'.ttf')
        if path.exists():return ImageFont.truetype(str(path),size)
    return ImageFont.load_default()

def contact_board(frames,out):
    board=Image.new('RGB',(1440,1080),'#faf7f0');d=ImageDraw.Draw(board)
    d.rectangle((0,0,1440,130),fill='#153c35')
    d.text((35,25),'HULK JAMESY  /  VICTORY 07',font=font(34,True),fill='white')
    d.text((35,78),'Eight selected pose candidates  |  Existing conversation source  |  Not production-approved',font=font(18),fill='#cbe8c5')
    for i,frame in enumerate(frames):
        x=24+(i%4)*354;y=150+(i//4)*425
        d.rounded_rectangle((x,y,x+336,y+406),radius=16,fill='white',outline='#d6ded8',width=2)
        display=frame.resize((264,330),Image.Resampling.LANCZOS);board.paste(display,(x+36,y+14),display)
        d.text((x+17,y+359),f'{i+1:02d}  {PHASES[i]}',font=font(18,True),fill='#153c35')
        d.text((x+17,y+383),f'Frame {i:03d}  /  Front three-quarter',font=font(13),fill='#5b6861')
    d.text((35,1037),'J chest + belt  •  Body art only  •  Source order retained  •  Motion and matte review remain open',font=font(17),fill='#153c35')
    board.save(out/'victory-contact-board.jpg',quality=92)

def export(source,out):
    if not source.is_file() or digest(source)!=SOURCE_HASH:
        raise ValueError('Upload the exact original Victory 07 source; no substitute or synthesized asset is accepted')
    with Image.open(source) as im:
        if im.size!=SOURCE_SIZE or im.format!='PNG':raise ValueError('Incorrect original PNG dimensions')
        original=im.convert('RGB')
    out.mkdir(parents=True,exist_ok=True)
    (out/'frames-512').mkdir(exist_ok=True);(out/'frames-256').mkdir(exist_ok=True)
    frames=[];entries=[];atlas=Image.new('RGBA',(2048,2048))
    for i in range(8):
        col,row=i%4,i//4;rect=(col*384,row*512,(col+1)*384,(row+1)*512)
        frame=register(isolate_white(original.crop(rect)))
        name=f'hulk_victory_front3q_{i:03d}.png'
        master=out/'frames-512'/name;runtime=out/'frames-256'/name
        runtime_img=frame.resize((256,320),Image.Resampling.LANCZOS)
        frame.save(master,optimize=True);runtime_img.save(runtime,optimize=True)
        x=(i%7)*264+4;y=(i//7)*328+4;atlas.paste(runtime_img,(x,y))
        entries.append({'id':f'victory_{i:03d}','sourceIndex':i,'phase':PHASES[i],
            'sourceRect':[rect[0],rect[1],384,512],'sourceRoot':list(ROOT),'scale':SCALE,
            'pivot':[.5,.9],'size512':[512,640],'master':f'frames-512/{name}',
            'runtime':f'frames-256/{name}','masterSha256':digest(master),
            'runtimeSha256':digest(runtime),'atlasRect':[x,y,256,320]})
        frames.append(frame)
    atlas.save(out/'victory-atlas.png',optimize=True)
    result={'schemaVersion':1,'batch':'Victory 07','hero':'hulk','clip':'victory',
        'status':'candidate_review','productionReady':False,'sourceSha256':digest(source),
        'sourceDimensions':list(SOURCE_SIZE),'sourceType':'existing_conversation_image',
        'generationThisBatch':False,'sourceResolutionNote':'384x512 source cells; registered 512x640 output is not new image detail.',
        'canvas':[512,640],'runtimeCanvas':[256,320],'pivot':[.5,.9],
        'registration':{'scale':SCALE,'sourceRoot':list(ROOT),'perPoseFit':False,'mirrored':False,'interpolated':False},
        'clips':[{'id':'victory','fps':10,'loop':False,'view':'front_three_quarter','frames':[e['id'] for e in entries]}],
        'atlas':{'file':'victory-atlas.png','width':2048,'height':2048,'padding':4,'rgbaBytes':16777216,'mipmaps':False,'origin':'top-left','colorSpace':'srgb','alpha':'straight'},
        'frames':entries,'reviewNotes':['Original drawings preserved in reading order.','One scale and source root; no per-pose fitting or mirroring.','Matte edges, enclosed gaps, body proportions and motion need visual review.','Artwork never triggers game, score or account events.']}
    (out/'manifest.json').write_text(json.dumps(result,indent=2)+'\n')
    (out/'manifest.js').write_text('window.VICTORY07 = '+json.dumps(result)+';\n')
    contact_board(frames,out)
    preview=[]
    for frame in frames:
        bg=Image.new('RGBA',(320,400),'#faf7f0');bg.alpha_composite(frame.resize((320,400),Image.Resampling.LANCZOS));preview.append(bg.convert('RGB'))
    preview[0].save(out/'victory-preview.webp',save_all=True,append_images=preview[1:],duration=[100]*7+[1100],loop=1,quality=90,method=6)
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',required=True,type=Path);parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args()
    try:result=export(args.source,args.out)
    except (ValueError,OSError) as error:parser.exit(2,f'Export stopped: {error}\n')
    print(f"Exported {len(result['frames'])} candidate drawings; no production approval implied")
