import {initializeApp,getApps} from 'firebase/app';
import {getAuth,setPersistence,browserLocalPersistence,signInAnonymously} from 'firebase/auth';
import {getFirestore,doc,getDoc,runTransaction,serverTimestamp} from 'firebase/firestore';
// Public browser configuration, not an admin secret. Access is enforced by firestore.rules.
const firebaseConfig={apiKey:'AIzaSyCkQdOb7Y_L0DWR3ech1x_KhKqWDt7wCsk',authDomain:'james-game-center.firebaseapp.com',projectId:'james-game-center',storageBucket:'james-game-center.firebasestorage.app',messagingSenderId:'184479595586',appId:'1:184479595586:web:3a2bc02579732535ddc1db'};
let ref,db;
export async function connect(){const app=getApps().find(a=>a.name==='james-center')||initializeApp(firebaseConfig,'james-center');const auth=getAuth(app);await setPersistence(auth,browserLocalPersistence);await auth.authStateReady();if(!auth.currentUser)await signInAnonymously(auth);db=getFirestore(app);ref=doc(db,'players',auth.currentUser.uid);const snap=await getDoc(ref);return snap.exists()?snap.data():null;}
export async function write(profile){if(!ref)throw new Error('Cloud backup is not connected.');const {sanitize,merge}=await import('./profile.js');const snapshot=sanitize(profile);await runTransaction(db,async tx=>{const current=await tx.get(ref),data=current.exists()?merge(snapshot,current.data()):snapshot;data.name=snapshot.name;tx.set(ref,{...data,updatedAt:serverTimestamp()});});}
