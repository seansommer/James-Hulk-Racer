import * as T from 'three';
import {mergeGeometries} from 'three/addons/utils/BufferGeometryUtils.js';
export const material=(color,options={})=>new T.MeshStandardMaterial({color,roughness:.48,metalness:.06,...options});
export function mesh(parent,geometry,color,pos=[0,0,0],scale=[1,1,1],rotation=[0,0,0]){
 const m=new T.Mesh(geometry,typeof color==='number'?material(color):color);m.position.set(...pos);m.scale.set(...scale);m.rotation.set(...rotation);parent.add(m);return m;
}
export const ball=(p,c,pos,scale)=>mesh(p,new T.SphereGeometry(1,20,14),c,pos,scale);
export const box=(p,c,pos,scale,rot)=>mesh(p,new T.BoxGeometry(1,1,1),c,pos,scale,rot);
/** Bake sculpted parts into one vertex-colored draw call, preserving real 3D normals. */
export function bake(group,options={}){
 group.updateMatrixWorld(true);const geos=[];group.traverse(m=>{if(!m.isMesh)return;const g=(m.geometry.index?m.geometry.toNonIndexed():m.geometry.clone());g.applyMatrix4(m.matrixWorld);for(const key of Object.keys(g.attributes))if(!['position','normal'].includes(key))g.deleteAttribute(key);const c=m.material.color,colors=new Float32Array(g.attributes.position.count*3);for(let i=0;i<colors.length;i+=3){colors[i]=c.r;colors[i+1]=c.g;colors[i+2]=c.b;}g.setAttribute('color',new T.BufferAttribute(colors,3));geos.push(g);});
 const geometry=mergeGeometries(geos);geos.forEach(g=>g.dispose());const out=new T.Mesh(geometry,material(0xffffff,{vertexColors:true,...options}));out.castShadow=true;out.receiveShadow=true;return out;
}
export function starGeometry(radius=.62,inner=.30){
 const shape=new T.Shape();for(let i=0;i<10;i++){const a=Math.PI/2+i*Math.PI/5,r=i%2?inner:radius;const x=Math.cos(a)*r,y=Math.sin(a)*r;i?shape.lineTo(x,y):shape.moveTo(x,y);}shape.closePath();const g=new T.ExtrudeGeometry(shape,{depth:.17,bevelEnabled:true,bevelSegments:2,steps:1,bevelSize:.075,bevelThickness:.065});g.translate(0,0,-.085);return g;
}
export function glowTexture(){const c=document.createElement('canvas');c.width=c.height=128;const x=c.getContext('2d'),g=x.createRadialGradient(64,64,0,64,64,64);g.addColorStop(0,'rgba(255,255,255,.95)');g.addColorStop(.15,'rgba(255,255,255,.55)');g.addColorStop(.45,'rgba(255,255,255,.16)');g.addColorStop(1,'rgba(255,255,255,0)');x.fillStyle=g;x.fillRect(0,0,128,128);return new T.CanvasTexture(c);}
export function labelTexture(text,bg,fg='#ffffff',size=128){const c=document.createElement('canvas');c.width=c.height=size;const x=c.getContext('2d');x.clearRect(0,0,size,size);if(bg){x.fillStyle=bg;x.fillRect(0,0,size,size);}x.fillStyle=fg;x.font=`900 ${size*.82}px system-ui`;x.textAlign='center';x.textBaseline='middle';x.fillText(text,size/2,size*.54);const t=new T.CanvasTexture(c);t.colorSpace=T.SRGBColorSpace;return t;}
export function createProp(type,theme){
 const g=new T.Group();
 if(type==='tree'){
  mesh(g,new T.CylinderGeometry(.25,.40,3.7,7),0x805837,[0,1.65,0]);
  if(theme===2){for(let i=0;i<7;i++){const a=i*Math.PI/3.5;const leaf=ball(g,0x42a75c,[Math.cos(a)*1.3,3.9,Math.sin(a)*1.3],[2.25,.20,.65]);leaf.rotation.set(0,-a,.15*Math.sin(a));}ball(g,0x56b873,[0,4.0,0],[.8,.6,.8]);}
  else{ball(g,0x469b57,[0,3.6,0],[1.65,1.9,1.65]);ball(g,0x79bf68,[-.9,3.0,.2],[1.2,1.35,1.2]);ball(g,0x6caf60,[1,3.4,.3],[1.2,1.45,1.2]);}
 }else if(type==='crystal'){
  for(let i=0;i<5;i++){const h=1.9+(i%3)*1.3;mesh(g,new T.ConeGeometry(.7,h,5),[0x66e8d7,0x7a6deb,0x3791c5][i%3],[(i-2)*.5,h*.42,Math.sin(i)*.45],[1,1,1],[0,i,.13*(i-2)]);}
 }else if(type==='building'){
  box(g,0xaaa7c7,[0,5.5,0],[3.7,11,3.7]);box(g,0xc4bfcb,[0,11.2,0],[2.9,.5,2.9]);box(g,0x8c8aaa,[0,12,0],[1.9,1.5,1.9]);
  for(let x=-1;x<=1;x++)for(let y=2;y<11;y+=1.6)box(g,0x799fab,[x,y,1.87],[.45,.75,.035]);
 }else if(type==='arch'){
  mesh(g,new T.TorusGeometry(10.7,.33,7,48,Math.PI),theme===1?0x5de6df:theme===2?0xd79971:0xf0e7c7,[0,8,0]);
  mesh(g,new T.TorusGeometry(10.7,.10,6,48,Math.PI),theme===1?0xb2fff7:0x9dcf9e,[0,8,.32]);
 }else if(type==='mountain'){
  mesh(g,new T.ConeGeometry(15,24,11),0x684f72,[0,9,0]);mesh(g,new T.ConeGeometry(4.4,6.2,11,1,true),0xff9973,[0,19,0]);
 }else if(type==='lamp'){
  mesh(g,new T.CylinderGeometry(.10,.17,6.5,7),0x375b60,[0,3,0]);ball(g,0xfff4c5,[0,6.3,0],[.38,.5,.38]);box(g,0x735ab4,[.7,4.7,0],[1.2,1.7,.10]);
 }else if(type==='rock'){
  const geo=new T.IcosahedronGeometry(1,1);mesh(g,geo,theme===2?0x695063:theme===1?0x485877:0x7c897c,[0,.70,0],[1.04,.83,.93],[.3,.5,.2]);
  if(theme===1){for(let i=0;i<3;i++)mesh(g,new T.ConeGeometry(.3,1.25,5),0xa39eea,[(i-1)*.42,1.3,.1],[1,1,1],[0,0,(i-1)*.25]);}
  if(theme===2){for(let i=0;i<4;i++)box(g,0xff9957,[Math.sin(i*2)*.8,.85+Math.cos(i)*.24,Math.cos(i*2)*.70],[.15,.58,.15],[0,0,i]);}
  if(theme===0){ball(g,0x78a363,[-.40,1.17,.15],[.48,.16,.47]);ball(g,0x8bb373,[.2,1.18,-.15],[.45,.1,.4]);}
 }else if(type==='orb'){
  ball(g,0x323348,[0,1.2,0],[.65,.65,.65]);
  for(let i=0;i<4;i++){const a=i*Math.PI/2;ball(g,theme===2?0xffa366:0xdd90ec,[Math.cos(a)*.59,1.2,Math.sin(a)*.59],[.24,.24,.24]);}
  mesh(g,new T.TorusGeometry(.72,.07,6,18),0x73638d,[0,1.2,0],[1,1,1],[Math.PI/2,0,0]);
 }else if(type==='goo'){
  ball(g,theme===1?0x9671ce:0x8a46b0,[0,.14,0],[1.15,.19,.9]);ball(g,0xa565d1,[-.3,.28,.13],[.44,.39,.4]);ball(g,0x985ccb,[.55,.16,-.2],[.32,.20,.34]);
 }
 return bake(g,type==='crystal'?{emissive:0x164e67,emissiveIntensity:.35}:{});
}
