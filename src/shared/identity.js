/** Same password-free email/nickname entry as the family hub. Not email verification. */
export function normalizeEmail(value) { return String(value || '').trim().toLowerCase(); }
export function normalizeLoginName(value) {
  return String(value || '').normalize('NFKC').trim().toLowerCase().replace(/[^\p{L}\p{N}]/gu, '');
}
export async function loginKey(email, name) {
  email = normalizeEmail(email);
  const nickname = normalizeLoginName(name);
  if (email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) throw new Error('Enter a valid email address.');
  if (!nickname || String(name).trim().length > 20) throw new Error('Enter a nickname of 1–20 characters.');
  const bytes = new TextEncoder().encode('james-rtdb-v1|' + email + '|' + nickname);
  const hash = await crypto.subtle.digest('SHA-256', bytes);
  return [...new Uint8Array(hash)].map(n => n.toString(16).padStart(2, '0')).join('');
}
