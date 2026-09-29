import * as T from 'three';
// Public preview files are siblings of this entry. The portable build supplies data URLs.
export const assetURL=file=>window.JAMESY_FILES?.[file]||new URL(`./${file}`,location.href).href;
export async function loadArt(){
 const response=await fetch(assetURL('manifest.json'));if(!response.ok)throw new Error('The Emerald art library could not load.');
 const data=await response.json(),loader=new T.TextureLoader(),cache=new Map();
 await Promise.all([...data.assets,...data.clips,...data.hero].map(async a=>{if(cache.has(a.file))return;const texture=await loader.loadAsync(assetURL(a.file));texture.colorSpace=T.SRGBColorSpace;texture.generateMipmaps=false;texture.minFilter=T.LinearFilter;texture.magFilter=T.LinearFilter;cache.set(a.file,texture);}));
 const assets=new Map(data.assets.map(a=>[a.id,{...a,texture:cache.get(a.file)}]));
 function clip(c){const texture=cache.get(c.file),material=new T.MeshBasicMaterial({map:texture,transparent:true,alphaTest:.06,depthWrite:false,side:T.DoubleSide,toneMapped:false});const geometries=c.frames.map(f=>{
  const g=new T.PlaneGeometry(c.canvas[0]/c.canvas[1],1);g.translate((.5-c.pivot[0])*c.canvas[0]/c.canvas[1],c.pivot[1]-.5,0);const[x,y,w,h]=f.rect,[aw,ah]=c.atlasSize;g.setAttribute('uv',new T.Float32BufferAttribute([x/aw,1-y/ah,(x+w)/aw,1-y/ah,x/aw,1-(y+h)/ah,(x+w)/aw,1-(y+h)/ah],2));return g;
 });return{...c,material,geometries};}
 const clips=new Map(data.clips.map(c=>[c.asset,clip(c)])),hero=new Map(data.hero.map(c=>[c.id,clip(c)]));
 function mesh(id,isHero=false){const c=(isHero?hero:clips).get(id);if(c){const m=new T.Mesh(c.geometries[0],c.material);m.userData.clip=c;return m;}const a=assets.get(id),g=new T.PlaneGeometry(a.sourceSize[0]/a.sourceSize[1],1);g.translate((.5-a.pivot[0])*a.sourceSize[0]/a.sourceSize[1],a.pivot[1]-.5,0);return new T.Mesh(g,new T.MeshBasicMaterial({map:a.texture,transparent:true,alphaTest:.05,depthWrite:false,side:T.DoubleSide,toneMapped:false}));}
 function frame(m,c,time){const index=c.loop?Math.floor(time*c.fps)%c.sequence.length:Math.min(c.sequence.length-1,Math.floor(time*c.fps));m.geometry=c.geometries[c.sequence[Math.max(0,index)]];m.material=c.material;}
 return{data,assets,clips,hero,mesh,frame};
}
