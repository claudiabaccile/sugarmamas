// Mobile menu
const menuToggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('#site-nav');

menuToggle?.addEventListener('click', () => {
  const isOpen = nav.classList.toggle('open');
  menuToggle.setAttribute('aria-expanded', String(isOpen));
});

nav?.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    nav.classList.remove('open');
    menuToggle?.setAttribute('aria-expanded', 'false');
  });
});

// Portfolio filters
const gallery = document.querySelector('.gallery');
const items = document.querySelectorAll('.g-item');
const filters = document.querySelectorAll('.filter');
const emptyMsg = document.querySelector('.empty-msg');

function applyFilter(category) {
  let visible = 0;
  filters.forEach((btn) => btn.classList.toggle('active', btn.dataset.filter === category));
  items.forEach((item) => {
    const match = category === 'all' || item.dataset.cat.split(' ').includes(category);
    item.classList.toggle('hidden', !match);
    if (match) visible += 1;
  });
  gallery.classList.toggle('filtered', category !== 'all');
  emptyMsg.hidden = visible > 0;
}

filters.forEach((btn) => btn.addEventListener('click', () => applyFilter(btn.dataset.filter)));

// Occasion icons jump to the matching portfolio filter
document.querySelectorAll('[data-jump]').forEach((link) => {
  link.addEventListener('click', () => applyFilter(link.dataset.jump));
});

// Testimonials slider
const slides = document.querySelector('.slides');
const cards = document.querySelectorAll('.quote-card');
const dotsWrap = document.querySelector('.dots');
let current = 0;

function perView() {
  if (window.innerWidth <= 560) return 1;
  if (window.innerWidth <= 1024) return 2;
  return 3;
}

function renderSlider() {
  const pages = Math.max(1, cards.length - perView() + 1);
  if (current >= pages) current = 0;
  dotsWrap.innerHTML = Array.from({ length: pages }, (_, i) => `<span class="${i === current ? 'on' : ''}"></span>`).join('');
  const gap = parseFloat(getComputedStyle(slides).gap) || 0;
  slides.style.transform = `translateX(-${current * (cards[0].offsetWidth + gap)}px)`;
}

document.querySelector('.slider-next')?.addEventListener('click', () => {
  current += 1;
  renderSlider();
});

window.addEventListener('resize', renderSlider);
renderSlider();

// Newsletter
document.querySelector('.newsletter')?.addEventListener('submit', (event) => {
  event.preventDefault();
  event.currentTarget.reset();
  document.querySelector('.form-msg').textContent = 'Thank you! You are on our sweet list.';
});

document.querySelector('#year').textContent = new Date().getFullYear();
