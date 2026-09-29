import sharp from 'sharp';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import path from 'node:path';

// Deterministic export only. Original AI artwork is never overwritten or repainted.
const root=process.cwd(), items='art/02-items/park/v02', env='art/03-environments/park/v01';
const sha=b=>createHash('sha256').update(b).digest('hex');
async function json(file,data){await mkdir(path.dirname(file),{recursive:true});await writeFile(file,JSON.stringify(data,null,2)+'\n');}
async function bounds(buffer,threshold=32){
 const {data,info}=await sharp(buffer).ensureAlpha().raw().toBuffer({resolveWithObject:true});
 let x0=info.width,y0=info.height,x1=-1,y1=-1,clear=0;
 for(let y=0;y<info.height;y++)for(let x=0;x<info.width;x++){const a=data[(y*info.width+x)*4+3];if(!a)clear++;if(a>=threshold){x0=Math.min(x0,x);y0=Math.min(y0,y);x1=Math.max(x1,x);y1=Math.max(y1,y);}}
 return {rect:[x0,y0,x1+1,y1+1],transparentFraction:clear/(info.width*info.height),width:info.width,height:info.height};
}
const specs=[
 ['gem','Power gem','gem','center',items],['star','Golden star','special','center',items],['rock','Moss rock','rock','ground',items],['bumper','Violet bumper','orb','center',items],['goo','Purple goo','goo','ground',items],
 ['tree','Park tree','tree','ground',env],['shrub','Leafy shrub','shrub','ground',env],['gateway','Park gateway','gateway','ground',env],['canopy','Canopy layer','canopy','ground',env],['backdrop','Park valley','backdrop','center',env]
];
const library={schemaVersion:1,title:'Emerald Park · Art and Motion Library',productionReady:false,approval:'Candidate — owner review pending',generator:'OpenAI native image generation',track:'Real curved 3D half-pipe; illustrated sprites placed in the world',assets:[],clips:[]};
for(const[id,label,kind,anchor,dir]of specs){
 const file=`${dir}/sources/${id}.png`,buffer=await readFile(file),b=await bounds(buffer),[x0,y0,x1,y1]=b.rect;
 const out={id,label,kind,source:file,sourceSha256:sha(buffer),sourceSize:[b.width,b.height],visibleBounds:b.rect,transparentFraction:b.transparentFraction,pivot:[(x0+x1)/2/b.width,(anchor==='ground'?y1:(y0+y1)/2)/b.height],anchor,exports:{},productionReady:false};
 for(const size of[512,1024]){const dest=`${dir}/textures-${size}/${id}.png`;await mkdir(path.dirname(dest),{recursive:true});await sharp(buffer).resize({width:size,height:size,fit:'inside',withoutEnlargement:true}).png().toFile(dest);out.exports[size]=dest;}
 library.assets.push(out);
}
const motion=`${items}/motion`;
const clipSpecs=[
 {id:'gem-turn',asset:'gem',grid:[4,3],count:12,fps:12,loop:true,anchor:'center',note:'AI facet-turn study. Check constant angular speed and final-to-first seam.'},
 {id:'star-turn',asset:'star',grid:[3,2],count:6,fps:6,loop:true,anchor:'center',note:'Six authored viewing angles; add in-betweens for a smoother close-up turn.'},
 {id:'rock-crumble',asset:'rock',grid:[4,2],count:8,fps:10,loop:false,anchor:'ground',note:'One-shot smash reaction; final rubble may fade in runtime. Physics clears at the smash event.'},
 {id:'bumper-pulse',asset:'bumper',grid:[3,2],count:6,fps:5,loop:true,anchor:'center',note:'Lens pulse. Inspect shell stability before final approval.'},
 {id:'goo-wobble',asset:'goo',grid:[3,2],count:6,fps:6,loop:true,anchor:'ground',note:'Jelly wobble; collision footprint remains fixed.'},
 {id:'tree-sway',sourceId:'tree-sway-v02',asset:'tree',grid:[3,2],count:3,fps:2,loop:true,anchor:'ground',sequence:[0,1,2,1],note:'Top-row poses only, ping-pong. Bottom row rejected for branch identity drift; first sheet rejected for clipping. More in-betweens and a steadier trunk remain polish tasks.'}
];
for(const spec of clipSpecs){
 const source=`${motion}/sources/${spec.sourceId||spec.id}.png`,buffer=await readFile(source),meta=await sharp(buffer).metadata(),cells=[];
 for(let i=0;i<spec.count;i++){
  const col=i%spec.grid[0],row=Math.floor(i/spec.grid[0]);const x=Math.round(col*meta.width/spec.grid[0]),y=Math.round(row*meta.height/spec.grid[1]),w=Math.round((col+1)*meta.width/spec.grid[0])-x,h=Math.round((row+1)*meta.height/spec.grid[1])-y;
  const cell=await sharp(buffer).extract({left:x,top:y,width:w,height:h}).png().toBuffer(),b=await bounds(cell),r=b.rect;
  let ax=(r[0]+r[2])/2,ay=spec.anchor==='ground'?r[3]:(r[1]+r[3])/2;
  if(spec.asset==='rock'){ax=w/2;ay=h*.96;} // Debris keeps the original ground registration.
  if(spec.asset==='tree'){ax=[302,300,285][i];ay=507;}
  cells.push({buffer:cell,sourceRect:[x,y,w,h],bounds:r,w,h,ax,ay});
 }
 // One common scale per clip, never stretch frames independently to fit.
 const extentX=Math.max(...cells.map(c=>Math.max(c.ax-c.bounds[0],c.bounds[2]-c.ax))),extentUp=Math.max(...cells.map(c=>c.ay-c.bounds[1])),extentDown=Math.max(...cells.map(c=>c.bounds[3]-c.ay));
 const targetY=spec.anchor==='ground'?464:256,scale=Math.min(220/extentX,(targetY-30)/extentUp,(500-targetY)/Math.max(1,extentDown));
 const frames=[],frameBuffers=[];
 for(let i=0;i<cells.length;i++){
  const c=cells[i],r=c.bounds,x=Math.max(0,r[0]-4),y=Math.max(0,r[1]-4),w=Math.min(c.w,r[2]+4)-x,h=Math.min(c.h,r[3]+4)-y;
  const piece=await sharp(c.buffer).extract({left:x,top:y,width:w,height:h}).resize(Math.max(1,Math.round(w*scale)),Math.max(1,Math.round(h*scale))).png().toBuffer();
  const left=Math.round(256-(c.ax-x)*scale),top=Math.round(targetY-(c.ay-y)*scale);
  const normalized=await sharp({create:{width:512,height:512,channels:4,background:{r:0,g:0,b:0,alpha:0}}}).composite([{input:piece,left,top}]).png().toBuffer();
  const file=`${motion}/frames-512/${spec.id}/${String(i).padStart(2,'0')}.png`;await mkdir(path.dirname(file),{recursive:true});await writeFile(file,normalized);frameBuffers.push(normalized);
  frames.push({file,sha256:sha(normalized),sourceRect:c.sourceRect,sourceAnchor:[c.ax,c.ay],crop:[x,y,w,h],commonScale:scale});
 }
 const size=spec.asset==='tree'?512:256,pad=4,cols=Math.min(4,spec.count),rows=Math.ceil(spec.count/cols),stride=size+pad*2,width=cols*stride,height=rows*stride;
 const composites=[];for(let i=0;i<frameBuffers.length;i++){const x=i%cols*stride+pad,y=Math.floor(i/cols)*stride+pad;composites.push({input:await sharp(frameBuffers[i]).resize(size,size).png().toBuffer(),left:x,top:y});frames[i].rect=[x,y,size,size];}
 const atlas=`${motion}/atlases/${spec.id}.png`;await mkdir(path.dirname(atlas),{recursive:true});const atlasBuffer=await sharp({create:{width,height,channels:4,background:{r:0,g:0,b:0,alpha:0}}}).composite(composites).png().toBuffer();await writeFile(atlas,atlasBuffer);
 library.clips.push({...spec,source,sourceSha256:sha(buffer),sourceSize:[meta.width,meta.height],atlas,atlasSha256:sha(atlasBuffer),atlasSize:[width,height],canvas:[512,512],pivot:[.5,targetY/512],frames,sequence:spec.sequence||frames.map((_,i)=>i),registration:'Translation with one shared clip scale; original source sheet preserved',productionReady:false});
}
await json(`${items}/library.json`,library);
console.log(`Exported ${library.assets.length} detailed assets and ${library.clips.reduce((n,c)=>n+c.frames.length,0)} selected animation drawings across ${library.clips.length} clips.`);
