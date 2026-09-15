/* ------------------------------------------------------------------
   The notes, shown in the right margin one at a time.

   On a page wide enough to carry a margin on both sides, touching a
   note's mark sets that note in the right margin, opposite the line
   that called it, at the width and the size of the rail on the left.
   One note at a time, so no note is ever pushed away from its mark.

   The apparatus at the foot of the chapter is the record, and is left
   alone: this copy is decorative, and hidden from assistive software.
   Narrower screens, print and the keyboard's own jump are unaffected.
   ------------------------------------------------------------------ */

(function () {
  'use strict';

  var page = document.querySelector('article.page');
  if (!page) return;

  var marks = page.querySelectorAll('.prose sup.noteref a[href^="#note-"]');
  if (!marks.length) return;

  var wide = window.matchMedia('(min-width: 88rem)');
  var panel = null;
  var shown = null;
  var timer = null;

  function make() {
    if (panel) return;
    panel = document.createElement('aside');
    panel.className = 'sidenote';
    panel.setAttribute('aria-hidden', 'true');
    panel.addEventListener('mouseenter', hold);
    panel.addEventListener('mouseleave', leave);
    page.appendChild(panel);
  }

  function show(mark) {
    if (!wide.matches) return;
    make();
    clearTimeout(timer);

    var note = document.getElementById(mark.getAttribute('href').slice(1));
    if (!note) return;
    var item = note.querySelector('li') || note;

    if (shown !== mark) {
      panel.innerHTML = '<span class="sidenote-number">' + mark.textContent + '</span> ' +
                        item.innerHTML;
      if (shown) shown.parentNode.classList.remove('is-open');
      shown = mark;
      mark.parentNode.classList.add('is-open');
    }

    // opposite the mark, and lifted if it would fall off the bottom. Both
    // rectangles are read in the one frame, so a scroll in flight cannot
    // put the note and its mark on different pages of the same page.
    var here = page.getBoundingClientRect();
    var there = mark.getBoundingClientRect();
    var at = there.top - here.top;
    panel.style.top = at + 'px';
    panel.classList.add('is-open');

    var over = there.top + panel.offsetHeight - window.innerHeight + 24;
    if (over > 0) panel.style.top = (at - over) + 'px';
  }

  function hide() {
    if (!panel) return;
    panel.classList.remove('is-open');
    if (shown) shown.parentNode.classList.remove('is-open');
    shown = null;
  }

  function hold() { clearTimeout(timer); }
  function leave() { clearTimeout(timer); timer = setTimeout(hide, 160); }

  Array.prototype.forEach.call(marks, function (mark) {
    mark.addEventListener('mouseenter', function () { show(mark); });
    mark.addEventListener('mouseleave', leave);
    mark.addEventListener('focus', function () { show(mark); });
    mark.addEventListener('blur', leave);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') hide();
  });

  wide.addEventListener('change', function () { if (!wide.matches) hide(); });
  window.addEventListener('resize', hide);
}());
