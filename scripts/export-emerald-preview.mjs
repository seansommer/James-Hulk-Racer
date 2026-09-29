import {readFile,writeFile,mkdir,copyFile,access} from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';
import {createHash} from 'node:crypto';
const artRoot=process.argv[2];if(!artRoot)throw new Error('Pass a checkout of the Jamesy art branch.');
const out='preview-public/preview';await mkdir(`${out}/media`,{recursive:true});
const library=JSON.parse(await readFile(path.join(artRoot,'art/02-items/park/v02/library.json'),'utf8'));
const result={schemaVersion:1,productionReady:false,practiceOnly:true,assets:[],clips:[],hero:[]};
for(const a of library.assets){const size=['tree','gateway','backdrop','canopy'].includes(a.id)?1024:512;const file=`media/${a.id}.png`;await copyFile(path.join(artRoot,a.exports[size]),`${out}/${file}`);result.assets.push({...a,file});}
for(const c of library.clips){const file=`media/${c.id}.png`;await copyFile(path.join(artRoot,c.atlas),`${out}/${file}`);result.clips.push({...c,file});}
const hero=JSON.parse(await readFile(path.join(artRoot,'art/01-characters/hulk/unified-review/v01/manifest.json'),'utf8'));
for(const c of hero.clips){
 if(c.id==='victory')continue;const size=[384,480],pad=4,cols=Math.min(4,c.frames.length),rows=Math.ceil(c.frames.length/cols),width=cols*(size[0]+pad*2),height=rows*(size[1]+pad*2),layers=[],frames=[];
 for(let i=0;i<c.frames.length;i++){
  const f=c.frames[i];if(!f.sourcePath)throw new Error(`Missing archived source for ${c.id}`);const source=f.sourcePath.replace('frames-256','frames-512');await access(path.join(artRoot,source));const b=await readFile(path.join(artRoot,source));const x=i%cols*(size[0]+pad*2)+pad,y=Math.floor(i/cols)*(size[1]+pad*2)+pad;
  const resized=await sharp(b).resize(...size).png().toBuffer();layers.push({input:resized,left:x,top:y});if(c.id==='menu_idle'&&i===0)await writeFile(`${out}/media/portrait.png`,resized);frames.push({rect:[x,y,...size],source,sourceSha256:createHash('sha256').update(b).digest('hex')});
 }
 const file=`media/hero-${c.id}.png`;await sharp({create:{width,height,channels:4,background:{r:0,g:0,b:0,alpha:0}}}).composite(layers).png().toFile(`${out}/${file}`);
 result.hero.push({id:c.id,label:c.label,fps:c.fps,loop:c.loop,canvas:size,pivot:hero.pivot,atlasSize:[width,height],file,frames,sequence:frames.map((_,i)=>i),productionReady:false,note:c.note});
}
await writeFile(`${out}/manifest.json`,JSON.stringify(result));
console.log(`Copied ${result.assets.length} assets, ${result.clips.length} object/environment clips and ${result.hero.reduce((n,c)=>n+c.frames.length,0)} hero drawings.`);
