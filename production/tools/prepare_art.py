"""Build reference extracts, a factual inventory and local gallery. No game integration."""
from pathlib import Path
from PIL import Image
import html, json, hashlib
ROOT=Path(__file__).resolve().parents[2]
HEROES=['hulk','spider','captain','iron','super']

def prepare():
    src=ROOT/'art/00-reference/lineup-j-v1.png'
    with Image.open(src) as original:
        im=original.convert('RGB')
    im.save(src.with_suffix('.webp'),quality=90,method=6)
    for i,hero in enumerate(HEROES):
        folder=ROOT/f'art/01-characters/{hero}/references';folder.mkdir(parents=True,exist_ok=True)
        crop=im.crop((round(im.width*i/5),0,round(im.width*(i+1)/5),im.height))
        crop.save(folder/'lineup-crop-v1.webp',quality=92,method=6)
        parent=folder.parent
        readme=parent/'README.md'
        if not readme.exists():
            readme.write_text(f'# {hero.title()} Jamesy — character group\n\n![Costume reference](references/lineup-crop-v1.webp)\n\nReference extract only. The ivory background is retained and a crop is not a registered sprite.\n\nPose reviews, individual frame sources and accepted exports belong here as they are completed. No finished animation is claimed by the reference image. See the main art bible and progress ledger.\n')
    queue=ROOT/'art/import-queue.json'
    metadata={e['path']:e for e in json.loads(queue.read_text()).get('imports',[])} if queue.exists() else {}
    records=[]
    for p in sorted((ROOT/'art').rglob('*')):
        if p.suffix.lower() not in {'.png','.jpg','.webp'}:continue
        rel=p.relative_to(ROOT).as_posix()
        with Image.open(p) as img:
            alpha=img.getchannel('A').getextrema() if 'A' in img.getbands() else None
            records.append({'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'width':img.width,'height':img.height,'status':'reference' if 'reference' in p.as_posix() else 'candidate_unreviewed','hasAlphaChannel':alpha is not None,'hasTransparentPixels':alpha is not None and alpha[0]<255,'productionReady':False,'notes':metadata.get(rel,{}).get('notes','')})
    total=sum(r['bytes'] for r in records)
    inventory={'schemaVersion':1,'files':records,'totalBytes':total,'productionReadyCount':0,'note':'Counts describe real files; no candidate is automatically approved.'}
    (ROOT/'art/inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
    cards=[]
    for r in records:
        rel=r['path'].removeprefix('art/')
        cards.append(f'<article><a href="{html.escape(rel)}"><img loading="lazy" src="{html.escape(rel)}" alt="{html.escape(rel)}"></a><h2>{html.escape(rel)}</h2><p>{r["width"]} × {r["height"]} · {r["status"]}</p><p>{html.escape(r["notes"])}</p></article>')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Jamesy Art Library</title><style>body{background:#faf7f0;color:#153c35;font:16px system-ui;margin:0;padding:28px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}article{background:white;border:1px solid #d8dece;border-radius:14px;padding:16px;min-width:0}img{width:100%;max-height:440px;object-fit:contain}h2{font-size:15px;overflow-wrap:anywhere}p{line-height:1.5}a{color:#7542b4}</style><h1>Jamesy Art Library</h1><p>Reference and candidate artwork. These are not finished production animations.</p>'''+f'<p>{len(records)} actual image files · {total/1048576:.2f} MiB · <a href="../production/art-bible-v1/Jamesy-Art-Bible-v1.2.pdf">Art bible PDF</a></p><main>'+''.join(cards)+'</main></html>'
    (ROOT/'art/gallery.html').write_text(page)
    print(f'Indexed {len(records)} actual image files; {total/1048576:.2f} MiB')
if __name__=='__main__':prepare()
