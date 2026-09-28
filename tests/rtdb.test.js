// Demo emulator only. No real emails, master matching keys or production data.
import { before, after, beforeEach, afterEach, test } from 'node:test';
import assert from 'node:assert/strict';
import { initializeTestEnvironment, assertFails } from '@firebase/rules-unit-testing';
import { ref, get, set, update, remove, serverTimestamp } from 'firebase/database';
import { buildRules, PLACEHOLDER } from '../scripts/database-rules.mjs';
import { CenterService } from '../src/shared/center-service.js';
import { loginKey } from '../src/shared/identity.js';
let env, ownerKey; const services=[];
const owner = {email:'owner@example.test',displayName:'Sean'};
const other = {email:'friend@example.test',displayName:'Friend'};
const run=()=>({mode:'cozy',world:0,score:250,treasures:5,smashes:1,bursts:0,complete:true,clean:true,medals:5,playedAt:Date.now()});
const make=(uid)=>{const s=new CenterService();s.db=env.authenticatedContext(uid,{firebase:{sign_in_provider:'anonymous'}}).database();s.auth={currentUser:{uid,isAnonymous:true}};s.ready=true;services.push(s);return s;};
const stored=async()=>env.withSecurityRulesDisabled(async c=>(await get(ref(c.database()))).val()||{});
before(async()=>{
 if(!process.env.FIREBASE_DATABASE_EMULATOR_HOST)throw Error('Use the Realtime Database DEMO emulator, never production.');
 ownerKey=await loginKey(owner.email,owner.displayName);
 env=await initializeTestEnvironment({projectId:'demo-james-game-center',database:{rules:JSON.stringify(buildRules(ownerKey))}});
});
beforeEach(async()=>env.clearDatabase());
afterEach(()=>{for(const s of services.splice(0))s.dispose();});
after(async()=>env?.cleanup());

