/* ------------------------------------------------------------------
   The contents button, on a narrow screen only.

   The opening is done in CSS: the shell is a grid whose single row goes
   from 0fr to 1fr, and the links ride in on their own small delays. All
   this does is carry the state, and keep the closed list out of reach of
   the keyboard and the screen reader.
   ------------------------------------------------------------------ */

(function () {
  'use strict';

  var button = document.querySelector('.nav-toggle');
  var shell = document.querySelector('.nav-shell');
  var nav = document.getElementById('site-nav');
  if (!button || !shell || !nav) return;

  var wide = window.matchMedia('(min-width: 48rem)');

  function apply(open) {
    button.setAttribute('aria-expanded', open ? 'true' : 'false');
    shell.classList.toggle('is-open', open);
    if ('inert' in HTMLElement.prototype) nav.inert = !open && !wide.matches;
  }

  function sync() {
    // on a wide screen the list is simply open, and the button is not shown
    if (wide.matches) {
      shell.classList.remove('is-open');
      button.setAttribute('aria-expanded', 'false');
      if ('inert' in HTMLElement.prototype) nav.inert = false;
    } else {
      apply(false);
    }
  }

  button.addEventListener('click', function () {
    apply(button.getAttribute('aria-expanded') !== 'true');
  });

  // a link inside it closes it, and so does the escape key
  nav.addEventListener('click', function (e) {
    if (e.target.closest('a') && !wide.matches) apply(false);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && shell.classList.contains('is-open')) {
      apply(false);
      button.focus();
    }
  });

  wide.addEventListener('change', sync);
  sync();
}());
