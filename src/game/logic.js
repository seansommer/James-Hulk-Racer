/** Pure game rules. A deterministic course always leaves at least two safe lanes. */
export const LEVELS = [
 {id:'park',name:'Emerald Park',tag:'A big-city adventure',collectible:'Power gems',special:'Golden stars',hazard:'Mossy boulders',length:1420,speed:21,seed:41,sky:0x8ed7f4,fog:0xb3dfd9,track:[0x53b892,0xede9d4,0x7967b0],accent:0x91ffab},
 {id:'cavern',name:'Crystal Caverns',tag:'Find your inner glow',collectible:'Crystal shards',special:'Moon crystals',hazard:'Crystal clusters',length:1620,speed:23,seed:73,sky:0x101d3f,fog:0x1b3862,track:[0x277b99,0x41789d,0x7560ac],accent:0x7ff8ff},
 {id:'volcano',name:'Volcano Jungle',tag:'An epic island finale',collectible:'Sunstones',special:'Golden suns',hazard:'Lava boulders',length:1820,speed:25,seed:103,sky:0x85567f,fog:0xbb827e,track:[0xb2686b,0xe3a068,0x705080],accent:0xffd388}
];
export const LANES=[-.88,-.44,0,.44,.88];
export const clamp=(x,a,b)=>Math.min(b,Math.max(a,x));
export function rng(seed){return()=>{seed|=0;seed=seed+0x6D2B79F5|0;let t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
export function makeCourse(level){
 const random=rng(level.seed),items=[];let lane=2;
 for(let s=30,wave=0;s<level.length-36;s+=26,wave++){
  lane=clamp(lane+(random()<.48?-1:1),0,4);
  const blocked=new Set();
  if(wave>1){for(let k=0;k<(wave%3===0?2:1);k++){let b=Math.floor(random()*5);if(b===lane)b=(b+2)%5;blocked.add(b);}}
  for(const b of blocked)items.push({s:s+7,lane:b,kind:wave%5===0?'orb':wave%4===0?'goo':'rock'});
  for(let k=0;k<4;k++)items.push({s:s+k*5,lane,kind:k===3&&wave%3===0?'special':'gem'});
  if(wave%5===2)items.push({s:s+13,lane:(lane+2)%5,kind:'special'});
 }
 return items.sort((a,b)=>a.s-b.s).map((item,id)=>({...item,id,theta:LANES[item.lane],done:false}));
}
export function powerStage(power,burst=false){return burst?4:power>=65?3:power>=25?2:power>=10?1:0;}
export function canCollect(playerTheta,itemTheta,jump,kind,mode,power,burst){
 const angle=burst?.74:power>=65?.40:mode==='cozy'?.34:.24;
 return Math.abs(playerTheta-itemTheta)<angle && (jump<2.9||kind==='special'||power>=65||burst);
}
export function collides(playerTheta,itemTheta,jump,kind){return Math.abs(playerTheta-itemTheta)<.23 && jump<(kind==='orb'?2.45:1.8);}
export function rating(collected,total,hits,complete){return complete?(1|(collected>=total*.5?2:0)|(hits===0?4:0)):0;}
export function bits(n){return(n&1)+((n>>1)&1)+((n>>2)&1);}
export function initialRun(level,mode='cozy'){
 return{level:level.id,mode,distance:0,time:0,score:0,gems:0,specials:0,power:0,hits:0,hearts:3,combo:0,maxCombo:0,jump:0,jumpTime:0,invulnerable:0,burst:0,bursts:0,smashes:0,smashTimer:0,clapTimer:0,smashAnim:0,clapAnim:0,collected:0,total:makeCourse(level).filter(i=>i.kind==='gem'||i.kind==='special').length};
}
export function courseX(s){return Math.sin(s/145)*14+Math.sin(s/61)*5;}
export function courseY(s){return Math.sin(s/107)*1.5;}
export function slope(s){return Math.cos(s/145)*14/145+Math.cos(s/61)*5/61;}
