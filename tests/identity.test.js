import test from 'node:test';
import assert from 'node:assert/strict';
import {loginKey,normalizeEmail,normalizeLoginName} from '../src/shared/identity.js';
test('Email/nickname lookup is stable, James-scoped, and contains no raw email',async()=>{
 const a=await loginKey(' TEST@Example.test ','Séan - 4');
 assert.match(a,/^[a-f0-9]{64}$/);
 assert.equal(a,await loginKey('test@example.test','séan4'));
 assert.notEqual(a,await loginKey('other@example.test','séan4'));
 assert.equal(normalizeEmail(' X@Y.COM '),'x@y.com');assert.equal(normalizeLoginName('Sean - 4'),'sean4');
});
test('Malformed email or nickname fails before any network write',async()=>{
 for(const pair of[['','Sean'],['not-email','Sean'],['a@b.test',''],['a@b.test','x'.repeat(21)]])await assert.rejects(loginKey(...pair));
});
