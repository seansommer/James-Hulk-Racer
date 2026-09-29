// Actual viewer script in a minimal DOM stub: NOT a browser/layout/device test.
import fs from 'node:fs';import vm from 'node:vm';import assert from 'node:assert/strict';
const root=process.argv[2];if(!root)throw new Error('Pass the review output directory.');
const html=fs.readFileSync(root+'/review.html','utf8'),data=JSON.parse(fs.readFileSync(root+'/manifest.json','utf8'));
const elements=[],ids=new Map();let callback,time=100;
class Node {constructor(tag='div'){this.tagName=tag;this.children=[];this.style={};this.attributes={};this.className='';this.value='';this.checked=false;this.src='';elements.push(this);}append(...ns){this.children.push(...ns);}setAttribute(k,v){this.attributes[k]=v;}getAttribute(k){return this.attributes[k];}click(){this.onclick?.({target:this});}}
for(const m of html.matchAll(/id="([^"]+)"/g))ids.set(m[1],new Node());
const document={createElement:t=>new Node(t),getElementById:k=>ids.get(k),querySelectorAll:s=>elements.filter(e=>s.split(',').some(c=>e.className.split(' ').includes(c.trim().slice(1)))),addEventListener(){}};
const window={REVIEW_DATA:data},ctx={window,document,console,requestAnimationFrame:f=>callback=f};
const code=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]).join('\n');vm.runInNewContext(code,ctx);
const audit=window.reviewAudit,checks=[],pass=s=>checks.push(s),advance=n=>{for(let i=0;i<n;i++){time+=1000/60;callback(time);}};
assert.equal(audit.cards.length,12);assert.ok(audit.cards.every(s=>!s.running&&s.i===0));pass('Twelve clips start paused');
ids.get('play-all').click();advance(24);assert.ok(audit.cards.find(s=>s.c.id==='run').i>0);pass('Run advances under actual viewer timing code');
advance(150);assert.ok(audit.cards.filter(s=>!s.c.loop&&s.c.frames.length).every(s=>!s.running&&s.i===s.c.frames.length-1));pass('Available one-shots stop on final pose');
ids.get('pause-all').click();const before=audit.cards.map(s=>s.i).join(',');advance(40);assert.equal(audit.cards.map(s=>s.i).join(','),before);pass('Pause preserves all frame indices');
ids.get('reset-all').click();assert.ok(audit.cards.every(s=>s.i===0&&!s.running));pass('Reset restores frame one');
const action=audit.cards.find(s=>s.c.id==='smash');action.thumbs[4].click();assert.equal(action.i,4);assert.equal(action.img.src,action.c.frames[4].file);pass('Thumbnail selection binds the correct source frame');
ids.get('background').onchange({target:{value:'dark'}});ids.get('size').onchange({target:{value:'120'}});ids.get('onion').onchange({target:{checked:true}});assert.equal(audit.state.bg,'dark');assert.equal(audit.state.height,120);assert.equal(action.old.style.display,'block');pass('Backdrop, size and onion state propagate');
ids.get('pair').value='2';ids.get('pair').onchange();const b=ids.get('compare-b').src;ids.get('compare-flip').click();assert.notEqual(ids.get('compare-b').src,b);assert.equal(ids.get('compare-b').src,ids.get('compare-a').src);pass('Transition comparison toggles the reference');
ids.get('speed').onchange({target:{value:'0.5'}});assert.equal(audit.state.speed,.5);pass('Playback speed control changes time multiplier');
assert.equal(audit.errors.length,0);assert.ok(audit.cards.filter(s=>!s.c.frames.length).every(s=>!s.running));pass('No script-state errors; absent clips stay paused');
fs.writeFileSync(root+'/playback-logic-checks.json',JSON.stringify({result:'PASS',availableFrames:data.availableFrames,testEnvironment:'Node VM plus minimal DOM stub; NOT a browser rendering, layout, image-decoding or device test',checks},null,2)+'\n');console.log(checks.length+' playback-logic checks passed (not a browser test)');
