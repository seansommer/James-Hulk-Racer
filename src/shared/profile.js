// Shared, same-origin progress. No emails, passwords, or public child profiles.
const KEY='james-center:profile:v1',SETTINGS='james-center:settings:v1';
const defaults=()=>({name:'Jamesy',bestCozy:[0,0,0],bestHero:[0,0,0],medals:[0,0,0],runs:0,gems:0,smashes:0,bursts:0,lastLevel:0});
const number=(v,max=9999999)=>Number.isFinite(Number(v))?Math.max(0,Math.min(max,Math.floor(Number(v)))):0;
export const cleanName=s=>String(s||'').replace(/[^\p{L}\p{N} _-]/gu,'').trim().slice(0,20)||'Jamesy';
export function sanitize(p={}){if(!p||typeof p!=='object')p={};const d=defaults();d.name=cleanName(p.name);for(const key of['bestCozy','bestHero','medals'])d[key]=[0,1,2].map(i=>number(p[key]?.[i],key==='medals'?7:500000));for(const k of['runs','gems','smashes','bursts'])d[k]=number(p[k]);d.lastLevel=number(p.lastLevel,2);return d;}
function read(k,fallback){try{return JSON.parse(localStorage.getItem(k))||fallback;}catch{return fallback;}}
export const profile=sanitize(read(KEY,defaults()));
export const settings=Object.assign({music:.25,sfx:.65,reduced:matchMedia('(prefers-reduced-motion: reduce)').matches,quality:'auto',cloud:false,mode:'cozy'},read(SETTINGS,{}));
settings.music=Math.max(0,Math.min(1,Number(settings.music)||0));settings.sfx=Math.max(0,Math.min(1,Number(settings.sfx)||0));settings.reduced=Boolean(settings.reduced);settings.cloud=Boolean(settings.cloud);if(!['auto','high','low'].includes(settings.quality))settings.quality='auto';if(!['cozy','hero'].includes(settings.mode))settings.mode='cozy';
export let storageAvailable=true;let cloud=null,connecting=null;
export function save(){Object.assign(profile,sanitize(profile));try{localStorage.setItem(KEY,JSON.stringify(profile));}catch{storageAvailable=false;}window.dispatchEvent(new Event('james-profile'));}
export function saveSettings(){try{localStorage.setItem(SETTINGS,JSON.stringify(settings));}catch{storageAvailable=false;}}
export function merge(a,b){const out=sanitize(a),other=sanitize(b);for(const k of['bestCozy','bestHero'])out[k]=out[k].map((v,i)=>Math.max(v,other[k][i]));out.medals=out.medals.map((v,i)=>v|other.medals[i]);for(const k of['runs','gems','smashes','bursts','lastLevel'])out[k]=Math.max(out[k],other[k]);return out;}
export function record(result,index){profile.runs++;profile.gems+=result.collected;profile.smashes+=result.smashes;profile.bursts+=result.bursts;const key=result.mode==='hero'?'bestHero':'bestCozy';profile[key][index]=Math.max(profile[key][index],result.score);profile.medals[index]|=result.medals;if(result.complete)profile.lastLevel=Math.min(2,index+1);save();sync();}
function status(detail){window.dispatchEvent(new CustomEvent('james-cloud',{detail}));}
export async function connectCloud(){if(connecting)return connecting;connecting=(async()=>{status('Connecting…');try{cloud=await import('./cloud.js');const remote=await cloud.connect();if(remote){const merged=merge(profile,remote);if(profile.name==='Jamesy')merged.name=cleanName(remote.name);Object.assign(profile,merged);save();}await cloud.write(profile);settings.cloud=true;saveSettings();status('Private cloud backup connected');return true;}catch(e){cloud=null;settings.cloud=false;saveSettings();status(cloudError(e));return false;}finally{connecting=null;}})();return connecting;}
function cloudError(e){const code=e?.code||'';if(code.includes('permission-denied'))return 'Saved on this device. Firebase Firestore rules still need to be published.';if(code.includes('configuration-not-found')||code.includes('operation-not-allowed')||code.includes('admin-restricted'))return 'Saved on this device. Enable Anonymous sign-in in the James Firebase project.';return 'Cloud backup is unavailable. Your game still saves on this device.';}
export async function sync(){if(!cloud||!settings.cloud)return;try{await cloud.write(profile);status('Private cloud backup connected');}catch(e){status(cloudError(e));}}
export function rename(name){profile.name=cleanName(name);save();sync();}
window.addEventListener('storage',e=>{if(e.key===KEY){Object.assign(profile,sanitize(read(KEY,profile)));window.dispatchEvent(new Event('james-profile'));}});
export const medalCount=()=>profile.medals.reduce((a,m)=>a+(m&1)+((m>>1)&1)+((m>>2)&1),0);
export const trophies=()=>[
 {title:'First adventure',description:'Go on your first run.',earned:profile.runs>0,icon:'flag'},
 {title:'Gem collector',description:'Collect 100 treasures.',earned:profile.gems>=100,icon:'gem'},
 {title:'Smash squad',description:'Smash 15 obstacles.',earned:profile.smashes>=15,icon:'bolt'},
 {title:'Super Jamesy',description:'Reach full power.',earned:profile.bursts>0,icon:'sun'},
 {title:'World explorer',description:'Finish all three worlds.',earned:profile.medals.every(m=>(m&1)>0),icon:'globe'},
 {title:'Three-star hero',description:'Earn all three medals in a world.',earned:profile.medals.some(m=>m===7),icon:'star'}
];
