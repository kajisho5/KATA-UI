// KATA Calendar — renders one month of day buttons; the pick is yours.
// Set data-selected="YYYY-MM-DD" to start with a selection. Emits a
// "kata:date" CustomEvent (detail: "YYYY-MM-DD") on the element per pick.
document.querySelectorAll('[data-cal]').forEach(function (el) {
  var title = el.querySelector('[data-cal-title]');
  var grid = el.querySelector('[data-cal-grid]');
  var sel = el.getAttribute('data-selected') || '';
  var now = new Date();
  var view = sel ? new Date(sel + 'T00:00:00') : new Date(now.getFullYear(), now.getMonth(), 1);
  view = new Date(view.getFullYear(), view.getMonth(), 1);
  var NAMES = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  var FULL = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  var MON = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  function iso(d) { return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  function render() {
    title.textContent = NAMES[view.getMonth()] + ' ' + view.getFullYear();
    grid.innerHTML = '';
    var first = new Date(view.getFullYear(), view.getMonth(), 1);
    var start = new Date(first); start.setDate(1 - first.getDay());
    for (var i = 0; i < 42; i++) {
      var d = new Date(start); d.setDate(start.getDate() + i);
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'k-cal-day' + (d.getMonth() !== view.getMonth() ? ' off' : '') + (iso(d) === iso(now) ? ' today' : '') + (iso(d) === sel ? ' sel' : '');
      b.textContent = d.getDate();
      b.setAttribute('aria-label', FULL[d.getDay()] + ', ' + MON[d.getMonth()] + ' ' + d.getDate() + ', ' + d.getFullYear());
      if (iso(d) === iso(now)) b.setAttribute('aria-current', 'date');
      b.setAttribute('data-date', iso(d));
      grid.appendChild(b);
    }
  }
  grid.addEventListener('click', function (e) {
    var b = e.target.closest('.k-cal-day'); if (!b) return;
    sel = b.getAttribute('data-date');
    el.setAttribute('data-selected', sel);
    el.dispatchEvent(new CustomEvent('kata:date', { detail: sel, bubbles: true }));
    render();
  });
  el.querySelector('[data-cal-prev]').addEventListener('click', function () { view = new Date(view.getFullYear(), view.getMonth() - 1, 1); render(); });
  el.querySelector('[data-cal-next]').addEventListener('click', function () { view = new Date(view.getFullYear(), view.getMonth() + 1, 1); render(); });
  render();
});
