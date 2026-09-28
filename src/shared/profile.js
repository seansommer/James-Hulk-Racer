// Practice is separate from every signed-in player's cached progress.
const KEY='james-center:profile:v1',SETTINGS='james-center:settings:v1';
const defaults=()=>({name:'Jamesy',bestCozy:[0,0,0],bestHero:[0,0,0],medals:[0,0,0],runs:0,gems:0,smashes:0,bursts:0,lastLevel:0});
const number=(v,max=9999999)=>Number.isFinite(Number(v))?Math.max(0,Math.min(max,Math.floor(Number(v)))):0;
export const cleanName=s=>String(s||'').replace(/[^\p{L}\p{N} _-]/gu,'').trim().slice(0,20)||'Jamesy';
export function sanitize(p={}){if(!p||typeof p!=='object')p={};const d=defaults();d.name=cleanName(p.name);for(const key of['bestCozy','bestHero','medals'])d[key]=[0,1,2].map(i=>number(p[key]?.[i],key==='medals'?7:500000));for(const k of['runs','gems','smashes','bursts'])d[k]=number(p[k]);d.lastLevel=number(p.lastLevel,2);return d;}
function read(k,fallback){try{return JSON.parse(localStorage.getItem(k))||fallback;}catch{return fallback;}}
let activeUid=null;const keyFor=uid=>uid?`james-center:member-progress:v1:${uid}`:KEY;
export const profile=sanitize(read(KEY,defaults()));
export const profileOwner=()=>activeUid;
export const settings=Object.assign({music:.25,sfx:.65,reduced:matchMedia('(prefers-reduced-motion: reduce)').matches,quality:'auto',cloud:false,mode:'cozy'},read(SETTINGS,{}));
settings.music=Math.max(0,Math.min(1,Number(settings.music)||0));settings.sfx=Math.max(0,Math.min(1,Number(settings.sfx)||0));settings.reduced=Boolean(settings.reduced);settings.cloud=Boolean(settings.cloud);if(!['auto','high','low'].includes(settings.quality))settings.quality='auto';if(!['cozy','hero'].includes(settings.mode))settings.mode='cozy';
export let storageAvailable=true;let cloud=null,connecting=null;
function persist(uid,data){try{localStorage.setItem(keyFor(uid),JSON.stringify(data));}catch{storageAvailable=false;}}
export function save(){Object.assign(profile,sanitize(profile));persist(activeUid,profile);window.dispatchEvent(new Event('james-profile'));}
export function usePlayerProfile(uid=null,name,source){const changed=activeUid!==uid;activeUid=uid;cloud=null;if(changed||source)Object.assign(profile,sanitize(source||read(keyFor(uid),defaults())));if(uid&&name)profile.name=cleanName(name);save();}
export function saveSettings(){try{localStorage.setItem(SETTINGS,JSON.stringify(settings));}catch{storageAvailable=false;}}
export function merge(a,b){const out=sanitize(a),other=sanitize(b);for(const k of['bestCozy','bestHero'])out[k]=out[k].map((v,i)=>Math.max(v,other[k][i]));out.medals=out.medals.map((v,i)=>v|other.medals[i]);for(const k of['runs','gems','smashes','bursts','lastLevel'])out[k]=Math.max(out[k],other[k]);return out;}
export function record(result,index,owner=activeUid){const p=owner===activeUid?profile:sanitize(read(keyFor(owner),defaults()));p.runs++;p.gems+=result.collected;p.smashes+=result.smashes;p.bursts+=result.bursts;const key=result.mode==='hero'?'bestHero':'bestCozy';p[key][index]=Math.max(p[key][index],result.score);p.medals[index]|=result.medals;if(result.complete)p.lastLevel=Math.min(2,index+1);if(owner===activeUid){save();if(!owner)sync();}else persist(owner,sanitize(p));}
function status(detail){window.dispatchEvent(new CustomEvent('james-cloud',{detail}));}
// Legacy anonymous backups remain readable by their owners; never merge into ranked records.
export async function connectCloud(){if(activeUid){status('Your approved player records save automatically.');return false;}if(connecting)return connecting;connecting=(async()=>{status('Connecting…');const owner=activeUid;try{cloud=await import('./cloud.js');const remote=await cloud.connect();if(owner!==activeUid)return false;if(remote){const merged=merge(profile,remote);if(profile.name==='Jamesy')merged.name=cleanName(remote.name);Object.assign(profile,merged);save();}await cloud.write(profile);settings.cloud=true;saveSettings();status('Private practice backup connected');return true;}catch{cloud=null;settings.cloud=false;saveSettings();status('Practice backup is unavailable. Your local progress is unchanged.');return false;}finally{connecting=null;}})();return connecting;}
export async function sync(){if(activeUid||!cloud||!settings.cloud)return;try{await cloud.write(profile);status('Private practice backup connected');}catch{status('Practice is saved on this device.');}}
export function rename(name){profile.name=cleanName(name);save();if(!activeUid)sync();}
window.addEventListener('storage',e=>{if(e.key===keyFor(activeUid)){Object.assign(profile,sanitize(read(keyFor(activeUid),profile)));window.dispatchEvent(new Event('james-profile'));}});
export const medalCount=()=>profile.medals.reduce((a,m)=>a+(m&1)+((m>>1)&1)+((m>>2)&1),0);
export const trophies=()=>[
 {title:'First adventure',description:'Go on your first run.',earned:profile.runs>0,icon:'flag'},
 {title:'Gem collector',description:'Collect 100 treasures.',earned:profile.gems>=100,icon:'gem'},
 {title:'Smash squad',description:'Smash 15 obstacles.',earned:profile.smashes>=15,icon:'bolt'},
 {title:'Super Jamesy',description:'Reach full power.',earned:profile.bursts>0,icon:'sun'},
 {title:'World explorer',description:'Finish all three worlds.',earned:profile.medals.every(m=>(m&1)>0),icon:'globe'},
 {title:'Three-star hero',description:'Earn all three medals in a world.',earned:profile.medals.some(m=>m===7),icon:'star'}
];
