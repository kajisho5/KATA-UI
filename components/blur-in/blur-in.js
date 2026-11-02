// KATA Blur In — splits the words, staggers the sharpening.
document.querySelectorAll('[data-blur]').forEach(function (el) {
  var words = el.textContent.trim().split(/\s+/);
  el.textContent = '';
  words.forEach(function (word, i) {
    var s = document.createElement('span');
    s.className = 'w';
    s.textContent = word;
    s.style.animationDelay = (i * 90) + 'ms';
    el.appendChild(s);
    el.appendChild(document.createTextNode(' '));
  });
});
