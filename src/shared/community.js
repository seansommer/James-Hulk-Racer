// Preserve the Hall of Fame and card views; restore the familiar email/nickname form.
import { installCommunity as installCore } from './community-core.js';
import { icon, esc, toast } from './ui.js';
import './rtdb-account.css';
export function installCommunity(options) {
  const c = installCore(options);
  c.accountMarkup = function () {
    const s = this.service, member = s?.member, ready = Boolean(s?.ready && !s.loading);
    return `<div class="jc-account"><span class="eyebrow">${member ? 'YOUR JAMES ACCOUNT' : 'MASTER-ONLY LAUNCH'}</span>
      <h3>${member ? icon('shield') + ' ' + esc(member.nickname) : 'Welcome back. Let’s play.'}</h3>
      <p>${member ? `${member.role === 'master' ? 'Master' : 'Player'} access · Your signed-in adventures appear on your Player Card and Hall of Fame.` : 'Sign in with your usual email address and nickname. Sean’s first sign-in creates the one master account with fresh scores.'}</p>
      ${s?.problem ? `<p class="jc-warning" role="status">${esc(s.problem)}</p>` : ''}
      ${this.connectionError ? `<p class="jc-warning">${esc(this.connectionError)}</p><button class="btn secondary" data-action="connect">Retry connection</button>` : ''}
      ${member ? `<div class="jc-account-actions"><button class="btn" data-community="mine">${icon('user')} My Player Card</button><button class="text-btn" data-action="logout">Sign out</button></div>` : `
      <form class="jc-signin" aria-label="James email and nickname sign-in">
        <label>Email address<input name="email" type="email" maxlength="254" autocomplete="email" required value="${esc(this.loginEmail || '')}" placeholder="Your email address"></label>
        <label>Nickname<input name="displayName" maxlength="20" autocomplete="nickname" required value="${esc(this.loginName || '')}" placeholder="Your nickname"></label>
        <p class="small-note">No password or codes. Your email is not displayed on player cards.</p>
        <button class="btn" type="button" data-action="login" ${ready ? '' : 'disabled'}>${icon('user')} ${ready ? 'Sign in' : 'Preparing sign-in…'}</button>
      </form>`}
      <p class="small-note">Only Sean is set up initially. Other players are added by the master. Email and nickname are trust-based sign-in details, not verified email authentication.</p><p class="jc-sync" role="status"></p></div>`;
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
      if (this.service.member) { this.loginEmail = ''; this.loginName = ''; toast('Welcome, ' + this.service.member.nickname + '.'); }
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
    const details = this.body.querySelector('.jc-add-player');
    if (!details) return;
    details.innerHTML = `<summary>Add a player later</summary><p>Leave this closed to keep Sean as the only player. To add someone later, enter the email and nickname they will use to sign in. No device IDs are needed.</p>
      <form id="jc-approve-form"><label for="jc-new-email">Player email address</label><input id="jc-new-email" type="email" required maxlength="254" autocomplete="off">
      <label for="jc-new-name">Player nickname</label><input id="jc-new-name" required maxlength="20" autocomplete="off">
      <label class="jc-confirm"><input type="checkbox" required> I intend to add this player.</label><button class="btn" type="submit">Add player</button><p id="jc-admin-status" role="status"></p></form>`;
    details.querySelector('form').onsubmit = async e => {
      e.preventDefault(); const form = e.target, button = form.querySelector('button'), status = form.querySelector('[role="status"]');
      if (!form.reportValidity()) return;
      button.disabled = true; status.textContent = 'Saving player…';
      try { await this.service.approve(form.querySelector('#jc-new-email').value.trim(), form.querySelector('#jc-new-name').value.trim()); await this.load(); toast('Player added. They can sign in with that email and nickname.'); }
      catch (error) { status.textContent = error.message || 'Player could not be added.'; button.disabled = false; }
    };
  };
  c.renderAccount(); return c;
}
