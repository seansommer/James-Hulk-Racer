/** One key per result avoids overwriting another tab's pending runs. */
export class RunQueue {
  constructor(storage) { this.storage=storage; this.memory=new Map(); this.durable=true; }
  key(uid,id) { return `james-center:run:v1:${uid}:${id}`; }
  put(uid,id,run) {
    const key=this.key(uid,id),entry={uid,id,run};
    this.memory.set(key,entry);
    try { this.storage.setItem(key,JSON.stringify(entry)); }
    catch { this.durable=false; }
    return this.durable;
  }
  entries(uid) {
    const prefix=this.key(uid,''),found=new Map();
    try { for(let i=0;i<this.storage.length;i++) { const key=this.storage.key(i); if(!key?.startsWith(prefix))continue;
      try { const entry=JSON.parse(this.storage.getItem(key)); if(entry?.uid===uid&&typeof entry.id==='string'&&entry.run&&this.key(uid,entry.id)===key)found.set(key,entry); } catch {} }
    } catch { this.durable=false; }
    for(const [key,entry] of this.memory)if(key.startsWith(prefix))found.set(key,entry);
    return [...found.values()].sort((a,b)=>a.run.playedAt-b.run.playedAt||a.id.localeCompare(b.id));
  }
  remove(uid,id) { const key=this.key(uid,id);this.memory.delete(key);try{this.storage.removeItem(key);}catch{this.durable=false;} }
}
