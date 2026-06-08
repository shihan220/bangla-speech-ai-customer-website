'use strict';

// ── Toast auto-dismiss ───────────────────────────────────────
document.querySelectorAll('.toast[data-auto-dismiss]').forEach(toast => {
  setTimeout(() => {
    toast.style.transition = 'opacity 0.4s, transform 0.4s';
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(8px)';
    setTimeout(() => toast.remove(), 400);
  }, 3500);
});

// ── Delete modal ─────────────────────────────────────────────
const overlay  = document.getElementById('deleteModal');
const modalDesc  = document.getElementById('modalDesc');
const cancelBtn  = document.getElementById('modalCancel');
const confirmBtn = document.getElementById('modalConfirm');
const actionForm = document.getElementById('deleteActionForm');

document.querySelectorAll('[data-delete-url]').forEach(btn => {
  btn.addEventListener('click', () => {
    const url  = btn.dataset.deleteUrl;
    const name = btn.dataset.deleteName || 'this item';
    modalDesc.textContent = `"${name}" will be permanently removed.`;
    actionForm.action = url;
    overlay.classList.add('open');
  });
});

cancelBtn?.addEventListener('click', () => overlay.classList.remove('open'));

overlay?.addEventListener('click', e => {
  if (e.target === overlay) overlay.classList.remove('open');
});

confirmBtn?.addEventListener('click', () => {
  overlay.classList.remove('open');
  actionForm.submit();
});

// ── Mobile sidebar toggle ────────────────────────────────────
const hamburger = document.getElementById('dbHamburger');
const sidebar   = document.getElementById('dbSidebar');
const overlay2  = document.getElementById('sidebarOverlay');

hamburger?.addEventListener('click', () => {
  sidebar.classList.toggle('open');
  overlay2?.classList.toggle('open');
});

overlay2?.addEventListener('click', () => {
  sidebar.classList.remove('open');
  overlay2.classList.remove('open');
});

// ── File input: show filename ────────────────────────────────
document.querySelectorAll('input[type="file"]').forEach(input => {
  input.addEventListener('change', () => {
    const label = input.closest('.db-file-wrap')?.querySelector('.db-file-name');
    if (label && input.files[0]) {
      label.textContent = input.files[0].name;
    }
  });
});
