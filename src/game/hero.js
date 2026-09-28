import * as T from 'three';
import {createHero as createArticulatedHero} from './hero-core.js';
import {ball,bake} from './assets.js';

/** Silhouette and cloth details over the shared articulated Jamesy rig. */
export function createHero(){
 const hero=createArticulatedHero(),hair=new T.Group();
 // Full rear hair volume makes the same character recognizable from the race camera.
 ball(hair,0xd96721,[0,.56,-.27],[.715,.72,.47]);
 ball(hair,0xe67b26,[0,1.12,-.12],[.74,.42,.55]);
 const sweep=ball(hair,0xf09131,[-.03,1.16,.18],[.72,.35,.37]);sweep.rotation.z=-.27;
 for(let i=0;i<7;i++){const a=-1.15+i*.38;const lock=ball(hair,i%2?0xeb832a:0xd96b20,[Math.sin(a)*.58,.67+Math.cos(a)*.11,-.54],[.19,.40,.17]);lock.rotation.z=-.25+Math.sin(a)*.24;}
 hero.headPivot.add(bake(hair));
 const cape=hero.body.children.find(o=>o.isMesh&&o.geometry?.type==='PlaneGeometry'&&o.material?.isMeshStandardMaterial);
 const tick=hero.tick.bind(hero);
 hero.tick=(time,run,settings)=>{
  tick(time,run,settings);
  if(!cape)return;
  const p=cape.geometry.attributes.position;
  for(let i=0;i<p.count;i++){const y=p.getY(i),v=Math.max(0,Math.min(1,-y/1.95)),x=p.getX(i),u=x/(.65*(1+v*.28));p.setXYZ(i,x*(1+v*.12),y+.10*Math.pow(v,5)*(1-Math.cos(u*Math.PI*3)),p.getZ(i)-v*v*.27+Math.sin(time*6+u*4)*v*.045);}
  p.needsUpdate=true;cape.geometry.computeVertexNormals();
 };
 return hero;
}
