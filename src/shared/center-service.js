import {initializeApp,getApps} from 'firebase/app';
import {getAuth,setPersistence,browserLocalPersistence,GoogleAuthProvider,signInWithPopup,linkWithPopup,signOut,onAuthStateChanged} from 'firebase/auth';
import {getFirestore,doc,getDoc,getDocs,collection,query,where,limit,startAfter,runTransaction,updateDoc,serverTimestamp} from 'firebase/firestore';
import {addToRecord,stats,nickname} from './center-model.js';
// Public browser configuration. Roles are assigned privately through Firestore rules.
const config={apiKey:'AIzaSyCkQdOb7Y_L0DWR3ech1x_KhKqWDt7wCsk',authDomain:'james-game-center.firebaseapp.com',projectId:'james-game-center',storageBucket:'james-game-center.firebasestorage.app',messagingSenderId:'184479595586',appId:'1:184479595586:web:3a2bc02579732535ddc1db'};
export class CenterService{
 constructor(){this.user=null;this.member=null;this.ready=false;this.ticket=0;this.listeners=new Set();}
 subscribe(fn){this.listeners.add(fn);return()=>this.listeners.delete(fn);}
 notify(){for(const fn of this.listeners)fn(this);}
 async init(){const app=getApps().find(a=>a.name==='james-center')||initializeApp(config,'james-center');this.auth=getAuth(app);this.db=getFirestore(app);await setPersistence(this.auth,browserLocalPersistence);await this.auth.authStateReady();this.ready=true;onAuthStateChanged(this.auth,user=>{this.inspect(user).catch(e=>{this.member=null;this.problem=explain(e);this.notify();});});return this;}
 async inspect(user){const ticket=++this.ticket;this.user=user;this.member=null;this.problem='';this.loading=true;this.notify();try{
  if(!user||user.isAnonymous)return;
  if(!user.providerData.some(p=>p.providerId==='google.com')||!user.emailVerified){this.problem='Use Google sign-in to verify your account.';return;}
  const launch=await getDoc(doc(this.db,'_admin','launch'));if(ticket!==this.ticket)return;
  if(!launch.exists()){this.problem='Master setup is not finished. Copy your User ID below and complete the private Firebase launch document.';return;}
  this.masterUid=launch.data().masterUid;const ref=doc(this.db,'members',user.uid);
  if(user.uid===this.masterUid)await runTransaction(this.db,async tx=>{const found=await tx.get(ref);if(!found.exists())tx.set(ref,{nickname:'Sean',role:'master',active:true,joinedAt:serverTimestamp()});});
  const found=await getDoc(ref);if(ticket!==this.ticket)return;
  if(!found.exists()||found.data().active!==true){this.problem='This account is not approved for James Game Center. No player card has been created.';return;}
  this.member={...found.data(),uid:user.uid,role:user.uid===this.masterUid?'master':'player'};
 }finally{if(ticket===this.ticket){this.loading=false;this.notify();}}}
 async login(){if(!this.ready)throw new Error('The account connection is still loading. Try again in a moment.');const provider=new GoogleAuthProvider();provider.setCustomParameters({prompt:'select_account'});try{if(this.auth.currentUser?.isAnonymous)await linkWithPopup(this.auth.currentUser,provider);else await signInWithPopup(this.auth,provider);}catch(e){if(e.code==='auth/credential-already-in-use')await signInWithPopup(this.auth,provider);else throw e;}}
 async logout(){await signOut(this.auth);}
 async refresh(){await this.inspect(this.auth.currentUser);}
 async ownRecord(){if(!this.member)throw new Error('Sign in with an approved account first.');const uid=this.member.uid,snap=await getDoc(doc(this.db,'racerRecords',uid));return {uid,cozy:stats(snap.data()?.cozy),hero:stats(snap.data()?.hero)};}
 async roster(all=false){if(!this.member)throw new Error('Sign in with an approved account first.');if(all&&this.member.role!=='master')throw new Error('Master access required.');let cursor=null;const people=[];
  do{const constraints=[...(all?[]:[where('active','==',true)]),limit(100),...(cursor?[startAfter(cursor)]:[])];const batch=await getDocs(query(collection(this.db,'members'),...constraints));for(const d of batch.docs)people.push({...d.data(),uid:d.id,role:d.id===this.masterUid?'master':'player'});cursor=batch.size===100?batch.docs.at(-1):null;}while(cursor);
  return Promise.all(people.map(async p=>{if(!p.active)return p;try{const record=await getDoc(doc(this.db,'racerRecords',p.uid));return {...p,records:{cozy:stats(record.data()?.cozy),hero:stats(record.data()?.hero)}};}catch{return {...p,unavailable:true};}}));
 }
 async submit(uid,id,run){if(!this.member||this.member.uid!==uid)throw new Error('Account changed; this run stays with its original player.');const userRef=doc(this.db,'members',uid),runRef=doc(userRef,'runs',id),summary=doc(this.db,'racerRecords',uid);
  await runTransaction(this.db,async tx=>{const previous=await tx.get(runRef);if(previous.exists())return;const before=await tx.get(summary),next=addToRecord(before.data(),run);tx.set(runRef,{...run,createdAt:serverTimestamp()});tx.set(summary,{...next,lastRunId:id,updatedAt:serverTimestamp()});},{maxAttempts:3});
 }
 async rename(name){if(!this.member)throw new Error('Sign in first.');await updateDoc(doc(this.db,'members',this.member.uid),{nickname:nickname(name)});this.member.nickname=nickname(name);this.notify();}
 async approve(uid,name){if(this.member?.role!=='master')throw new Error('Master access required.');if(!/^[A-Za-z0-9:_-]{1,128}$/.test(uid))throw new Error('Paste the exact Firebase User ID.');if(uid===this.masterUid)throw new Error('Your master account is already active.');const ref=doc(this.db,'members',uid);await runTransaction(this.db,async tx=>{const old=await tx.get(ref);if(old.exists())tx.update(ref,{nickname:nickname(name),active:true,role:'player'});else tx.set(ref,{nickname:nickname(name),active:true,role:'player',joinedAt:serverTimestamp()});});}
 async setActive(uid,active){if(this.member?.role!=='master'||uid===this.masterUid)throw new Error('The sole master cannot be removed or disabled here.');await updateDoc(doc(this.db,'members',uid),{active:Boolean(active)});}
}
export function explain(e){const c=e?.code||'';if(c.includes('popup-closed-by-user'))return 'Sign-in was cancelled. Your practice progress is unchanged.';if(c.includes('popup-blocked'))return 'Allow pop-ups for this site, then tap Google sign-in again.';if(c.includes('unauthorized-domain'))return 'Add seansommer.github.io to Authentication → Settings → Authorized domains in the James Firebase project.';if(c.includes('operation-not-allowed')||c.includes('configuration-not-found'))return 'Enable Google under Authentication → Sign-in method in the James Firebase project.';if(c.includes('permission-denied'))return 'Account access is not ready. Publish the new James Firestore rules and check the private master setup.';if(c.includes('unavailable')||c.includes('network'))return 'The account connection is unavailable. Try again online; practice mode is still available.';return e?.message||'Connection unavailable. Try again.';}
