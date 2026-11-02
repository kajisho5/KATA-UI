// KATA Transfer — checked items move; counts and filters stay honest.
document.querySelectorAll('[data-xfer]').forEach(function (root) {
  var sides = { l: root.querySelector('[data-xfer-l]'), r: root.querySelector('[data-xfer-r]') };
  function items(side) { return Array.prototype.slice.call(side.querySelectorAll('.k-xfer-it')); }
  function refresh() {
    Object.keys(sides).forEach(function (k) {
      var s = sides[k], list = items(s);
      var checked = list.filter(function (i) { return i.querySelector('input').checked; }).length;
      s.querySelector('[data-xfer-cnt]').textContent = list.length + ' items';
      var all = s.querySelector('[data-xfer-all]');
      all.checked = list.length > 0 && checked === list.length;
      all.indeterminate = checked > 0 && checked < list.length;
    });
    root.querySelector('[data-xfer-tor]').disabled = !items(sides.l).some(function (i) { return i.querySelector('input').checked; });
    root.querySelector('[data-xfer-tol]').disabled = !items(sides.r).some(function (i) { return i.querySelector('input').checked; });
  }
  function move(from, to) {
    items(from).forEach(function (i) {
      var box = i.querySelector('input');
      if (box.checked) { box.checked = false; to.querySelector('.k-xfer-list').appendChild(i); }
    });
    refresh();
  }
  root.querySelector('[data-xfer-tor]').addEventListener('click', function () { move(sides.l, sides.r); });
  root.querySelector('[data-xfer-tol]').addEventListener('click', function () { move(sides.r, sides.l); });
  Object.keys(sides).forEach(function (k) {
    var s = sides[k];
    s.addEventListener('change', refresh);
    s.querySelector('[data-xfer-all]').addEventListener('change', function (e) {
      items(s).forEach(function (i) { if (i.style.display !== 'none') i.querySelector('input').checked = e.target.checked; });
      refresh();
    });
    s.querySelector('[data-xfer-q]').addEventListener('input', function (e) {
      var q = e.target.value.toLowerCase();
      items(s).forEach(function (i) { i.style.display = i.textContent.toLowerCase().indexOf(q) !== -1 ? '' : 'none'; });
    });
  });
  refresh();
});
