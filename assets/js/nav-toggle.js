/* ------------------------------------------------------------------
   The contents sheet, on a narrow screen only.

   Opening and closing are done in CSS; this carries the state, holds the
   page still behind the sheet, keeps the closed list out of reach of the
   keyboard and the screen reader, and puts focus where it belongs.
   ------------------------------------------------------------------ */

(function () {
  'use strict';

  var toggle = document.querySelector('.nav-toggle');
  var close = document.querySelector('.nav-close');
  var shell = document.querySelector('.nav-shell');
  var nav = document.getElementById('site-nav');
  if (!toggle || !shell || !nav) return;

  var wide = window.matchMedia('(min-width: 48rem)');
  var scrollY = 0;

  function setInert(hidden) {
    if ('inert' in HTMLElement.prototype) shell.inert = hidden;
  }

  function open() {
    scrollY = window.scrollY;
    document.body.classList.add('nav-open');
    document.body.style.top = -scrollY + 'px';
    shell.classList.add('is-open');
    toggle.setAttribute('aria-expanded', 'true');
    setInert(false);
    if (close) close.focus();
  }

  function shut(returnFocus) {
    shell.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('nav-open');
    document.body.style.top = '';
    window.scrollTo(0, scrollY);
    setInert(true);
    if (returnFocus) toggle.focus();
  }

  function sync() {
    if (wide.matches) {
      // the list is simply there; nothing is hidden and nothing is fixed
      shell.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('nav-open');
      document.body.style.top = '';
      setInert(false);
    } else if (!shell.classList.contains('is-open')) {
      setInert(true);
    }
  }

  toggle.addEventListener('click', function () {
    if (shell.classList.contains('is-open')) shut(true); else open();
  });

  if (close) close.addEventListener('click', function () { shut(true); });

  nav.addEventListener('click', function (e) {
    if (e.target.closest('a') && !wide.matches) shut(false);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && shell.classList.contains('is-open')) shut(true);
  });

  wide.addEventListener('change', sync);
  sync();
}());
