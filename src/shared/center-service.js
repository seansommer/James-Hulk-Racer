import { initializeApp, getApps } from 'firebase/app';
import { getAuth, setPersistence, browserLocalPersistence, signInAnonymously, onAuthStateChanged } from 'firebase/auth';
import { getDatabase, ref, get, set, update, remove, query, orderByChild, equalTo, onValue, serverTimestamp, push } from 'firebase/database';
import { firebaseConfig } from './firebase-config.js';
import { addToRecord, stats, nickname } from './center-model.js';
import { loginKey } from './identity.js';

// Fresh James profiles only. Legacy root records are neither read, copied nor deleted.
export const ACCOUNT_PATH = 'jamesV1';
export const MASTER_PROFILE = 'sean';
export function recordsFromRuns(runs) {
  let result = { cozy: stats(), hero: stats() };
  for (const [, run] of Object.entries(runs || {}).sort(([a, x], [b, y]) => x.playedAt - y.playedAt || a.localeCompare(b))) result = addToRecord(result, run);
  return result;
}
export class CenterService {
  constructor() {
    this.user = null; this.member = null; this.ready = false; this.loading = false;
    this.ticket = 0; this.listeners = new Set(); this.problem = '';
  }
  subscribe(fn) { this.listeners.add(fn); return () => this.listeners.delete(fn); }
  notify() { for (const fn of this.listeners) fn(this); }
  ref(path = '') { return ref(this.db, ACCOUNT_PATH + (path ? '/' + path : '')); }
  async init() {
    const app = getApps().find(a => a.name === 'james-center') || initializeApp(firebaseConfig, 'james-center');
    this.auth = getAuth(app); this.db = getDatabase(app);
    await setPersistence(this.auth, browserLocalPersistence);
    await this.auth.authStateReady(); this.ready = true;
    this.stopAuth = onAuthStateChanged(this.auth, user => {
      this.stopSession?.(); this.stopMember?.(); this.watchedMember = null;
      if (!user) { this.inspect(null); return; }
      this.stopSession = onValue(this.ref('sessions/' + user.uid), () => this.inspect(user), error => this.fail(error));
    });
    await this.inspect(this.auth.currentUser);
    return this;
  }
  fail(error) {
    ++this.ticket; this.member = null; this.loading = false; this.problem = explain(error); this.notify();
  }
  async inspect(user) {
    const ticket = ++this.ticket;
    this.user = user; this.member = null; this.loading = true; this.problem = ''; this.notify();
    try {
      if (!user) return;
      const session = (await get(this.ref('sessions/' + user.uid))).val();
      if (ticket !== this.ticket) return;
      if (!session) { this.stopMember?.(); this.watchedMember = null; return; }
      const uid = session.profileId;
      const found = (await get(this.ref('members/' + uid))).val();
      if (ticket !== this.ticket) return;
      if (!found?.active) { this.problem = 'Player access is paused. Ask the master to restore it.'; return; }
      this.member = { ...found, uid };
      if (this.watchedMember !== uid) {
        this.stopMember?.(); this.watchedMember = uid;
        this.stopMember = onValue(this.ref('members/' + uid), snapshot => {
          if (this.user?.uid !== user.uid || this.watchedMember !== uid) return;
          const value = snapshot.val();
          if (!value?.active) this.fail(new Error('Player access is paused.'));
          else if (!this.loading) { this.member = { ...value, uid }; this.notify(); }
        }, error => this.fail(error));
      }
    } catch (error) { if (ticket === this.ticket) this.problem = explain(error); }
    finally { if (ticket === this.ticket) { this.loading = false; this.notify(); } }
  }
  async login({ email, displayName } = {}) {
    if (!this.ready) throw new Error('The account connection is still loading. Try again.');
    try {
      const key = await loginKey(email, displayName);
      const user = this.auth.currentUser || (await signInAnonymously(this.auth)).user;
      let uid = (await get(this.ref('loginLookup/' + key))).val();
      if (!uid) {
        // Only the privately reserved email/nickname key can pass the bootstrap rules.
        // Nothing is approved based on first visit, displayed nickname or device ID.
        try {
          await update(this.ref(), {
            ['members/' + MASTER_PROFILE]: { nickname: 'Sean', role: 'master', active: true, joinedAt: serverTimestamp() },
            ['identities/' + MASTER_PROFILE]: { loginKey: key },
            ['loginLookup/' + key]: MASTER_PROFILE,
            ['sessions/' + user.uid]: { profileId: MASTER_PROFILE, loginKey: key }
          });
          uid = MASTER_PROFILE;
        } catch (error) {
          // Another browser may have completed the same bootstrap atomically.
          uid = (await get(this.ref('loginLookup/' + key))).val();
          if (!uid) throw new Error('That email and nickname are not registered. For Sean’s first sign-in, publish the personalized James rules and use your original email with Sean.');
        }
      }
      await set(this.ref('sessions/' + user.uid), { profileId: uid, loginKey: key });
      await this.inspect(user);
    } catch (error) {
      this.problem = explain(error); this.notify(); throw new Error(this.problem);
    }
  }
  async logout() {
    this.stopMember?.(); this.watchedMember = null;
    if (this.auth.currentUser) await remove(this.ref('sessions/' + this.auth.currentUser.uid));
    ++this.ticket; this.member = null; this.loading = false; this.problem = ''; this.notify();
  }
  async refresh() { await this.inspect(this.auth.currentUser); }
  async ownRecord() {
    if (!this.member) throw new Error('Sign in first.');
    return { uid: this.member.uid, ...recordsFromRuns((await get(this.ref('racerRuns/' + this.member.uid))).val()) };
  }
  async roster(all = false) {
    if (!this.member || (all && this.member.role !== 'master')) throw new Error('Approved access required.');
    const target = all ? this.ref('members') : query(this.ref('members'), orderByChild('active'), equalTo(true));
    const people = (await get(target)).val() || {};
    return Promise.all(Object.entries(people).map(async ([uid, p]) => {
      if (!p.active) return { ...p, uid };
      try { return { ...p, uid, records: recordsFromRuns((await get(this.ref('racerRuns/' + uid))).val()) }; }
      catch { return { ...p, uid, unavailable: true }; }
    }));
  }
  async submit(uid, id, run) {
    if (!this.member || this.member.uid !== uid) throw new Error('This result belongs to another player.');
    if (!/^[A-Za-z0-9_-]{1,80}$/.test(id)) throw new Error('Invalid run ID.');
    const target = this.ref('racerRuns/' + uid + '/' + id);
    const existing = (await get(target)).val();
    if (existing) { this.checkReceipt(existing, run); return; }
    try { await set(target, { ...run, createdAt: serverTimestamp() }); }
    catch (error) {
      const saved = (await get(target)).val();
      if (!saved) throw error;
      this.checkReceipt(saved, run);
    }
  }
  checkReceipt(saved, run) {
    if (Object.entries(run).some(([key, value]) => saved[key] !== value)) throw new Error('Run ID conflict. Existing result was not changed.');
  }
  async rename(name) {
    if (!this.member) throw new Error('Sign in first.');
    await update(this.ref('members/' + this.member.uid), { nickname: nickname(name) });
    this.member.nickname = nickname(name); this.notify();
  }
  async approve(email, name) {
    if (this.member?.role !== 'master') throw new Error('Master access required.');
    const key = await loginKey(email, name);
    if ((await get(this.ref('loginLookup/' + key))).exists()) throw new Error('That email and nickname already have a player. Use the existing card.');
    const uid = push(this.ref('members')).key;
    await update(this.ref(), {
      ['members/' + uid]: { nickname: nickname(name), role: 'player', active: true, joinedAt: serverTimestamp() },
      ['identities/' + uid]: { loginKey: key }, ['loginLookup/' + key]: uid
    });
    return uid;
  }
  async setActive(uid, active) {
    if (this.member?.role !== 'master' || uid === MASTER_PROFILE) throw new Error('The sole master cannot be disabled here.');
    await update(this.ref('members/' + uid), { active: Boolean(active) });
  }
  dispose() { ++this.ticket; this.stopAuth?.(); this.stopSession?.(); this.stopMember?.(); this.listeners.clear(); }
}
export function explain(error) {
  const code = String(error?.code || error?.message || '').toLowerCase();
  if (/operation-not-allowed|configuration-not-found|admin-restricted/.test(code)) return 'Enable Anonymous under Authentication → Sign-in method in james-game-center.';
  if (/permission.denied|permission_denied/.test(code)) return 'Publish the new personalized rules under Realtime Database → Rules in james-game-center, then sign in again.';
  if (/network|unavailable|disconnected/.test(code)) return 'Connect to the internet and try again. Local practice is still available.';
  return error?.message || 'Sign-in could not finish. Try again.';
}
