import { initializeApp, getApps } from 'firebase/app';
import { getAuth, setPersistence, browserLocalPersistence, signInAnonymously, onAuthStateChanged } from 'firebase/auth';
import { getDatabase, ref, get, set, update, remove, query, orderByChild, equalTo, onValue, serverTimestamp } from 'firebase/database';
import { firebaseConfig } from './firebase-config.js';
import { addToRecord, stats, nickname } from './center-model.js';
import { loginKey } from './identity.js';

// Immutable run receipts are the source of truth. No writable aggregate counters.
export function recordsFromRuns(runs) {
  let result = { cozy: stats(), hero: stats() };
  for (const [, run] of Object.entries(runs || {}).sort(([a, x], [b, y]) => x.playedAt - y.playedAt || a.localeCompare(b))) {
    result = addToRecord(result, run);
  }
  return result;
}

export class CenterService {
  constructor() {
    this.user = null; this.member = null; this.ready = false; this.loading = false;
    this.ticket = 0; this.listeners = new Set(); this.pending = null; this.problem = '';
  }
  subscribe(fn) { this.listeners.add(fn); return () => this.listeners.delete(fn); }
  notify() { for (const fn of this.listeners) fn(this); }
  ref(path) { return ref(this.db, path); }
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
    this.member = null; this.loading = false; this.problem = explain(error); this.notify();
  }
  async inspect(user) {
    const ticket = ++this.ticket;
    this.user = user; this.member = null; this.pending = null; this.loading = true; this.problem = ''; this.notify();
    try {
      if (!user) return;
      const session = (await get(this.ref('sessions/' + user.uid))).val();
      if (ticket !== this.ticket) return;
      if (!session) {
        this.stopMember?.(); this.watchedMember = null;
        const pending = (await get(this.ref('accessRequests/' + user.uid))).val();
        if (ticket !== this.ticket) return;
        this.pending = pending;
        if (!pending) return;
        const master = (await get(this.ref('_admin/masterUid'))).val();
        if (ticket !== this.ticket) return;
        if (master === user.uid) {
          await this.activateMaster(user.uid, pending);
          // The realtime session listener will also refresh; generations prevent stale results.
          return await this.inspect(this.auth.currentUser || user);
        }
        this.problem = 'Your details are saved for approval, not a player card. For the first launch, set your User ID as _admin/masterUid in Realtime Database, then press Check access.';
        return;
      }
      const uid = session.profileId;
      const found = (await get(this.ref('members/' + uid))).val();
      if (ticket !== this.ticket) return;
      if (!found?.active) { this.problem = 'This player is not approved or access is paused.'; return; }
      this.member = { ...found, uid }; this.pending = null;
      if (this.watchedMember !== uid) {
        this.stopMember?.(); this.watchedMember = uid;
        this.stopMember = onValue(this.ref('members/' + uid), snapshot => {
          if (this.user?.uid !== user.uid || this.watchedMember !== uid) return;
          const value = snapshot.val();
          if (!value?.active) this.fail(new Error('Player access is paused.'));
          else if (!this.loading) { this.member = { ...value, uid }; this.notify(); }
        }, error => this.fail(error));
      }
    } catch (error) {
      if (ticket === this.ticket) this.problem = explain(error);
    } finally {
      if (ticket === this.ticket) { this.loading = false; this.notify(); }
    }
  }
  async activateMaster(uid, request) {
    const existing = (await get(this.ref('members/' + uid))).val();
    if (existing) throw new Error('This account already exists. Sign in with its original email and nickname.');
    // Master authority comes exclusively from a console-assigned UID, never a name or first visit.
    await update(this.ref(), {
      ['members/' + uid]: { nickname: 'Sean', role: 'master', active: true, joinedAt: serverTimestamp() },
      ['identities/' + uid]: { loginKey: request.loginKey },
      ['loginLookup/' + request.loginKey]: uid,
      ['sessions/' + uid]: { profileId: uid, loginKey: request.loginKey },
      ['accessRequests/' + uid]: null
    });
  }
  async login({ email, displayName } = {}) {
    if (!this.ready) throw new Error('The account connection is still loading. Try again.');
    const key = await loginKey(email, displayName);
    const user = this.auth.currentUser || (await signInAnonymously(this.auth)).user;
    const uid = (await get(this.ref('loginLookup/' + key))).val();
    if (uid) {
      try { await set(this.ref('sessions/' + user.uid), { profileId: uid, loginKey: key }); }
      catch (error) {
        this.user = user; this.pending = { nickname: nickname(displayName) };
        this.problem = 'Access was not granted. Master access on another browser requires authorizing that browser’s User ID in _admin/masterDevices. Other players may be paused.';
        this.notify(); throw new Error(this.problem);
      }
    } else {
      const previous = (await get(this.ref('accessRequests/' + user.uid))).val();
      await set(this.ref('accessRequests/' + user.uid), { nickname: nickname(displayName), loginKey: key, createdAt: previous?.createdAt || serverTimestamp() });
    }
    await this.inspect(user);
  }
  async logout() {
    // End the app session, retaining the underlying anonymous device identity for protected master re-entry.
    this.stopMember?.(); this.watchedMember = null;
    if (this.auth.currentUser) {
      await remove(this.ref('sessions/' + this.auth.currentUser.uid));
      await remove(this.ref('accessRequests/' + this.auth.currentUser.uid)).catch(() => {});
    }
    ++this.ticket; this.member = null; this.pending = null; this.loading = false; this.problem = ''; this.notify();
  }
  async refresh() { await this.inspect(this.auth.currentUser); }
  async ownRecord() {
    if (!this.member) throw new Error('Sign in with an approved player first.');
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
      // A simultaneous retry may already have saved the same immutable receipt.
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
  async approve(uid, name) {
    if (this.member?.role !== 'master') throw new Error('Master access required.');
    if (!/^[A-Za-z0-9_-]{1,128}$/.test(uid) || uid === this.member.uid) throw new Error('Enter the intended new player’s exact User ID.');
    const request = (await get(this.ref('accessRequests/' + uid))).val();
    if (!request?.loginKey) throw new Error('Have this player enter an email and nickname in James Game Center first, then share their User ID.');
    await update(this.ref(), {
      ['members/' + uid]: { nickname: nickname(name), role: 'player', active: true, joinedAt: serverTimestamp() },
      ['identities/' + uid]: { loginKey: request.loginKey },
      ['loginLookup/' + request.loginKey]: uid
    });
  }
  async setActive(uid, active) {
    if (this.member?.role !== 'master' || uid === this.member.uid) throw new Error('The sole master cannot be disabled here.');
    await update(this.ref('members/' + uid), { active: Boolean(active) });
  }
}
export function explain(error) {
  const code = String(error?.code || error?.message || '').toLowerCase();
  if (/operation-not-allowed|configuration-not-found|admin-restricted/.test(code)) return 'Enable Anonymous sign-in in the james-game-center Firebase project.';
  if (/permission.denied|permission_denied/.test(code)) return 'Access is not ready. Publish the new Realtime Database rules and check your master setup. Do not use the old Firestore rules.';
  if (/network|unavailable|disconnected/.test(code)) return 'Connect to the internet and try again. Local practice is still available.';
  return error?.message || 'Account connection unavailable. Try again.';
}
