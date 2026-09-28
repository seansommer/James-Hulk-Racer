// Generate the exact RTDB JSON used by emulator tests and the downloadable setup file.
// This is a build-time serializer, not a Firebase deployment or production-data mutation.
import { writeFileSync, mkdirSync } from 'node:fs';
const session = "root.child('sessions').child(auth.uid).child('profileId')";
const masterId = "root.child('_admin/masterUid').val()";
const device = `(auth.uid === ${masterId} || root.child('_admin/masterDevices').child(auth.uid).val() === true)`;
const approved = `(auth !== null && ${session}.isString() && root.child('members').child(${session}.val()).child('active').val() === true && (${session}.val() !== ${masterId} || ${device}))`;
const master = `(${approved} && ${session}.val() === ${masterId})`;
const bootstrap = `(auth !== null && auth.uid === ${masterId} && auth.uid === $uid)`;
const owner = `(auth !== null && auth.uid === $uid)`;
const memberOwner = `(${approved} && ${session}.val() === $uid)`;
const nextRoot = 'newData.parent().parent()';
const int = max => ({ '.validate': `newData.isNumber() && newData.val() >= 0 && newData.val() <= ${max} && newData.val() % 1 === 0` });
const text = max => ({ '.validate': `newData.isString() && newData.val().length > 0 && newData.val().length <= ${max}` });
const triple = max => ({ '.validate': "newData.hasChildren(['0','1','2'])", '0': int(max), '1': int(max), '2': int(max), '$other': { '.validate': false } });
const rules = {
  '.read': false, '.write': false,
  _admin: {
    masterUid: { '.read': 'auth !== null', '.write': false },
    masterDevices: { '$uid': { '.read': owner, '.write': false } }
  },
  accessRequests: {
    '.read': master,
    '$uid': {
      '.read': `${owner} || ${master}`,
      '.write': `${master} || (${owner} && (!newData.exists() || !root.child('members').child($uid).exists()))`,
      '.validate': "newData.hasChildren(['nickname','loginKey','createdAt'])",
      nickname: text(20),
      loginKey: { '.validate': "newData.isString() && newData.val().matches(/^[a-f0-9]{64}$/)" },
      createdAt: { '.validate': "newData.isNumber() && (data.exists() ? newData.val() === data.val() : newData.val() === now)" },
      '$other': { '.validate': false }
    }
  },
  members: {
    '.indexOn': ['active'],
    '.read': `${master} || (${approved} && query.orderByChild === 'active' && query.equalTo === true)`,
    '$uid': {
      '.read': `${owner} || ${master} || (${approved} && data.child('active').val() === true)`,
      '.write': `newData.exists() && (${master} || (!data.exists() && ${bootstrap}) || (${memberOwner} && newData.child('role').val() === data.child('role').val() && newData.child('active').val() === data.child('active').val()))`,
      '.validate': `newData.hasChildren(['nickname','role','active','joinedAt']) && ${nextRoot}.child('identities').child($uid).child('loginKey').isString() && ${nextRoot}.child('loginLookup').child(${nextRoot}.child('identities').child($uid).child('loginKey').val()).val() === $uid`,
      nickname: text(20),
      role: { '.validate': `$uid === ${masterId} ? newData.val() === 'master' : newData.val() === 'player'` },
      active: { '.validate': `newData.isBoolean() && ($uid !== ${masterId} || newData.val() === true)` },
      joinedAt: { '.validate': 'newData.isNumber() && (data.exists() ? newData.val() === data.val() : newData.val() === now)' },
      '$other': { '.validate': false }
    }
  },
  identities: {
    '$uid': {
      '.read': `${owner} || ${memberOwner} || ${master}`,
      '.write': `!data.exists() && newData.exists() && (${bootstrap} || ${master})`,
      '.validate': `newData.hasChildren(['loginKey']) && newData.child('loginKey').val() === root.child('accessRequests').child($uid).child('loginKey').val() && ${nextRoot}.child('members').child($uid).exists()`,
      loginKey: { '.validate': "newData.isString() && newData.val().matches(/^[a-f0-9]{64}$/)" },
      '$other': { '.validate': false }
    }
  },
  loginLookup: {
    '$key': {
      '.read': "auth !== null && $key.matches(/^[a-f0-9]{64}$/)",
      '.write': `auth !== null && !data.exists() && newData.exists() && (auth.uid === ${masterId} || ${master})`,
      '.validate': `newData.isString() && $key.matches(/^[a-f0-9]{64}$/) && ${nextRoot}.child('members').child(newData.val()).child('active').val() === true && ${nextRoot}.child('identities').child(newData.val()).child('loginKey').val() === $key`
    }
  },
  sessions: {
    '$uid': {
      '.read': owner,
      '.write': owner,
      '.validate': `newData.hasChildren(['profileId','loginKey']) && newData.child('profileId').isString() && newData.child('loginKey').isString() && ${nextRoot}.child('loginLookup').child(newData.child('loginKey').val()).val() === newData.child('profileId').val() && ${nextRoot}.child('members').child(newData.child('profileId').val()).child('active').val() === true && (newData.child('profileId').val() !== ${masterId} || ${device})`,
      profileId: text(128), loginKey: { '.validate': "newData.isString() && newData.val().matches(/^[a-f0-9]{64}$/)" },
      '$other': { '.validate': false }
    }
  },
  racerRuns: {
    '$uid': {
      '.read': `${approved} && root.child('members').child($uid).child('active').val() === true`,
      '.indexOn': ['playedAt'],
      '$id': {
        '.write': `${memberOwner} && !data.exists() && newData.exists() && $id.matches(/^[A-Za-z0-9_-]{1,80}$/)`,
        '.validate': "newData.hasChildren(['mode','world','score','treasures','smashes','bursts','complete','clean','medals','playedAt','createdAt']) && (newData.child('complete').val() === true ? (newData.child('medals').val() % 2 === 1 && (newData.child('clean').val() === true ? newData.child('medals').val() >= 5 : newData.child('medals').val() < 5)) : (newData.child('medals').val() === 0 && newData.child('clean').val() === false))",
        mode: { '.validate': "newData.val() === 'cozy' || newData.val() === 'hero'" },
        world: int(2), score: int(500000), treasures: int(2000), smashes: int(1000), bursts: int(100),
        complete: { '.validate': 'newData.isBoolean()' }, clean: { '.validate': 'newData.isBoolean()' }, medals: int(7),
        playedAt: { '.validate': 'newData.isNumber() && newData.val() >= 0 && newData.val() % 1 === 0 && newData.val() <= now + 600000' },
        createdAt: { '.validate': 'newData.val() === now' },
        '$other': { '.validate': false }
      }
    }
  },
  practiceBackups: {
    '$uid': {
      '.read': owner, '.write': owner,
      '.validate': "newData.hasChildren(['name','bestCozy','bestHero','medals','runs','gems','smashes','bursts','lastLevel','updatedAt'])",
      name: text(20), bestCozy: triple(500000), bestHero: triple(500000), medals: triple(7),
      runs: int(9999999), gems: int(9999999), smashes: int(9999999), bursts: int(9999999), lastLevel: int(2),
      updatedAt: { '.validate': 'newData.val() === now' }, '$other': { '.validate': false }
    }
  }
};
const json = JSON.stringify({ rules }, null, 2) + '\n';
writeFileSync('firebase-database.rules.json', json);
if (process.argv.includes('--publish')) {
  mkdirSync('dist', { recursive: true });
  writeFileSync('dist/firebase-database.rules.json', json);
}
console.log('Generated locked-down James Realtime Database rules. No live project was modified.');
