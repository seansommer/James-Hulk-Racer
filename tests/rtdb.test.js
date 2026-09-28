// All permission and adapter tests run ONLY on the demo Realtime Database emulator.
import { before, after, beforeEach, test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { initializeTestEnvironment, assertSucceeds, assertFails } from '@firebase/rules-unit-testing';
import { ref, get, set, update, remove, query, orderByChild, equalTo, serverTimestamp } from 'firebase/database';
import { CenterService, recordsFromRuns } from '../src/shared/center-service.js';
import { loginKey } from '../src/shared/identity.js';
import { normalizeRun } from '../src/shared/center-model.js';
let env; const services=[]; const MASTER='master-device';
const db=uid=>uid ? env.authenticatedContext(uid,{firebase:{sign_in_provider:'anonymous'}}).database() : env.unauthenticatedContext().database();
const service=uid=>{const s=new CenterService();s.ready=true;s.auth={currentUser:{uid,isAnonymous:true}};s.user=s.auth.currentUser;s.db=db(uid);services.push(s);return s;};
const request=async(uid,name='Sean',email='owner@example.test')=>{const key=await loginKey(email,name);const r={nickname:name,loginKey:key,createdAt:serverTimestamp()};await set(ref(db(uid),'accessRequests/'+uid),r);return r;};
const activate=async()=>{const s=service(MASTER);const r=await request(MASTER);await s.activateMaster(MASTER,r);await s.inspect(s.user);assert.equal(s.member?.role,'master');return s;};
const rawRun=(mode='cozy',points=250)=>normalizeRun({mode,score:points,complete:true,hits:0,collected:10,total:20,smashes:2,bursts:1},0);
before(async()=>{
 if(!process.env.FIREBASE_DATABASE_EMULATOR_HOST)throw new Error('Demo database emulator required; never contact production.');
 env=await initializeTestEnvironment({projectId:'demo-james-game-center',database:{rules:readFileSync('firebase-database.rules.json','utf8')}});
});
beforeEach(async()=>{for(const s of services.splice(0)){s.stopMember?.();s.stopSession?.();}await env.clearDatabase();await env.withSecurityRulesDisabled(async context=>set(ref(context.database()),{_admin:{masterUid:MASTER}}));});
after(async()=>{for(const s of services){s.stopMember?.();s.stopSession?.();}await env?.cleanup();});

test('No public reads/writes, no first-visitor master claim, no private lookup enumeration',async()=>{
 await assertFails(get(ref(db(null))));await assertFails(set(ref(db(null),'anything'),true));
 const stranger=db('stranger');await assertFails(set(ref(stranger,'_admin/masterUid'),'stranger'));
 await assertFails(set(ref(stranger,'_admin/masterDevices/stranger'),true));
 await assertFails(get(ref(stranger,'loginLookup')));await assertFails(get(ref(stranger,'identities')));
 await assertFails(get(ref(stranger,'members')));await assertFails(get(ref(stranger,'racerRuns')));
 await assertFails(set(ref(stranger,'members/stranger'),{nickname:'Sean',role:'master',active:true,joinedAt:serverTimestamp()}));
});
test('Only console-designated master activates; initial roster contains exactly Sean and no scores',async()=>{
 const stranger=service('stranger');await request('stranger');await stranger.inspect(stranger.user);assert.equal(stranger.member,null);
 const s=await activate();const people=await s.roster(true);assert.equal(people.length,1);assert.equal(people[0].nickname,'Sean');assert.equal(people[0].records.cozy.attempts,0);
 await assertFails(remove(s.ref('members/'+MASTER)));await assertFails(update(s.ref('members/'+MASTER),{active:false}));
 await assertFails(update(s.ref('members/'+MASTER),{role:'player'}));await assertFails(set(s.ref('_admin/masterUid'),'other'));
});
test('Knowing master email and nickname does not grant master access on an unapproved browser',async()=>{
 const s=await activate(),other=db('second-device'),key=await loginKey('owner@example.test','Sean');
 assert.equal((await get(ref(other,'loginLookup/'+key))).val(),MASTER);
 await assertFails(set(ref(other,'sessions/second-device'),{profileId:MASTER,loginKey:key}));
 await env.withSecurityRulesDisabled(async c=>set(ref(c.database(),'_admin/masterDevices/second-device'),true));
 await assertSucceeds(set(ref(other,'sessions/second-device'),{profileId:MASTER,loginKey:key}));
 await assertSucceeds(get(ref(other,'members')));
 await env.withSecurityRulesDisabled(async c=>remove(ref(c.database(),'_admin/masterDevices/second-device')));
 await assertFails(get(ref(other,'members')));
 await s.logout();assert.equal(s.member,null);await s.login({email:'owner@example.test',displayName:'Sean'});assert.equal(s.member?.role,'master');
});
test('Future users require explicit approval; normal email/nickname re-entry works and never promotes roles',async()=>{
 const master=await activate(),pending=service('player-one');await pending.login({email:'player@example.test',displayName:'Player One'});assert.equal(pending.member,null);
 assert.equal((await master.roster()).length,1);await master.approve('player-one','Player One');
 await pending.login({email:'player@example.test',displayName:'Player One'});assert.equal(pending.member?.role,'player');
 const second=service('player-browser-two');await second.login({email:'player@example.test',displayName:'Player One'});assert.equal(second.member?.uid,'player-one');
 await assertFails(update(second.ref('members/player-one'),{role:'master'}));await assertFails(set(second.ref('_admin/masterDevices/player-browser-two'),true));
 await assertFails(get(second.ref('members')));await assertSucceeds(get(query(second.ref('members'),orderByChild('active'),equalTo(true))));
 await assertFails(get(second.ref('identities/'+MASTER)));await assertFails(get(second.ref('accessRequests')));
 await second.rename('New Display');assert.equal((await get(second.ref('members/player-one/nickname'))).val(),'New Display');
 await master.setActive('player-one',false);await assertFails(get(query(second.ref('members'),orderByChild('active'),equalTo(true))));
 await assertFails(set(second.ref('racerRuns/player-one/no-access'),{...rawRun(),createdAt:serverTimestamp()}));
});
test('Runs are append-only, account-owned, idempotent across retries, with separate difficulty totals',async()=>{
 const s=await activate(),r=rawRun();await s.submit(MASTER,'run-1',r);await s.submit(MASTER,'run-1',r);
 const one=await s.ownRecord();assert.equal(one.cozy.attempts,1);assert.equal(one.cozy.points,250);assert.equal(one.hero.points,0);
 await s.submit(MASTER,'run-2',rawRun('hero',400));const two=await s.ownRecord();assert.equal(two.hero.points,400);assert.equal(two.cozy.points,250);
 await assert.rejects(s.submit(MASTER,'run-1',{...r,score:999}));await assertFails(remove(s.ref('racerRuns/'+MASTER+'/run-1')));
 await assertFails(update(s.ref('racerRuns/'+MASTER+'/run-1'),{score:999}));await assertFails(set(s.ref('racerRecords/'+MASTER),{cozy:{points:9999999}}));
 await assertFails(set(s.ref('racerRuns/someone-else/run-x'),{...r,createdAt:serverTimestamp()}));
 const merged=recordsFromRuns({b:{...r,playedAt:2000},a:{...r,playedAt:1000}});assert.equal(merged.cozy.bestStreak,2);
});
test('Invalid fields, values, completion medals, timestamps and forged sessions are rejected',async()=>{
 const s=await activate(),base={...rawRun(),createdAt:serverTimestamp()};let i=0;
 for(const wrong of [{score:-1},{score:500001},{score:1.5},{mode:'cheat'},{world:3},{medals:8},{complete:false},{clean:false},{role:'master'},{email:'private@example.test'},{createdAt:1},{playedAt:Date.now()+3600000}]) {
  await assertFails(set(s.ref('racerRuns/'+MASTER+'/bad-'+i++),{...base,...wrong}));
 }
 const missing={...base};delete missing.score;await assertFails(set(s.ref('racerRuns/'+MASTER+'/missing'),missing));
 await assertFails(set(s.ref('sessions/'+MASTER),{profileId:MASTER,loginKey:'0'.repeat(64)}));
 await assertFails(update(s.ref('members/'+MASTER),{email:'private@example.test'}));
});
test('Practice backup stays owner-private and does not enter the roster',async()=>{
 const other=db('practice'),p={name:'Jamesy',bestCozy:[0,0,0],bestHero:[0,0,0],medals:[0,0,0],runs:0,gems:0,smashes:0,bursts:0,lastLevel:0,updatedAt:serverTimestamp()};
 await assertSucceeds(set(ref(other,'practiceBackups/practice'),p));await assertSucceeds(get(ref(other,'practiceBackups/practice')));
 await assertFails(get(ref(db('outsider'),'practiceBackups/practice')));await assertFails(get(ref(other,'practiceBackups')));
 await assertFails(set(ref(other,'practiceBackups/practice'),{...p,medals:[8,0,0]}));
 const s=await activate();assert.equal((await s.roster()).length,1);
});