test('Public rule template is locked and contains no usable master key',()=>{
 const text=JSON.stringify(buildRules());assert.ok(text.includes(PLACEHOLDER));assert.ok(!text.includes(ownerKey));
 assert.equal(buildRules().rules['.read'],false);assert.equal(buildRules().rules['.write'],false);
});
test('Wrong email or Sean nickname alone cannot bootstrap, write requests or create a profile',async()=>{
 const s=make('visitor');await assert.rejects(s.login({email:'wrong@example.test',displayName:'Sean'}));
 const all=await stored();assert.equal(all.jamesV1?.members,undefined);assert.equal(all.accessRequests,undefined);
 await assertFails(set(s.ref('members/sean'),{nickname:'Sean',role:'master',active:true,joinedAt:serverTimestamp()}));
});
test('Usual email and nickname create exactly one master automatically with zero scores',async()=>{
 const s=make('first-browser');await s.login(owner);assert.equal(s.member.uid,'sean');assert.equal(s.member.role,'master');
 const all=await stored();assert.deepEqual(Object.keys(all.jamesV1.members),['sean']);assert.equal(all.jamesV1.members.sean.nickname,'Sean');
 assert.equal(all.jamesV1.racerRuns,undefined);assert.equal(all._admin,undefined);
 assert.equal((await s.ownRecord()).cozy.attempts,0);assert.equal((await s.ownRecord()).hero.points,0);
 assert.ok(!JSON.stringify(all).includes(owner.email));
});
test('Same pair signs in on another browser without codes, approval or duplicate card',async()=>{
 const a=make('browser-A'),b=make('browser-B');await a.login(owner);await b.login(owner);
 assert.equal(a.member.uid,b.member.uid);assert.equal(b.member.role,'master');assert.equal((await b.roster(true)).length,1);
 await a.logout();assert.equal(a.member,null);await a.login(owner);assert.equal(a.member.uid,'sean');
});
test('Concurrent first sign-ins converge on one master profile',async()=>{
 const a=make('first-A'),b=make('first-B');await Promise.all([a.login(owner),b.login(owner)]);
 assert.equal(a.member.uid,'sean');assert.equal(b.member.uid,'sean');assert.equal((await a.roster(true)).length,1);
});
test('Legacy root requests and records are left untouched, not migrated into fresh scores',async()=>{
 await env.withSecurityRulesDisabled(c=>set(ref(c.database()),{_admin:{masterUid:'old-device'},accessRequests:{old:{nickname:'Sean'}},members:{old:{nickname:'Sean',role:'master'}},racerRuns:{old:{sample:{score:999}}}}));
 const s=make('new-browser');await s.login(owner);assert.equal((await s.ownRecord()).cozy.points,0);
 const all=await stored();assert.equal(all.racerRuns.old.sample.score,999);assert.equal(all._admin.masterUid,'old-device');
});
test('Root, login directory, private identities and other sessions are not publicly readable',async()=>{
 const s=make('master-browser');await s.login(owner);const v=make('visitor');
 await assertFails(get(ref(v.db)));await assertFails(get(v.ref('members')));await assertFails(get(v.ref('loginLookup')));
 await assertFails(get(v.ref('identities/sean')));await assertFails(get(v.ref('sessions/master-browser')));
 await assertFails(set(v.ref('sessions/visitor'),{profileId:'sean',loginKey:'a'.repeat(64)}));
 const noAuth=env.unauthenticatedContext().database();await assertFails(get(ref(noAuth,'jamesV1/loginLookup/'+ownerKey)));
});
test('Only master can add a player by email and nickname; normal players cannot elevate roles',async()=>{
 const master=make('master-browser');await master.login(owner);const id=await master.approve(other.email,other.displayName);
 const player=make('friend-browser');await player.login(other);assert.equal(player.member.uid,id);assert.equal(player.member.role,'player');
 await assertFails(update(player.ref('members/'+id),{role:'master'}));await assertFails(update(player.ref('members/sean'),{active:false}));
 await assertFails(update(master.ref('members/sean'),{role:'player'}));await assertFails(remove(master.ref('members/sean')));
 await assert.rejects(master.approve(other.email,other.displayName));assert.equal((await master.roster(true)).length,2);
 await master.setActive(id,false);await assertFails(get(player.ref('racerRuns/sean')));
 await master.setActive(id,true);await player.login(other);assert.equal(player.member.role,'player');
});
test('Display nickname changes preserve original sign-in pair and master identity',async()=>{
 const a=make('browser-A');await a.login(owner);await a.rename('Sean Hero');await a.logout();await a.login(owner);
 assert.equal(a.member.uid,'sean');assert.equal(a.member.nickname,'Sean Hero');assert.equal(a.member.role,'master');
});
test('Valid receipts save once; conflicting retry, editing, deletion, negative and injected scores fail',async()=>{
 const s=make('owner-browser');await s.login(owner);const r=run();await s.submit('sean','run-one',r);await s.submit('sean','run-one',r);
 const record=await s.ownRecord();assert.equal(record.cozy.attempts,1);assert.equal(record.cozy.points,250);
 await assert.rejects(s.submit('sean','run-one',{...r,score:500}));
 await assertFails(update(s.ref('racerRuns/sean/run-one'),{score:1000}));await assertFails(remove(s.ref('racerRuns/sean/run-one')));
 await assertFails(set(s.ref('racerRuns/sean/bad'),{...r,score:-1,createdAt:serverTimestamp()}));
 await assertFails(set(s.ref('racerRuns/sean/injected'),{...r,role:'master',createdAt:serverTimestamp()}));
 await assertFails(set(s.ref('racerRecords/sean'),{points:999}));
});
test('Master matching credentials and member identity cannot be replaced through browser writes',async()=>{
 const s=make('owner-browser');await s.login(owner);
 await assertFails(set(s.ref('identities/sean'),{loginKey:'b'.repeat(64)}));
 await assertFails(remove(s.ref('loginLookup/'+ownerKey)));await assertFails(set(s.ref('_admin/masterUid'),'other'));
});
