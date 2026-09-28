import test from 'node:test';
import assert from 'node:assert/strict';
import {LEVELS,LANES,makeCourse,powerStage,canCollect,collides,rating,bits,initialRun,courseX,courseY} from '../src/game/logic.js';
for(const level of LEVELS){
 test(`${level.name}: repeatable course and valid positions`,()=>{const a=makeCourse(level);assert.deepEqual(a,makeCourse(level));assert.ok(a.length>100);for(let i=0;i<a.length;i++){assert.equal(a[i].id,i);assert.ok(a[i].s>=30&&a[i].s<level.length);assert.ok(LANES.includes(a[i].theta));if(i)assert.ok(a[i].s>=a[i-1].s);}});
 test(`${level.name}: no fully blocked rows`,()=>{const obstacles=makeCourse(level).filter(i=>!['gem','special'].includes(i.kind));const rows=new Map();for(const o of obstacles){if(!rows.has(o.s))rows.set(o.s,new Set());rows.get(o.s).add(o.lane);}for(const row of rows.values())assert.ok(row.size<=2);});
 test(`${level.name}: coherent initial run`,()=>{const r=initialRun(level);assert.equal(r.score,0);assert.equal(r.mode,'cozy');assert.equal(r.hearts,3);assert.equal(r.total,makeCourse(level).filter(i=>['gem','special'].includes(i.kind)).length);for(let s=0;s<level.length;s+=10){assert.ok(Number.isFinite(courseX(s)));assert.ok(Number.isFinite(courseY(s)));}});
}
test('Power thresholds and active super burst',()=>{assert.deepEqual([0,9,10,24,25,64,65,99].map(p=>powerStage(p)),[0,0,1,1,2,2,3,3]);assert.equal(powerStage(100,true),4);});
test('Collection tolerance grows with power',()=>{assert.equal(canCollect(0,.3,0,'gem','cozy',0,false),true);assert.equal(canCollect(0,.3,0,'gem','hero',0,false),false);assert.equal(canCollect(0,.35,0,'gem','hero',65,false),true);assert.equal(canCollect(0,.7,0,'gem','hero',100,true),true);assert.equal(canCollect(0,.9,0,'gem','hero',100,true),false);});
test('Jump dodges hazards; neighboring lane remains safe',()=>{assert.equal(collides(0,0,0,'rock'),true);assert.equal(collides(0,.44,0,'rock'),false);assert.equal(collides(0,0,2,'rock'),false);assert.equal(collides(0,0,2,'orb'),true);assert.equal(collides(0,0,3,'orb'),false);});
test('Three independent medals, never awarded on a failed run',()=>{assert.equal(rating(60,100,0,true),7);assert.equal(bits(7),3);assert.equal(rating(30,100,2,true),1);assert.equal(rating(60,100,2,true),3);assert.equal(rating(30,100,0,true),5);assert.equal(rating(100,100,0,false),0);});
