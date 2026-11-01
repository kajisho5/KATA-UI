// KATA Copy field — click to copy, confirm in place.
document.querySelectorAll('[data-copy-field]').forEach(function (field) {
  var btn = field.querySelector('[data-copy-btn]');
  var val = field.querySelector('code');
  if (!btn || !val) return;
  var timer = null;
  btn.addEventListener('click', function () {
    var text = val.textContent.trim();
    function done() {
      field.dataset.copied = 'true';
      btn.textContent = 'Copied';
      clearTimeout(timer);
      timer = setTimeout(function () {
        field.dataset.copied = 'false';
        btn.textContent = 'Copy';
      }, 1600);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, done);
    } else {
      var ta = document.createElement('textarea');
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); } catch (e) {}
      document.body.removeChild(ta);
      done();
    }
  });
});
