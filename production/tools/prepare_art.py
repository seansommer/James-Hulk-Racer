"""Build reference extracts, an honest inventory and local gallery. No game integration."""
from pathlib import Path
from PIL import Image
import html, json, hashlib
ROOT=Path(__file__).resolve().parents[2]
HEROES=['hulk','spider','captain','iron','super']

def prepare():
    src=ROOT/'art/00-reference/lineup-j-v1.png'
    with Image.open(src) as original: im=original.convert('RGB')
    im.save(src.with_suffix('.webp'),quality=90,method=6)
    for i,hero in enumerate(HEROES):
        folder=ROOT/f'art/01-characters/{hero}/references';folder.mkdir(parents=True,exist_ok=True)
        crop=im.crop((round(im.width*i/5),0,round(im.width*(i+1)/5),im.height))
        crop.save(folder/'lineup-crop-v1.webp',quality=92,method=6)
        readme=folder.parent/'README.md'
        if not readme.exists():
            readme.write_text(f'# {hero.title()} Jamesy — character group\n\n![Costume reference](references/lineup-crop-v1.webp)\n\nReference extract only. Not a registered sprite. See the art bible and progress ledger.\n')
    metadata={}
    for name in ['import-queue.json','character-batch-02.json']:
        path=ROOT/'art'/name
        if path.exists():
            metadata.update({e['path']:e for e in json.loads(path.read_text()).get('imports',[])})
    exports=[]
    for path in (ROOT/'art/01-characters').rglob('manifest.json'):
        data=json.loads(path.read_text())
        if data.get('schemaVersion')==1 and isinstance(data.get('frames'),list):
            exports.append((path.parent,data))
    records=[]
    for p in sorted((ROOT/'art').rglob('*')):
        if p.suffix.lower() not in {'.png','.jpg','.webp'}:continue
        rel=p.relative_to(ROOT).as_posix();entry=metadata.get(rel,{})
        status=entry.get('reviewStatus','reference' if 'reference' in p.parts else 'candidate_unreviewed')
        if '/references/' in rel or '/00-reference/' in rel:status='reference'
        notes=entry.get('notes','')
        for folder,manifest in exports:
            if p.is_relative_to(folder):
                status=manifest.get('status','candidate_unreviewed');notes=manifest.get('notes','')
                if p.name=='contact-review.jpg':status='review_contact_board'
        with Image.open(p) as img:
            alpha=img.getchannel('A').getextrema() if 'A' in img.getbands() else None
            records.append({'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'width':img.width,'height':img.height,'status':status,'hasAlphaChannel':alpha is not None,'hasTransparentPixels':alpha is not None and alpha[0]<255,'productionReady':False,'notes':notes})
    total=sum(r['bytes'] for r in records)
    inventory={'schemaVersion':1,'files':records,'totalBytes':total,'productionReadyCount':0,'note':'Real image-file counts include alternate resolutions, atlases and review boards. They are not unique animation-frame counts. No candidate is automatically approved.'}
    (ROOT/'art/inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
    cards=[]
    for r in records:
        rel=r['path'].removeprefix('art/')
        cards.append(f'<article><a href="{html.escape(rel)}"><img loading="lazy" src="{html.escape(rel)}" alt="{html.escape(rel)}"></a><h2>{html.escape(rel)}</h2><p>{r["width"]} × {r["height"]} · {html.escape(r["status"])}</p><p>{html.escape(r["notes"])}</p></article>')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Jamesy Art Library</title><style>body{background:#faf7f0;color:#153c35;font:16px system-ui;margin:0;padding:28px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}article{background:white;border:1px solid #d8dece;border-radius:14px;padding:16px;min-width:0}img{width:100%;max-height:440px;object-fit:contain}h2{font-size:15px;overflow-wrap:anywhere}p{line-height:1.5}a{color:#7542b4}</style><h1>Jamesy Art Library</h1><p>Character references and review candidates. Not finished production animations.</p><p><a href="01-characters/hulk/pose-reviews/v02-cutouts/review.html">Corrected poses viewer</a> · <a href="01-characters/hulk/run-reviews/v01/review-export/review.html">Rear run review</a></p>'''+f'<p>{len(records)} actual image files · {total/1048576:.2f} MiB · <a href="../production/art-bible-v1/Jamesy-Art-Bible-v1.2.pdf">Art bible PDF</a></p><main>'+''.join(cards)+'</main></html>'
    (ROOT/'art/gallery.html').write_text(page)
    print(f'Indexed {len(records)} actual image files; {total/1048576:.2f} MiB')
if __name__=='__main__':prepare()
