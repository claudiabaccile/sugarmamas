const menuButton = document.querySelector('.menu-button');
const nav = document.querySelector('#site-nav');
const cartCount = document.querySelector('.cart-link span');
let itemsInBag = 0;

menuButton?.addEventListener('click', () => {
  const isOpen = nav.classList.toggle('open');
  menuButton.setAttribute('aria-expanded', String(isOpen));
});

document.querySelectorAll('.quick-add').forEach((button) => {
  button.addEventListener('click', () => {
    itemsInBag += 1;
    cartCount.textContent = itemsInBag;
    button.innerHTML = 'Added to bag <span>✓</span>';
    setTimeout(() => { button.innerHTML = 'Quick add <span>+</span>'; }, 1400);
  });
});

document.querySelector('.quote form')?.addEventListener('submit', (event) => {
  event.preventDefault();
  event.currentTarget.querySelector('.form-message').textContent = 'Thank you! This prototype would now send your request to the bakery.';
});

// CTAs do cardápio: já deixa o produto escolhido no formulário de pedido
document.querySelectorAll('.menu-cta[data-order]').forEach((link) => {
  link.addEventListener('click', () => {
    const select = document.querySelector('.quote select');
    if (select) select.value = link.dataset.order;
  });
});

// Navegação por páginas: mostra uma seção (ou grupo de seções) por vez, guiada pelo #hash
const pageOrder = [
  { id: 'home', label: 'Home', hash: '#top' },
  { id: 'menu', label: 'Menu', hash: '#menu' },
  { id: 'cakes', label: 'Custom cakes', hash: '#cakes' },
  { id: 'gallery', label: 'Gallery', hash: '#gallery' },
  { id: 'about', label: 'About', hash: '#about' },
  { id: 'order', label: 'How to order', hash: '#how-it-works' },
  { id: 'visit', label: 'Visit', hash: '#visit' },
];
const pageSections = document.querySelectorAll('[data-page]');
const pager = document.querySelector('.pager');

function pageFor(hash) {
  const target = hash && hash.length > 1 ? document.getElementById(hash.slice(1)) : null;
  const section = target?.closest('[data-page]');
  return { target, page: section ? section.dataset.page : 'home' };
}

function showPage(hash, { initial = false } = {}) {
  const { target, page } = pageFor(hash);
  pageSections.forEach((section) => {
    const active = section.dataset.page === page;
    section.hidden = !active;
    if (active && !initial) {
      section.classList.remove('page-enter');
      void section.offsetWidth;
      section.classList.add('page-enter');
    }
  });

  const current = pageOrder.find((p) => p.id === page);
  document.querySelectorAll('#site-nav a').forEach((link) => {
    const linkPage = pageFor(link.getAttribute('href')).page;
    link.classList.toggle('is-active', linkPage === page);
    if (linkPage === page) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
  });

  const index = pageOrder.findIndex((p) => p.id === page);
  const prev = pageOrder[index - 1];
  const next = pageOrder[index + 1];
  pager.innerHTML = `${prev ? `<a class="pager-prev" href="${prev.hash}"><span>←</span> ${prev.label}</a>` : '<span></span>'}${next ? `<a class="pager-next" href="${next.hash}">Next: ${next.label} <span>→</span></a>` : `<a class="pager-next" href="#top">Back to home <span>↑</span></a>`}`;

  document.title = page === 'home'
    ? 'Sugar Mamas Cakes & Bakery — La Habra, CA'
    : `${current.label} — Sugar Mamas Cakes & Bakery`;

  // Abre no topo da página; só desce direto quando o link aponta para um trecho dentro dela
  const firstOfPage = document.querySelector(`[data-page="${page}"]`);
  const deepLink = target && target !== firstOfPage && firstOfPage.contains(target) === false && target.id !== 'top';
  document.documentElement.style.scrollBehavior = 'auto';
  if (deepLink) target.scrollIntoView();
  else window.scrollTo(0, 0);
  document.documentElement.style.scrollBehavior = '';
}

window.addEventListener('hashchange', () => showPage(location.hash));
showPage(location.hash, { initial: true });

// No celular, fecha o menu depois de escolher uma página
nav?.addEventListener('click', (event) => {
  if (event.target.closest('a') && nav.classList.contains('open')) {
    nav.classList.remove('open');
    menuButton?.setAttribute('aria-expanded', 'false');
  }
});
