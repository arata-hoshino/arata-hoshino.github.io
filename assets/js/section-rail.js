/* ------------------------------------------------------------------
   The section rail: a list of the sections inside one essay, parked in
   the left margin, after the contents rail on the OpenAI article pages.
   Click an entry to jump to that section; the one you are reading is
   marked as you scroll.

   Built from the DOM rather than from Liquid, so it stays correct for
   whatever headings an essay happens to have. Kramdown gives every
   heading an id (auto_ids), which is what the links point at.
   ------------------------------------------------------------------ */

(function () {
  'use strict';

  var prose = document.querySelector('.prose');
  if (!prose) return;

  var headings = prose.querySelectorAll('h2[id], h3[id]');
  if (headings.length < 2) return;

  var rail = document.createElement('nav');
  rail.className = 'rail';
  rail.setAttribute('aria-label', 'Sections in this essay');

  var label = document.createElement('p');
  label.className = 'rail-label';
  label.textContent = 'On this page';
  rail.appendChild(label);

  var list = document.createElement('ul');
  list.className = 'rail-list';

  var links = {};

  Array.prototype.forEach.call(headings, function (heading) {
    var item = document.createElement('li');
    item.className = 'rail-item' + (heading.tagName === 'H3' ? ' is-sub' : '');

    var link = document.createElement('a');
    link.className = 'rail-link';
    link.href = '#' + heading.id;
    link.textContent = heading.textContent;

    item.appendChild(link);
    list.appendChild(item);
    links[heading.id] = link;
  });

  rail.appendChild(list);
  document.body.appendChild(rail);

  /* Mark the section currently under the top of the window. Watching a
     band across the upper third keeps the mark from flickering between
     two headings that share a screen. */
  if (!('IntersectionObserver' in window)) return;

  var visible = [];

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      var id = entry.target.id;
      var at = visible.indexOf(id);
      if (entry.isIntersecting && at === -1) visible.push(id);
      if (!entry.isIntersecting && at !== -1) visible.splice(at, 1);
    });

    if (!visible.length) return;

    var order = Array.prototype.map.call(headings, function (h) { return h.id; });
    var current = visible.slice().sort(function (a, b) {
      return order.indexOf(a) - order.indexOf(b);
    })[0];

    Object.keys(links).forEach(function (id) {
      var isCurrent = id === current;
      links[id].classList.toggle('is-current', isCurrent);
      if (isCurrent) {
        links[id].setAttribute('aria-current', 'true');
      } else {
        links[id].removeAttribute('aria-current');
      }
    });
  }, { rootMargin: '0px 0px -70% 0px' });

  Array.prototype.forEach.call(headings, function (heading) {
    observer.observe(heading);
  });
})();
