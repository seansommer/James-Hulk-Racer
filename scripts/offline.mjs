import {readdir,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const files=[];
async function walk(dir){for(const file of await readdir(dir,{withFileTypes:true})){const p=dir+'/'+file.name;if(file.isDirectory())await walk(p);else if(!p.includes('/qa/')&&!p.endsWith('/sw.js'))files.push('./'+p.slice(5));}}
await walk('dist');
const version=createHash('sha256').update(files.sort().join('\n')+(process.env.GITHUB_SHA||Date.now())).digest('hex').slice(0,12);
const script=`const CACHE='james-racer-${version}',FILES=${JSON.stringify(['./',...files])};
self.addEventListener('install',event=>{
 event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(FILES)).then(()=>self.skipWaiting()));
});
self.addEventListener('activate',event=>{
 event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(key=>key.startsWith('james-racer-')&&key!==CACHE).map(key=>caches.delete(key)))).then(()=>self.clients.claim()));
});
self.addEventListener('fetch',event=>{
 const url=new URL(event.request.url);
 if(event.request.method!=='GET'||url.origin!==self.location.origin||!url.pathname.startsWith(new URL(self.registration.scope).pathname))return;
 if(event.request.mode==='navigate'){
  const key=url.pathname.endsWith('/')?url.pathname+'index.html':url.pathname;
  event.respondWith(fetch(event.request).then(response=>{if(response.ok){const copy=response.clone();event.waitUntil(caches.open(CACHE).then(cache=>cache.put(key,copy)));}return response;}).catch(()=>caches.match(key).then(cached=>cached||caches.match('./'))));
  return;
 }
 event.respondWith(caches.match(event.request).then(cached=>cached||fetch(event.request)));
});`;
await writeFile('dist/sw.js',script);
console.log('Offline shell prepared:',files.length,'files. Firebase requests are never cached.');
