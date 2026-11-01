const drawer = document.querySelector('[data-drawer]');
document.querySelector('[data-drawer-open]').addEventListener('click', () => drawer.showModal());
drawer.querySelectorAll('[data-drawer-close]').forEach(b => b.addEventListener('click', () => drawer.close()));
