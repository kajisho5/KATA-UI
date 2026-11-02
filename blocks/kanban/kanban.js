// KATA Kanban (Block) — HTML5 drag between columns; counts recount.
document.querySelectorAll('[data-kan]').forEach(function (board) {
  var dragged = null;
  function recount() {
    board.querySelectorAll('.k-kan-col').forEach(function (col) {
      col.querySelector('[data-kan-cnt]').textContent = col.querySelectorAll('.k-kan-card').length;
    });
  }
  board.querySelectorAll('.k-kan-card').forEach(function (card) {
    card.addEventListener('dragstart', function () { dragged = card; card.classList.add('drag'); });
    card.addEventListener('dragend', function () {
      card.classList.remove('drag');
      board.querySelectorAll('.k-kan-col').forEach(function (c) { c.classList.remove('over'); });
      recount();
    });
  });
  board.querySelectorAll('.k-kan-col').forEach(function (col) {
    col.addEventListener('dragover', function (e) { e.preventDefault(); col.classList.add('over'); });
    col.addEventListener('dragleave', function () { col.classList.remove('over'); });
    col.addEventListener('drop', function (e) {
      e.preventDefault();
      if (dragged) col.querySelector('.k-kan-list').appendChild(dragged);
      col.classList.remove('over');
      recount();
    });
  });
  recount();
});
