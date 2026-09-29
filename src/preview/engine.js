import * as T from 'three';
import {RaceEngine} from '../game/engine-core.js';
import {LEVELS,makeCourse,initialRun,courseX,courseY,slope} from '../game/logic.js';
const radius=9.2,roll=new T.Quaternion(),axis=new T.Vector3(0,0,1);
export function surfacePoint(s,theta=0,out=new T.Vector3()){
 const d=slope(s),h=radius*Math.sin(theta),n=Math.sqrt(1+d*d);
 return out.set(courseX(s)+h/n,courseY(s)+radius*(1-Math.cos(theta)),-s+h*d/n);
}
// Practice-only visual adapter. The existing collision, power and movement rules remain authoritative.
export class EmeraldPreview extends RaceEngine{
 constructor(canvas,settings,audio,events,art){
  super(canvas,settings,audio,events);this.art=art;this.spriteWorld=new T.Group();this.scene.add(this.spriteWorld);
  this.scene.remove(this.hero.root);this.heroVisual=art.mesh('rear_idle',true);const root=new T.Group();root.add(this.heroVisual);this.hero={root,tick:(t,r)=>this.animateHero(t,r)};this.scene.add(root);this.heroVisual.scale.setScalar(4.6);
  this.sky.visible=false;this.scene.background=art.assets.get('backdrop').texture;this.renderer.toneMappingExposure=1.04;this.scene.fog=new T.Fog(0xc6e6cf,75,225);this.rebuildSprites();
 }
 loadLevel(){
  super.loadLevel(0);this.level={...LEVELS[0],length:720};this.course=makeCourse(this.level);this.run=initialRun(this.level);this.finishRoot.visible=false;this.sky.visible=false;
  if(this.art)this.rebuildSprites();
 }
 makeScenery(){this.scenery=[];}
 makeItems(){super.makeItems();Object.values(this.itemMeshes).forEach(m=>m.visible=false);this.pickupGlows.visible=false;}
 makeTrack(){
  const positions=[],colors=[],indices=[],color=new T.Color(),cols=36,rows=Math.ceil((LEVELS[0].length+100)/4),palette=[0x54c94e,0xf4edce,0x9060d0];
  for(let j=0;j<rows;j++)for(let i=0;i<cols;i++){
   const s=j*4-32,a=-1.4+i*2.8/cols,b=a+2.8/cols,base=positions.length/3;
   for(const[distance,theta]of[[s,a],[s,b],[s+4,a],[s+4,b]]){const p=surfacePoint(distance,theta);positions.push(p.x,p.y,p.z);}
   const band=Math.floor(i/6),tile=Math.floor(j/3);color.setHex(palette[(band+tile)%3]);if(j%3===0)color.multiplyScalar(.92);
   for(let v=0;v<4;v++)colors.push(color.r,color.g,color.b);indices.push(base,base+2,base+1,base+1,base+2,base+3);
  }
  const geometry=new T.BufferGeometry();geometry.setAttribute('position',new T.Float32BufferAttribute(positions,3));geometry.setAttribute('color',new T.Float32BufferAttribute(colors,3));geometry.setIndex(indices);geometry.computeVertexNormals();
  const track=new T.Mesh(geometry,new T.MeshStandardMaterial({vertexColors:true,roughness:.3,metalness:.12,side:T.DoubleSide}));track.receiveShadow=true;this.world.add(track);
  for(const theta of[-1.4,1.4]){const points=[];for(let s=-32;s<LEVELS[0].length+80;s+=8)points.push(surfacePoint(s,theta));const edge=new T.Mesh(new T.TubeGeometry(new T.CatmullRomCurve3(points),300,.16,6,false),new T.MeshStandardMaterial({color:0xf8e5ae,roughness:.35}));this.world.add(edge);}
 }
 rebuildSprites(){
  this.spriteWorld.clear();this.props=[];this.itemSprites=[];this.lastHits=0;this.previousJump=0;this.heroClip='rear_idle';this.heroChanged=this.elapsed;
  for(const item of this.course){const id={special:'star',orb:'bumper'}[item.kind]||item.kind,m=this.art.mesh(id);this.spriteWorld.add(m);this.itemSprites.push({item,id,mesh:m,doneAt:null});}
  const prop=(id,s,side,size,phase=0)=>{const m=this.art.mesh(id);m.scale.setScalar(size);this.spriteWorld.add(m);this.props.push({id,s,side,size,mesh:m,phase});};
  for(let s=5;s<820;s+=26)for(const side of[-1,1]){prop('tree',s,side*(14+Math.sin(s*.4)*2),15+Math.sin(s)*1.5,s*.137);prop('shrub',s+10,side*11.2,5,s*.117);}
  for(let s=90;s<820;s+=110)prop('gateway',s,0,24);
  for(let s=40;s<820;s+=65)for(const side of[-1,1])prop('canopy',s,side*33,21,s*.1);
  this.sky.visible=false;this.floor.material.color.setHex(0x87ba63);this.floor.material.roughness=.85;
 }
 animateHero(time,r){
  let id='rear_idle',phase=time;
  if(r.hits>this.lastHits){this.hurtUntil=time+.45;this.lastHits=r.hits;}
  if(this.previousJump>0&&r.jumpTime===0)this.landUntil=time+.24;this.previousJump=r.jumpTime;
  if(r.moving)id=Math.abs(this.steer)>.1?(this.steer<0?'lean_left':'lean_right'):'run';
  if(r.jumpTime>0){id='jump';phase=(r.jumpTime/.95)*(this.art.hero.get(id).frames.length/this.art.hero.get(id).fps);}
  else if(time<this.landUntil)id='land';
  if(r.smashAnim>0){id='smash';phase=(1-r.smashAnim/.65)*(this.art.hero.get(id).frames.length/this.art.hero.get(id).fps);}
  if(r.clapAnim>0){id='thunderclap';phase=(1-r.clapAnim/.45)*(this.art.hero.get(id).frames.length/this.art.hero.get(id).fps);}
  if(time<this.hurtUntil&&r.smashAnim<=0&&r.clapAnim<=0)id='hurt';
  if(id!==this.heroClip){this.heroClip=id;this.heroChanged=time;}
  const c=this.art.hero.get(id)||this.art.hero.get('rear_idle');if(!c.loop&&!['jump','smash','thunderclap'].includes(id))phase=time-this.heroChanged;
  this.art.frame(this.heroVisual,c,phase);
 }
 drawWorld(dt){
  super.drawWorld(dt);if(!this.art)return;
  const D=this.run.distance;
  const background=this.scene.background,ratio=this.camera.aspect/(1672/941);background.repeat.set(Math.min(1,ratio),Math.min(1,1/ratio));background.offset.set((1-background.repeat.x)/2,(1-background.repeat.y)/2);
  if(this.state==='menu'){this.camera.fov=60;this.camera.position.set(courseX(-11.5),courseY(0)+7.1,11.5);this.camera.lookAt(courseX(18),courseY(18)+2,-18);this.camera.updateProjectionMatrix();}
  this.heroVisual.quaternion.copy(this.hero.root.quaternion).invert().multiply(this.camera.quaternion).multiply(roll.setFromAxisAngle(axis,-this.theta*.65));
  for(const p of this.props){const m=p.mesh;m.visible=p.s>D-25&&p.s<D+225;if(!m.visible)continue;m.position.set(courseX(p.s)+p.side,courseY(p.s)+(p.id==='gateway'?4.5:0),-p.s);m.quaternion.copy(this.camera.quaternion);if(p.id==='tree')this.art.frame(m,this.art.clips.get('tree'),this.settings.reduced?0:this.elapsed*.5+p.phase);else if(p.id==='shrub'&&!this.settings.reduced)m.quaternion.multiply(roll.setFromAxisAngle(axis,Math.sin(this.elapsed*.7+p.phase)*.012));}
  for(const p of this.itemSprites){
   const {item}=p;const mesh=p.mesh,clip=this.art.clips.get(p.id);if(item.done&&p.doneAt===null)p.doneAt=this.elapsed;
   const age=p.doneAt===null?0:this.elapsed-p.doneAt,breaking=item.done&&item.kind==='rock'&&age<1.05,popping=item.done&&['gem','special'].includes(item.kind)&&age<.16;
   mesh.visible=item.s>D-10&&item.s<D+165&&(!item.done||breaking||popping);if(!mesh.visible)continue;
   surfacePoint(item.s,item.theta,mesh.position);const pickup=item.kind==='gem'||item.kind==='special';mesh.position.y+=pickup?1.25+Math.sin(this.elapsed*2+item.id)*.12:item.kind==='orb'?1.4:.06;mesh.quaternion.copy(this.camera.quaternion);
   const size={gem:1.7,star:2,rock:3.05,bumper:2.6,goo:3.1}[p.id];mesh.scale.setScalar(size*(popping?1+age*2:1));
   this.art.frame(mesh,clip,breaking?Math.min(age,.79):item.kind==='rock'?0:this.settings.reduced?0:this.elapsed+item.id*.137);
  }
 }
}
