// Keep the original Hall of Fame and cards; change only account entry and help.
import { installCommunity as installCore } from './community-core.js';
import { icon, esc, toast } from './ui.js';
import './rtdb-account.css';
export function installCommunity(options) {
  const c = installCore(options);
  c.accountMarkup = function () {
    const s = this.service, member = s?.member, pending = Boolean(s?.pending);
    const ready = Boolean(s?.ready && !s.loading), setup = Boolean(s?.user && (member || pending));
    return `<div class="jc-account"><span class="eyebrow">${member ? 'YOUR JAMES ACCOUNT' : 'MASTER-ONLY LAUNCH'}</span>
      <h3>${member ? icon('shield') + ' ' + esc(member.nickname) : 'One player. All your James adventures.'}</h3>
      <p>${member ? `${member.role === 'master' ? 'Master' : 'Player'} access · Signed-in results appear on your Player Card and Hall of Fame.` : 'Use your email and nickname, just like the other Game Centers. No Google sign-in or password is required.'}</p>
      ${s?.problem ? `<p class="jc-warning" role="status">${esc(s.problem)}</p>` : ''}
      ${this.connectionError ? `<p class="jc-warning">${esc(this.connectionError)}</p><button class="btn secondary" data-action="connect">Retry account connection</button>` : ''}
      ${member ? `<div class="jc-account-actions"><button class="btn" data-community="mine">${icon('user')} My Player Card</button><button class="btn secondary" data-action="account-refresh">Check access</button><button class="text-btn" data-action="logout">Sign out</button></div>` : `
      <form class="jc-signin" aria-label="James email and nickname sign-in">
        <label>Email address<input name="email" type="email" maxlength="254" autocomplete="email" required value="${esc(this.loginEmail || '')}" placeholder="Your email address"></label>
        <label>Sign-in nickname<input name="displayName" maxlength="20" autocomplete="nickname" required value="${esc(this.loginName || '')}" placeholder="Your nickname"></label>
        <p class="small-note">Email matches your account details; it is not shown on cards. This is trust-based entry, not email verification.</p>
        <button class="btn" type="button" data-action="login" ${ready ? '' : 'disabled'}>${icon('user')} ${ready ? 'Sign in / Request access' : 'Preparing sign-in…'}</button>
      </form>${pending ? '<div class="jc-account-actions"><button class="btn secondary" data-action="account-refresh">Check access</button><button class="text-btn" data-action="logout">Cancel / Sign out</button></div>' : ''}`}
      ${setup ? `<details class="jc-uid" ${pending ? 'open' : ''}><summary>Account setup · Your User ID</summary><p>For the first master, copy this exact ID into Realtime Database at <code>_admin/masterUid</code>. Other accounts require explicit approval.</p><code>${esc(s.user.uid)}</code><button class="text-btn" data-action="copy-uid">Copy User ID</button></details>` : ''}
      <p class="small-note">Only your privately designated master can activate the first card. Visitors can practice; requesting access does not create a card or add scores.</p><p class="jc-sync" role="status"></p></div>`;
  };
  const action = c.action.bind(c);
  c.action = async function (button) {
    if (button.dataset.action !== 'login') return action(button);
    const form = button.closest('form');
    if (!form || !form.reportValidity() || !this.service?.ready) return;
    this.loginEmail = form.elements.email.value.trim(); this.loginName = form.elements.displayName.value.trim();
    try { localStorage.setItem('james-center:accounts:enabled', '1'); } catch {}
    button.disabled = true;
    try {
      await this.service.login({ email: this.loginEmail, displayName: this.loginName });
      if (this.service.member) { this.loginEmail = ''; this.loginName = ''; }
    } catch (error) { toast(error.message || 'Sign-in could not finish. Try again.'); }
    finally { button.disabled = false; this.renderAccount(); if (this.dialog.open && !this.service.member) this.renderLocked(); }
  };
  document.addEventListener('submit', event => {
    if (!event.target.matches('.jc-signin')) return;
    event.preventDefault(); event.target.querySelector('[data-action="login"]').click();
  });
  const renderAccount = c.renderAccount.bind(c);
  c.renderAccount = function () {
    renderAccount();
    const note = document.getElementById('nickname-note');
    if (note && this.service?.member) note.textContent = 'Display nickname only. Keep using your original sign-in nickname when signing in.';
  };
  const drawMaster = c.drawMaster.bind(c);
  c.drawMaster = function () {
    drawMaster();
    const help = this.body.querySelector('.jc-add-player > p');
    if (help) help.textContent = 'Leave this closed to keep Sean as the only approved player. Later, have a player enter their email and nickname here and share their James User ID. Confirm the intended person before approving.';
  };
  c.renderAccount(); return c;
}
