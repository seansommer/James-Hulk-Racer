/** Pure score and ranking functions for James Game Center. */
export const MODES={cozy:'Little Hero',hero:'Superhero'};
export const WORLDS=['Emerald Park','Crystal Caverns','Volcano Jungle'];
export const CATEGORIES=[
 {id:'points',title:'Most Points',label:'lifetime points',icon:'star',value:s=>s.points},
 {id:'adventures',title:'Most Adventures',label:'finished attempts',icon:'flag',value:s=>s.attempts},
 {id:'completions',title:'Most Worlds Completed',label:'world completions',icon:'globe',value:s=>s.completions},
 {id:'average',title:'Highest Average',label:'points / adventure · 3 minimum',icon:'gem',value:s=>s.attempts>=3?Math.round(s.points/s.attempts*100)/100:0},
 {id:'best',title:'Highest Single Run',label:'points in one run',icon:'bolt',value:s=>s.best},
 {id:'streak',title:'Longest Clean Streak',label:'no-bump completions in a row',icon:'shield',value:s=>s.bestStreak}
];
export const integer=(n,max=2000000000)=>Number.isFinite(n)?Math.max(0,Math.min(max,Math.floor(n))):0;
export const nickname=s=>String(s||'').replace(/[^\p{L}\p{N} _-]/gu,'').trim().slice(0,20)||'Hero';
export const emptyStats=()=>({points:0,attempts:0,completions:0,best:0,treasures:0,smashes:0,bursts:0,cleanRuns:0,currentStreak:0,bestStreak:0,lastPlayed:0,worldBest:[0,0,0],medals:[0,0,0]});
export function stats(raw={}){const out=emptyStats();for(const key of Object.keys(out)){if(['worldBest','medals'].includes(key))out[key]=[0,1,2].map(i=>integer(raw?.[key]?.[i],key==='medals'?7:500000));else out[key]=integer(raw?.[key],key==='lastPlayed'?4102444800000:2000000000);}return out;}
export function normalizeRun(result,index,now=Date.now()){
 if(!result||!Object.hasOwn(MODES,result.mode)||!Number.isInteger(index)||index<0||index>2||!Number.isFinite(result.score)||typeof result.complete!=='boolean')throw new Error('Invalid race result');
 const complete=result.complete,hits=integer(result.hits,10000),collected=integer(result.collected,2000),total=integer(result.total,2000);
 return {mode:result.mode,world:index,score:integer(result.score,500000),treasures:collected,smashes:integer(result.smashes,1000),bursts:integer(result.bursts,100),complete,clean:complete&&hits===0,medals:complete?1|(total>0&&collected>=total/2?2:0)|(hits===0?4:0):0,playedAt:integer(now,4102444800000)};
}
export function addRun(raw,run){const s=stats(raw);s.points+=run.score;s.attempts++;s.completions+=Number(run.complete);s.best=Math.max(s.best,run.score);s.treasures+=run.treasures;s.smashes+=run.smashes;s.bursts+=run.bursts;s.cleanRuns+=Number(run.clean);s.currentStreak=run.clean?s.currentStreak+1:0;s.bestStreak=Math.max(s.bestStreak,s.currentStreak);s.lastPlayed=Math.max(s.lastPlayed,run.playedAt);s.worldBest[run.world]=Math.max(s.worldBest[run.world],run.score);s.medals[run.world]|=run.medals;return stats(s);}
export function addToRecord(record,run){return {cozy:stats(record?.cozy),hero:stats(record?.hero),[run.mode]:addRun(record?.[run.mode],run)};}
export const medals=s=>stats(s).medals.reduce((n,v)=>n+(v&1)+((v>>1)&1)+((v>>2)&1),0);
export function rankings(players,mode,category='points'){
 const c=CATEGORIES.find(c=>c.id===category);if(!c||!Object.hasOwn(MODES,mode))return [];
 const rows=players.filter(p=>p.active!==false&&!p.unavailable).map(p=>({...p,value:c.value(stats(p.records?.[mode]))})).filter(p=>p.value>0).sort((a,b)=>b.value-a.value||a.nickname.localeCompare(b.nickname)||a.uid.localeCompare(b.uid));
 let rank=0;return rows.map((p,i)=>{if(!i||p.value!==rows[i-1].value)rank=i+1;return {...p,rank};});
}
export function progressFromRecords(records,name){const a=stats(records?.cozy),b=stats(records?.hero);return {name,bestCozy:a.worldBest,bestHero:b.worldBest,medals:a.medals.map((m,i)=>m|b.medals[i]),runs:a.attempts+b.attempts,gems:a.treasures+b.treasures,smashes:a.smashes+b.smashes,bursts:a.bursts+b.bursts,lastLevel:a.medals[1]||b.medals[1]?2:a.medals[0]||b.medals[0]?1:0};}
