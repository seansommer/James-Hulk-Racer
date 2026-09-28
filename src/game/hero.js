import * as T from 'three';
import {mesh,ball,box,bake,material,labelTexture,glowTexture} from './assets.js';
/** Original articulated Jamesy model: swept red hair, eye mask, 4 shield and J belt. */
export function createHero(){
 const root=new T.Group(),body=new T.Group();root.add(body);
 const green=0x1dba77,purple=0x7950b6,skin=0xf4b68b,dark=0x214c49;
 const torso=new T.Group();
 ball(torso,dark,[0,2.12,0],[.67,.9,.39]);ball(torso,green,[0,2.18,.035],[.62,.85,.40]);
 ball(torso,green,[-.26,2.50,.28],[.34,.31,.18]);ball(torso,green,[.26,2.50,.28],[.34,.31,.18]);
 box(torso,purple,[-.49,2.08,.12],[.12,.75,.25],[0,0,-.15]);box(torso,purple,[.49,2.08,.12],[.12,.75,.25],[0,0,.15]);
 mesh(torso,new T.CylinderGeometry(.59,.55,.18,24),dark,[0,1.66,0],[1,1,.77]);
 ball(torso,green,[-.47,1.65,.36],[.2,.24,.13]);ball(torso,green,[.47,1.65,.36],[.2,.24,.13]);
 mesh(torso,new T.CylinderGeometry(.20,.20,.1,24),purple,[0,1.67,.43],[1,1,1],[Math.PI/2,0,0]);
 const shield=new T.Shape();shield.moveTo(0,-.45);shield.lineTo(-.40,.08);shield.lineTo(-.28,.4);shield.lineTo(.28,.4);shield.lineTo(.40,.08);shield.closePath();
 mesh(torso,new T.ExtrudeGeometry(shield,{depth:.07,bevelEnabled:true,bevelSize:.045,bevelThickness:.03,bevelSegments:2,steps:1}),dark,[0,2.48,.385]);
 mesh(torso,new T.ShapeGeometry(shield),purple,[0,2.48,.49],[.84,.85,1]);
 body.add(bake(torso));
 const number=mesh(body,new T.PlaneGeometry(.57,.59),new T.MeshBasicMaterial({map:labelTexture('4'),transparent:true,depthWrite:false}),[0,2.51,.499]);
 mesh(body,new T.PlaneGeometry(.24,.24),new T.MeshBasicMaterial({map:labelTexture('J'),transparent:true,depthWrite:false}),[0,1.68,.491]);
 const headPivot=new T.Group();headPivot.position.set(0,3.04,0);body.add(headPivot);
 const head=new T.Group();
 ball(head,skin,[0,.43,.03],[.72,.82,.65]);ball(head,skin,[-.71,.33,.015],[.16,.23,.15]);ball(head,skin,[.71,.33,.015],[.16,.23,.15]);
 ball(head,0xed9475,[-.75,.32,.12],[.07,.12,.025]);ball(head,0xed9475,[.75,.32,.12],[.07,.12,.025]);
 ball(head,0x14a65e,[-.30,.48,.565],[.37,.285,.12]);ball(head,0x14a65e,[.30,.48,.565],[.37,.285,.12]);
 ball(head,0x14a65e,[0,.47,.625],[.22,.14,.11]);
 for(const x of[-.29,.29]){ball(head,0xffffff,[x,.48,.676],[.224,.23,.059]);ball(head,0x3c86d1,[x,.48,.73],[.13,.155,.035]);ball(head,0x123348,[x,.48,.76],[.075,.105,.018]);ball(head,0xffffff,[x-.025,.532,.781],[.038,.04,.012]);}
 ball(head,0xf2a078,[0,.28,.668],[.14,.105,.14]);
 const smile=new T.CatmullRomCurve3([new T.Vector3(-.25,.075,.608),new T.Vector3(-.1,.018,.656),new T.Vector3(.12,.022,.651),new T.Vector3(.26,.087,.604)]);mesh(head,new T.TubeGeometry(smile,20,.022,6,false),0x9b5544);
 ball(head,0xbf501e,[0,.93,-.08],[.76,.51,.62]);
 for(let i=0;i<13;i++){
  const x=(i%5-2)*.26,z=-.44+Math.floor(i/5)*.31;const start=new T.Vector3(x,.99,z),end=new T.Vector3(x+.30,1.52+Math.sin(i*1.7)*.16,z-.16);
  const curve=new T.CatmullRomCurve3([start,new T.Vector3(x-.08,1.3,z+.10),new T.Vector3(x+.09,1.55,z+.02),end]);
  const geo=new T.TubeGeometry(curve,12,.20,8,false),p=geo.attributes.position;
  for(let a=0;a<=12;a++){const center=curve.getPointAt(a/12),f=Math.max(.035,1-Math.pow(a/12,2));for(let b=0;b<=8;b++){const idx=a*9+b;const v=new T.Vector3().fromBufferAttribute(p,idx).sub(center).multiplyScalar(f).add(center);p.setXYZ(idx,v.x,v.y,v.z);}}
  geo.computeVertexNormals();mesh(head,geo,[0xe87925,0xf39132,0xd45d1f][i%3]);
 }
 headPivot.add(bake(head));const arms=[],legs=[];
 for(const side of[-1,1]){
  const pivot=new T.Group();pivot.position.set(side*.66,2.65,0);body.add(pivot);arms.push(pivot);const a=new T.Group();ball(a,purple,[side*.08,0,.0],[.33,.22,.38]);ball(a,green,[side*.13,-.36,0],[.255,.44,.25]);mesh(a,new T.CylinderGeometry(.245,.255,.47,16),purple,[side*.20,-.77,.04]);ball(a,green,[side*.20,-1.08,.10],[.32,.32,.31]);for(let j=0;j<3;j++)ball(a,0x20b975,[side*.20+(j-1)*.135,-1.18,.29],[.081,.13,.09]);ball(a,0x149962,[side*.20-side*.26,-1.01,.16],[.12,.18,.15]);pivot.add(bake(a));
  const lPivot=new T.Group();lPivot.position.set(side*.28,1.50,0);body.add(lPivot);legs.push(lPivot);const l=new T.Group();ball(l,green,[0,-.32,0],[.27,.5,.29]);ball(l,dark,[0,-.67,.05],[.26,.20,.28]);ball(l,purple,[0,-.89,.02],[.27,.4,.31]);ball(l,purple,[0,-1.18,.17],[.30,.24,.47]);box(l,0x234e4c,[0,-1.37,.15],[.54,.10,.70]);ball(l,0xac7de4,[0,-.93,.29],[.16,.26,.055]);lPivot.add(bake(l));
 }
 const capeGeo=new T.PlaneGeometry(1.3,1.95,12,15);capeGeo.translate(0,-.97,0);const capeBase=capeGeo.attributes.position.array.slice();const cape=mesh(body,capeGeo,material(purple,{side:T.DoubleSide,roughness:.76}),[0,2.72,-.38]);cape.castShadow=true;
 const glow=new T.Sprite(new T.SpriteMaterial({map:glowTexture(),color:0x69ff9b,blending:T.AdditiveBlending,depthWrite:false,transparent:true,opacity:0}));glow.position.y=2.1;glow.scale.set(7,7,1);root.add(glow);
 const rim=mesh(root,new T.SphereGeometry(1,24,18),new T.ShaderMaterial({uniforms:{amount:{value:0}},vertexShader:'varying vec3 n; varying vec3 v; void main(){vec4 p=modelViewMatrix*vec4(position,1.); n=normalize(normalMatrix*normal); v=normalize(-p.xyz); gl_Position=projectionMatrix*p;}',fragmentShader:'uniform float amount; varying vec3 n; varying vec3 v; void main(){float rim=pow(1.-abs(dot(normalize(n),normalize(v))),3.);gl_FragColor=vec4(.3,1.,.5,rim*amount);}',transparent:true,blending:T.AdditiveBlending,depthWrite:false}),[0,2,0],[1.4,2.4,1.0]);
 return{root,body,headPivot,tick(t,run,settings={}){const moving=run?.moving??false,phase=t*(run?.burst?16:12),jump=run?.jump||0,smash=run?.smashAnim||0,clap=run?.clapAnim||0;body.position.y=moving?Math.abs(Math.sin(phase))*.08:Math.sin(t*2)*.045;body.rotation.x=moving?.09:0;headPivot.rotation.y=moving?Math.sin(t*1.6)*.05:Math.sin(t*.6)*.16;arms.forEach((a,i)=>{a.rotation.x=clap>0?-1.35:smash>0?-2.6:jump>0?-1.6:(moving?Math.sin(phase+i*Math.PI)*.70:-.12);a.rotation.z=clap>0?(i===0?-.65:.65):(i===0?.10:-.10);});legs.forEach((l,i)=>l.rotation.x=jump>0?(i===0?-.7:.5):(moving?Math.sin(phase+i*Math.PI+Math.PI)*.78:0));const p=capeGeo.attributes.position;for(let i=0;i<p.count;i++){const x=capeBase[i*3],y=capeBase[i*3+1],v=-y/1.95;p.setXYZ(i,x*(1+v*.28),y,-v*(moving?.8:.28)+Math.sin(t*7+v*5+x*2)*v*.15);}p.needsUpdate=true;capeGeo.computeVertexNormals();const a=(run?.power||0)/100;glow.material.opacity=settings.reduced?0:(run?.burst?.35:a*.15);rim.material.uniforms.amount.value=settings.reduced?0:(run?.burst?.65:a*.32);number.visible=true;}};
}
