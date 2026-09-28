import { initializeApp, getApps } from 'firebase/app';
import { getAuth, setPersistence, browserLocalPersistence, signInAnonymously } from 'firebase/auth';
import { getDatabase, ref, get, runTransaction, serverTimestamp } from 'firebase/database';
import { firebaseConfig } from './firebase-config.js';
let target;
export async function connect() {
  const app = getApps().find(a => a.name === 'james-center') || initializeApp(firebaseConfig, 'james-center');
  const auth = getAuth(app);
  await setPersistence(auth, browserLocalPersistence); await auth.authStateReady();
  if (!auth.currentUser) await signInAnonymously(auth);
  target = ref(getDatabase(app), 'practiceBackups/' + auth.currentUser.uid);
  return (await get(target)).val();
}
export async function write(profile) {
  if (!target) throw new Error('Practice backup is not connected.');
  const { sanitize, merge } = await import('./profile.js');
  const snapshot = sanitize(profile);
  await runTransaction(target, current => ({ ...merge(snapshot, current || {}), name: snapshot.name, updatedAt: serverTimestamp() }), { applyLocally: false });
}
