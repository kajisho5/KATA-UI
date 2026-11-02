// KATA Cascader — the tree is nested lists in the markup; the script
// deals the current path into columns. A leaf pick writes the path.
document.querySelectorAll('[data-casc]').forEach(function (el) {
  var btn = el.querySelector('[data-casc-btn]');
  var label = el.querySelector('[data-casc-label]');
  var panel = el.querySelector('[data-casc-panel]');
  var src = el.querySelector('[data-casc-src]');
  function toData(ul) {
    return Array.prototype.map.call(ul.children, function (li) {
      var a = li.querySelector(':scope > span');
      var sub = li.querySelector(':scope > ul');
      return { label: a.textContent, children: sub ? toData(sub) : null };
    });
  }
  var tree = toData(src.querySelector('ul'));
  var path = [];
  function render() {
    panel.innerHTML = '';
    var level = tree;
    for (var d = 0; ; d++) {
      var col = document.createElement('div');
      col.className = 'k-casc-col';
      (function (nodes, depth) {
        nodes.forEach(function (n) {
          var b = document.createElement('button');
          b.type = 'button';
          b.className = 'k-casc-it' + (path[depth] === n ? ' on' : '');
          b.textContent = n.label;
          if (n.children) b.innerHTML += '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="square" stroke-linejoin="bevel" aria-hidden="true"><path d="m9 6 6 6-6 6"/></svg>';
          b.addEventListener('click', function () {
            path = path.slice(0, depth); path.push(n);
            if (n.children) { render(); }
            else {
              label.textContent = path.map(function (x) { return x.label; }).join(' / ');
              el.setAttribute('data-value', JSON.stringify(path.map(function (x) { return x.label; })));
              el.dispatchEvent(new CustomEvent('kata:cascader', { detail: path.map(function (x) { return x.label; }), bubbles: true }));
              close();
            }
          });
          col.appendChild(b);
        });
      })(level, d);
      panel.appendChild(col);
      if (path[d] && path[d].children) { level = path[d].children; } else { break; }
    }
  }
  function open() { render(); panel.classList.add('open'); btn.setAttribute('aria-expanded', 'true'); }
  function close() { panel.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
  btn.addEventListener('click', function () { panel.classList.contains('open') ? close() : open(); });
  document.addEventListener('click', function (e) { if (!el.contains(e.target)) close(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
});
