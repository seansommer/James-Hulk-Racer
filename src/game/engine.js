import * as T from 'three';
import {RaceEngine as CoreEngine} from './engine-core.js';
import {courseX,courseY,slope,rng} from './logic.js';
import {mesh,material,ball,bake} from './assets.js';

// World art is layered on top of the independently tested race simulation.
const RADIUS=9.2,EDGE=1.36;
function surface(s,a,lift=0){const d=slope(s),h=RADIUS*Math.sin(a),n=Math.sqrt(1+d*d);return new T.Vector3(courseX(s)+h/n,courseY(s)+RADIUS*(1-Math.cos(a))+lift,-s+h*d/n);}
function geometry(positions,indices,colors){const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(positions,3));g.setIndex(indices);if(colors)g.setAttribute('color',new T.Float32BufferAttribute(colors,3));g.computeVertexNormals();return g;}

export class RaceEngine extends CoreEngine{
 loadLevel(index){
  super.loadLevel(index);
  // Custom sky shaders need the same linear-to-display conversion as PBR meshes.
  const sky=this.sky.material;
  if(!sky.userData.outputReady){const text=sky.fragmentShader;sky.fragmentShader=text.slice(0,text.lastIndexOf('}'))+'\n#include <colorspace_fragment>\n}';sky.userData.outputReady=true;sky.toneMapped=false;sky.needsUpdate=true;}
 }
 makeScenery(){
  super.makeScenery();
  // The course is sunk into its landscape: tree roots belong on the raised banks,
  // not at the bottom of the half-pipe where the walls would conceal the trees.
  this.scenery.forEach((batch,index)=>{if(index!==1)batch.mesh.position.y=7.55;});
  this.makeBanks();this.makeWayfinding();
  if(this.levelIndex===1)this.makeCave();else this.makeClouds();
  if(this.levelIndex===2)this.makeLavaStreams();
 }
 makeBanks(){
  const random=rng(this.level.seed+900),color=new T.Color(),base=[0x6aaf76,0x294b68,0x53845f][this.levelIndex];
  for(const side of[-1,1]){const positions=[],indices=[],colors=[];let row=0;
   for(let s=-40;s<=this.level.length+100;s+=12,row++){
    const inner=surface(s,side*EDGE,.035),d=slope(s),n=Math.sqrt(1+d*d),outer=inner.clone().add(new T.Vector3(side*140/n,1.2,side*140*d/n));positions.push(...inner.toArray(),...outer.toArray());color.setHex(base).multiplyScalar(.90+random()*.16);for(let k=0;k<2;k++)colors.push(color.r,color.g,color.b);if(row){const b=row*2;indices.push(b-2,b,b-1,b-1,b,b+1);}
   }
   const bank=mesh(this.world,geometry(positions,indices,colors),material(0xffffff,{vertexColors:true,roughness:.94,side:T.DoubleSide}));bank.receiveShadow=true;
  }
 }
 makeWayfinding(){
  const positions=[],indices=[];
  for(let s=12;s<this.level.length;s+=32)for(const side of[-1,1])for(const shift of[0,5]){
   const a=side*1.08,b=positions.length/3;
   for(const[da,ds]of[[-.11,0],[0,2],[.11,0],[.11,-1.6],[0,.4],[-.11,-1.6]])positions.push(...surface(s+shift+ds,a+da,.035).toArray());
   for(const i of[0,1,5,1,4,5,1,2,3,1,3,4])indices.push(b+i);
  }
  mesh(this.world,geometry(positions,indices),new T.MeshBasicMaterial({color:0xf2ffde,transparent:true,opacity:.56,side:T.DoubleSide,depthWrite:false}));
 }
 makeClouds(){
  const group=new T.Group();ball(group,0xfffcf1,[0,0,0],[4,1.2,2]);ball(group,0xffffff,[-1.7,.55,0],[1.9,1.55,1.7]);ball(group,0xffffff,[.9,1.0,-.3],[2.1,1.8,1.8]);ball(group,0xf6f7f2,[3,0,.2],[1.8,.9,1.5]);const template=bake(group,{roughness:1});
  const random=rng(this.level.seed+300),data=[];
  for(let s=5;s<this.level.length+200;s+=80)for(const side of[-1,1])data.push({s,side:side*(27+random()*40),scale:1.25+random(),rot:random()*2});
  const clouds=new T.InstancedMesh(template.geometry,template.material,data.length);clouds.instanceMatrix.setUsage(T.DynamicDrawUsage);clouds.frustumCulled=false;clouds.position.y=24;clouds.count=0;this.world.add(clouds);this.scenery.push({mesh:clouds,data});
 }
 makeCave(){
  const positions=[],indices=[],colors=[],random=rng(555),color=new T.Color(),columns=14;let row=0;
  for(let s=-45;s<=this.level.length+100;s+=14,row++)for(let j=0;j<=columns;j++){
   const a=-Math.PI/2+j*Math.PI/columns,x=Math.sin(a)*23,y=12+Math.cos(a)*(14+random()*2);positions.push(courseX(s)+x,courseY(s)+y,-s);color.setHex([0x283b59,0x344660,0x3c4266][j%3]).multiplyScalar(.75+random()*.45);colors.push(color.r,color.g,color.b);if(row&&j<columns){const b=row*(columns+1)+j;indices.push(b-columns-1,b,b+1,b-columns-1,b+1,b-columns);}
  }
  mesh(this.world,geometry(positions,indices,colors),material(0xffffff,{vertexColors:true,roughness:.95,flatShading:true,side:T.DoubleSide}));
 }
 makeLavaStreams(){
  for(const side of[-1,1]){const positions=[],indices=[];let row=0;
   for(let s=-40;s<=this.level.length+100;s+=12,row++)for(const offset of[-1.8,1.8]){const x=side*(28+Math.sin(s/40)*3)+offset;positions.push(courseX(s)+x,courseY(s)+7.7,-s);if(row&&offset===1.8){const b=row*2;indices.push(b-2,b,b-1,b-1,b,b+1);}}
   mesh(this.world,geometry(positions,indices),material(0xf9914b,{emissive:0xff5b22,emissiveIntensity:.75,roughness:.38,side:T.DoubleSide}));
  }
 }
}
