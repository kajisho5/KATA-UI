// KATA Goo Tabs — real tabs; only the indicator is theatrical.
document.querySelectorAll('[data-gootabs]').forEach(function (root) {
  var bar = root.querySelector('.k-goo-bar');
  var ind = root.querySelector('.k-goo-ind');
  var tabs = Array.prototype.slice.call(bar.querySelectorAll('button[role="tab"]'));
  var panels = Array.prototype.slice.call(root.querySelectorAll('[role="tabpanel"]'));
  function place(tab, animate) {
    ind.style.left = tab.offsetLeft + 'px';
    ind.style.width = tab.offsetWidth + 'px';
    if (animate) {
      ind.classList.add('moving');
      ind.style.width = (tab.offsetWidth * 1.18) + 'px';
      setTimeout(function () { ind.style.width = tab.offsetWidth + 'px'; ind.classList.remove('moving'); }, 180);
    }
  }
  function choose(tab, focus) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', on);
      t.tabIndex = on ? 0 : -1;
      var p = panels[tabs.indexOf(t)];
      if (p) p.hidden = !on;
    });
    place(tab, true);
    if (focus) tab.focus();
  }
  tabs.forEach(function (t) { t.addEventListener('click', function () { choose(t, false); }); });
  bar.addEventListener('keydown', function (e) {
    var i = tabs.indexOf(document.activeElement);
    if (i < 0) return;
    if (e.key === 'ArrowRight') { choose(tabs[(i + 1) % tabs.length], true); e.preventDefault(); }
    if (e.key === 'ArrowLeft') { choose(tabs[(i - 1 + tabs.length) % tabs.length], true); e.preventDefault(); }
  });
  var start = tabs.filter(function (t) { return t.getAttribute('aria-selected') === 'true'; })[0] || tabs[0];
  choose(start, false);
  place(start, false);
});
