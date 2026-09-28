// Generate RTDB rules. The owner's matching key belongs ONLY in their private console copy.
import { writeFileSync, mkdirSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
export const NAMESPACE = 'jamesV1';
export const PLACEHOLDER = 'OWNER_LOGIN_KEY_GOES_HERE';
export function buildRules(masterKey = PLACEHOLDER) {
  if (masterKey !== PLACEHOLDER && !/^[a-f0-9]{64}$/.test(masterKey)) throw new Error('Invalid owner matching key');
  const app = "root.child('jamesV1')";
  const session = `${app}.child('sessions').child(auth.uid).child('profileId')`;
  const approved = `(auth !== null && ${session}.isString() && ${app}.child('members').child(${session}.val()).child('active').val() === true)`;
  const master = `(${approved} && ${session}.val() === 'sean' && ${app}.child('members/sean/role').val() === 'master')`;
  const owner = '(auth !== null && auth.uid === $uid)';
  const memberOwner = `(${approved} && ${session}.val() === $uid)`;
  const next = 'newData.parent().parent()';
  const bootstrap = `(auth !== null && $uid === 'sean' && !${app}.child('members/sean').exists() && ${next}.child('identities/sean/loginKey').val() === '${masterKey}')`;
  const int = max => ({ '.validate': `newData.isNumber() && newData.val() >= 0 && newData.val() <= ${max} && newData.val() % 1 === 0` });
  const text = max => ({ '.validate': `newData.isString() && newData.val().length > 0 && newData.val().length <= ${max}` });
  const key = () => ({ '.validate': "newData.isString() && newData.val().matches(/^[a-f0-9]{64}$/)" });
  const rules = { '.read': false, '.write': false, jamesV1: {
    members: {
      '.indexOn': ['active'],
      '.read': `${master} || (${approved} && query.orderByChild === 'active' && query.equalTo === true)`,
      '$uid': {
        '.read': `${master} || (${approved} && data.child('active').val() === true)`,
        '.write': `newData.exists() && (${master} || (!data.exists() && ${bootstrap}) || (${memberOwner} && newData.child('role').val() === data.child('role').val() && newData.child('active').val() === data.child('active').val()))`,
        '.validate': `newData.hasChildren(['nickname','role','active','joinedAt']) && ${next}.child('identities').child($uid).child('loginKey').isString() && ${next}.child('loginLookup').child(${next}.child('identities').child($uid).child('loginKey').val()).val() === $uid`,
        nickname: text(20),
        role: { '.validate': "$uid === 'sean' ? newData.val() === 'master' : newData.val() === 'player'" },
        active: { '.validate': "newData.isBoolean() && ($uid !== 'sean' || newData.val() === true)" },
        joinedAt: { '.validate': 'newData.isNumber() && (data.exists() ? newData.val() === data.val() : newData.val() === now)' },
        '$other': { '.validate': false }
      }
    },
    identities: { '$uid': {
      '.read': `${memberOwner} || ${master}`,
      '.write': `!data.exists() && newData.exists() && (${bootstrap} || ${master})`,
      '.validate': `newData.hasChildren(['loginKey']) && ${next}.child('members').child($uid).exists() && ${next}.child('loginLookup').child(newData.child('loginKey').val()).val() === $uid`,
      loginKey: key(), '$other': { '.validate': false }
    } },
    loginLookup: { '$key': {
      '.read': "auth !== null && $key.matches(/^[a-f0-9]{64}$/)",
      '.write': `auth !== null && !data.exists() && newData.exists() && (${master} || ($key === '${masterKey}' && newData.val() === 'sean' && !${app}.child('members/sean').exists()))`,
      '.validate': `newData.isString() && $key.matches(/^[a-f0-9]{64}$/) && ${next}.child('members').child(newData.val()).child('active').val() === true && ${next}.child('identities').child(newData.val()).child('loginKey').val() === $key`
    } },
    sessions: { '$uid': {
      '.read': owner, '.write': owner,
      '.validate': `newData.hasChildren(['profileId','loginKey']) && newData.child('profileId').isString() && newData.child('loginKey').isString() && ${next}.child('loginLookup').child(newData.child('loginKey').val()).val() === newData.child('profileId').val() && ${next}.child('members').child(newData.child('profileId').val()).child('active').val() === true`,
      profileId: text(128), loginKey: key(), '$other': { '.validate': false }
    } },
    racerRuns: { '$uid': {
      '.read': `${approved} && ${app}.child('members').child($uid).child('active').val() === true`,
      '.indexOn': ['playedAt'],
      '$id': {
        '.write': `${memberOwner} && !data.exists() && newData.exists() && $id.matches(/^[A-Za-z0-9_-]{1,80}$/)`,
        '.validate': "newData.hasChildren(['mode','world','score','treasures','smashes','bursts','complete','clean','medals','playedAt','createdAt']) && (newData.child('complete').val() === true ? (newData.child('medals').val() % 2 === 1 && (newData.child('clean').val() === true ? newData.child('medals').val() >= 5 : newData.child('medals').val() < 5)) : (newData.child('medals').val() === 0 && newData.child('clean').val() === false))",
        mode: { '.validate': "newData.val() === 'cozy' || newData.val() === 'hero'" }, world: int(2), score: int(500000), treasures: int(2000), smashes: int(1000), bursts: int(100),
        complete: { '.validate': 'newData.isBoolean()' }, clean: { '.validate': 'newData.isBoolean()' }, medals: int(7),
        playedAt: { '.validate': 'newData.isNumber() && newData.val() >= 0 && newData.val() % 1 === 0 && newData.val() <= now + 600000' },
        createdAt: { '.validate': 'newData.val() === now' }, '$other': { '.validate': false }
      }
    } }
  } };
  return { rules };
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  // Public builds are fail-closed templates; never put the owner's value in CI or GitHub.
  const json = JSON.stringify(buildRules(), null, 2) + '\n';
  writeFileSync('firebase-database.rules.json', json);
  if (process.argv.includes('--publish')) { mkdirSync('dist', { recursive: true }); writeFileSync('dist/firebase-database.rules.json', json); }
  console.log('Generated PUBLIC RULE TEMPLATE. Use the owner-personalized copy in Firebase for initial Sean sign-in.');
}
