// Local UI fixture only: no production identities or records are created.
import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {mkdir,writeFile} from 'node:fs/promises';
const base=process.env.APP_BASE||'/James-Hulk-Racer/',root='http://127.0.0.1:4173'+base;
const server=spawn(process.execPath,[fileURLToPath(new URL('./serve.mjs',import.meta.url))],{stdio:'inherit',env:{...process.env,APP_BASE:base}});
let browser,page;const errors=[],checks=[],ok=s=>{checks.push(s);console.log('PASS',s);};
await mkdir('dist/qa',{recursive:true});
try{
 for(let i=0;i<70;i++){try{if((await fetch(root)).ok)break;}catch{}await new Promise(r=>setTimeout(r,100));}
 browser=await chromium.launch({headless:true,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const context=await browser.newContext({viewport:{width:1280,height:900},deviceScaleFactor:1});
 await context.addInitScript(()=>localStorage.setItem('james-center:settings:v1',JSON.stringify({quality:'low',music:0,sfx:0,cloud:false})));
 page=await context.newPage();page.setDefaultTimeout(60000);page.on('pageerror',e=>errors.push(e.message));
 await page.goto(root);await page.waitForFunction(()=>window.__jamesCommunity&&(window.__hubReady||window.__jamesReady));
 await page.evaluate(()=>{
  const empty=()=>({points:0,attempts:0,completions:0,best:0,treasures:0,smashes:0,bursts:0,cleanRuns:0,currentStreak:0,bestStreak:0,lastPlayed:0,worldBest:[0,0,0],medals:[0,0,0]});
  const s={ready:true,loading:false,user:null,member:null,pending:null,problem:'',listeners:new Set(),records:{cozy:empty(),hero:empty()},receipts:new Set(),partial:false,
   subscribe(fn){this.listeners.add(fn);return()=>this.listeners.delete(fn);},notify(){for(const f of this.listeners)f(this);},
   async login({email,displayName}){if(email!=='test@example.test'||displayName!=='Sean')throw Error('Incorrect fixture input');this.member={uid:'master-fixture',nickname:'Sean',active:true,role:'master'};this.user={uid:'master-fixture',isAnonymous:true};this.notify();},
   async logout(){this.member=null;this.user=null;this.notify();},async refresh(){this.notify();},async ownRecord(){return structuredClone(this.records);},
   async roster(){return[{...this.member,records:structuredClone(this.records),unavailable:this.partial}];},
   async rename(name){this.member.nickname=name;this.notify();},
   async submit(uid,id,r){if(uid!==this.member?.uid)throw Error('Wrong player');if(this.receipts.has(id))return;this.receipts.add(id);const s=this.records[r.mode];s.points+=r.score;s.attempts++;s.completions+=Number(r.complete);s.best=Math.max(s.best,r.score);s.treasures+=r.treasures;s.smashes+=r.smashes;s.bursts+=r.bursts;s.cleanRuns+=Number(r.clean);s.currentStreak=r.clean?s.currentStreak+1:0;s.bestStreak=Math.max(s.bestStreak,s.currentStreak);s.lastPlayed=r.playedAt;s.worldBest[r.world]=Math.max(s.worldBest[r.world],r.score);s.medals[r.world]|=r.medals;},
   async approve(){throw Error('No extra fixture players');},async setActive(){throw Error('No fixture changes');}};
  window.__fixture=s;window.__jamesCommunity.useService(s);
 });
 await page.locator('.jc-launcher [data-community="hall"]').click();await page.waitForSelector('#jc-center[open]');
 assert.equal(await page.locator('.jc-award').count(),0);assert.equal(await page.locator('#jc-center [data-jc-master]:visible').count(),0);
 assert.equal(await page.locator('#jc-center input[name="email"]').count(),1);assert.equal(await page.locator('#jc-center input[name="displayName"]').count(),1);
 await page.locator('#jc-center input[name="email"]').fill('test@example.test');await page.locator('#jc-center input[name="displayName"]').fill('Sean');
 await page.screenshot({path:'dist/qa/rtdb-sign-in.png'});ok('Visitors use email and nickname; no Google popup or fabricated master');
 await page.locator('#jc-center [data-action="login"]').click();await page.waitForSelector('.jc-award');
 assert.equal(await page.locator('.jc-award').count(),6);assert.equal(await page.locator('.jc-leaderboard tbody tr').count(),0);
 await page.screenshot({path:'dist/qa/hall-of-fame-empty.png'});ok('Six empty award categories, no unearned championships');
 await page.locator('#jc-center [data-community="players"]').click();await page.waitForSelector('.jc-player-tile');assert.equal(await page.locator('.jc-player-tile').count(),1);
 await page.locator('.jc-player-tile').click();await page.waitForSelector('#jc-player[open]');assert.equal(await page.locator('#jc-player-title').textContent(),'Sean');
 assert.equal(await page.locator('.jc-stat-grid>div').count(),12);assert.equal(await page.locator('.jc-world-records>div').count(),3);
 await page.locator('[data-action="close-player"]').click();await page.locator('#jc-search').fill('Nobody');assert.equal(await page.locator('.jc-player-tile').count(),0);
 await page.locator('#jc-search').fill('Sean');assert.equal(await page.locator('.jc-player-tile').count(),1);ok('Sole master card, world records and nickname search preserved');
 await page.locator('#jc-center [data-community="master"]').click();await page.waitForSelector('.jc-admin-list article');assert.equal(await page.locator('.jc-admin-list article').count(),1);
 assert.equal(await page.locator('[data-action="active"]').count(),0);assert.equal(await page.locator('.jc-add-player').getAttribute('open'),null);ok('Master protected; adding players remains opt-in');
 await page.locator('[data-action="close-center"]').click();
 if(base.includes('Hulk-Racer')){
  await page.locator('#play').click();await page.waitForFunction(()=>window.__race.state==='running',null,{timeout:90000});
  await page.evaluate(()=>{const e=window.__race;e.run.score=250;e.run.collected=1;e.run.distance=e.level.length-.01;e.tick(.05);});
  await page.waitForSelector('#results-dialog[open]');await page.waitForFunction(()=>window.__fixture.records.cozy.attempts===1&&!window.__jamesCommunity.flushing);
  assert.equal(await page.evaluate(()=>window.__fixture.receipts.size),1);await page.locator('#result-menu').click();
 }else{
  await page.evaluate(async()=>{const c=window.__jamesCommunity;c.finishRun(c.beginRun(),{mode:'cozy',score:250,complete:true,hits:0,collected:1,total:10,smashes:0,bursts:0},0);await c.flush();});
  await page.waitForFunction(()=>window.__fixture.records.cozy.attempts===1&&!window.__jamesCommunity.flushing);
 }
 ok('Finished adventure updates the captured approved player once');
 await page.locator('.jc-launcher [data-community="hall"]').click();await page.waitForSelector('.jc-leaderboard tbody tr');assert.equal(await page.locator('.jc-leaderboard tbody tr').count(),1);
 await page.locator('[data-action="category"][data-category="average"]').click();assert.equal(await page.locator('.jc-leaderboard tbody tr').count(),0);
 await page.locator('[data-action="mode"][data-score-mode="hero"]').click();assert.equal(await page.locator('.jc-leaderboard tbody tr').count(),0);
 await page.locator('[data-action="mode"][data-score-mode="cozy"]').click();await page.locator('[data-action="category"][data-category="points"]').click();
 await page.locator('.jc-player-link').click();await page.waitForSelector('#jc-player[open]');await page.locator('[data-action="card-mode"][data-score-mode="hero"]').click();
 assert.ok((await page.locator('.jc-game-line').innerText()).includes('Superhero'));await page.locator('[data-action="close-player"]').click();await page.locator('[data-action="mode"][data-score-mode="cozy"]').click();
 ok('Ranked player links, three-attempt average minimum and separated difficulties');
 await page.evaluate(async()=>{window.__fixture.partial=true;await window.__jamesCommunity.load();});assert.equal(await page.locator('.jc-award').count(),0);
 await page.evaluate(async()=>{window.__fixture.partial=false;await window.__jamesCommunity.load();});ok('Missing records do not produce false winners');
 await page.setViewportSize({width:390,height:844});await page.waitForTimeout(250);
 assert.ok(await page.evaluate(()=>document.getElementById('jc-center').scrollWidth<=document.getElementById('jc-center').clientWidth+1));
 await page.screenshot({path:'dist/qa/hall-of-fame-phone.png'});await page.locator('#jc-center [data-community="players"]').click();await page.waitForSelector('.jc-player-tile');await page.locator('.jc-player-tile').click();
 await page.waitForSelector('#jc-player[open]');assert.ok(await page.evaluate(()=>document.getElementById('jc-player').scrollWidth<=document.getElementById('jc-player').clientWidth+1));
 const close=await page.locator('[data-action="close-player"]').boundingBox();assert.ok(close.x>=0&&close.x+close.width<=390&&close.y>=0);
 await page.screenshot({path:'dist/qa/player-card-phone.png'});await page.locator('[data-action="close-player"]').click();await page.locator('[data-action="close-center"]').click();ok('Phone cards and Hall fit, close controls remain reachable');
 await page.evaluate(async()=>window.__fixture.logout());await page.locator('.jc-launcher [data-community="hall"]').click();assert.equal(await page.locator('.jc-award').count(),0);assert.equal(await page.locator('#jc-center [data-jc-master]:visible').count(),0);
 assert.deepEqual(errors,[]);ok('Sign-out clears private records and master controls; no uncaught errors');
 await writeFile('dist/qa/center-report.json',JSON.stringify({result:'PASS',scope:'Chromium UI fixture, not live Firebase login',checks,errors},null,2));
}catch(error){try{await page?.screenshot({path:'dist/qa/center-failure.png'});}catch{}await writeFile('dist/qa/center-report.json',JSON.stringify({result:'FAIL',checks,errors,error:error.stack},null,2));console.error(error);process.exitCode=1;}
finally{await browser?.close();server.kill();}
