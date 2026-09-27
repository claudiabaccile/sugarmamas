// Mobile menu + Shop dropdown
const burger = document.querySelector('.burger');
const nav = document.querySelector('#nav');
const dropdown = document.querySelector('.dropdown');
const dropBtn = document.querySelector('.drop-btn');

burger.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  burger.setAttribute('aria-expanded', String(open));
});

dropBtn.addEventListener('click', () => {
  const open = dropdown.classList.toggle('open');
  dropBtn.setAttribute('aria-expanded', String(open));
});

document.addEventListener('click', (e) => {
  if (!dropdown.contains(e.target)) dropdown.classList.remove('open');
});

nav.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => {
  nav.classList.remove('open');
  dropdown.classList.remove('open');
  burger.setAttribute('aria-expanded', 'false');
}));

// Product filter (tabs, category tiles and dropdown links all use data-filter)
const products = document.querySelectorAll('.product');
const tabs = document.querySelectorAll('.tab');

function filterProducts(cat) {
  tabs.forEach((t) => t.classList.toggle('active', t.dataset.filter === cat));
  products.forEach((p) => { p.hidden = cat !== 'all' && p.dataset.cat !== cat; });
}

document.querySelectorAll('[data-filter]').forEach((el) => {
  el.addEventListener('click', () => filterProducts(el.dataset.filter));
});

// Order bag (demo)
const bag = document.querySelector('.bag');
const bagCount = document.querySelector('.bag-count');
const toast = document.querySelector('.toast');
let count = 0;
let toastTimer;

function showToast(msg) {
  toast.textContent = msg;
  toast.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { toast.hidden = true; }, 2200);
}

document.querySelectorAll('.add').forEach((btn) => {
  btn.addEventListener('click', () => {
    count += 1;
    bagCount.textContent = count;
    bag.classList.remove('bump');
    void bag.offsetWidth;
    bag.classList.add('bump');
    btn.textContent = 'Added ✓';
    btn.classList.add('added');
    setTimeout(() => { btn.textContent = 'Add to order'; btn.classList.remove('added'); }, 1500);
    showToast(`${btn.dataset.name} added to your order`);
  });
});

bag.addEventListener('click', () => {
  showToast(count ? `${count} item${count > 1 ? 's' : ''} in your order · checkout coming soon` : 'Your order is empty');
});

// Custom quote form (demo, nothing is sent)
const form = document.querySelector('.quote-form');
const dateInput = document.querySelector('#q-date');
const minDate = new Date(Date.now() + 14 * 864e5);
dateInput.min = minDate.toISOString().slice(0, 10);

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const note = form.querySelector('.form-note');
  let ok = true;
  form.querySelectorAll('[required]').forEach((f) => {
    const bad = !f.value || (f.type === 'email' && !f.checkValidity());
    f.classList.toggle('invalid', bad);
    if (bad) ok = false;
  });
  if (!ok) { note.textContent = 'Please fill in your name, a valid email and the event date.'; return; }
  if (new Date(dateInput.value) < new Date(dateInput.min)) {
    dateInput.classList.add('invalid');
    note.textContent = 'We need at least 14 days of lead time. Please pick a later date.';
    return;
  }
  note.textContent = `Thanks, ${document.querySelector('#q-name').value.split(' ')[0]}! This draft doesn't send yet, but the bakery would reply with a quote.`;
  form.reset();
});

// Newsletter (demo)
document.querySelector('.news').addEventListener('submit', (e) => {
  e.preventDefault();
  e.currentTarget.reset();
  document.querySelector('.news-note').textContent = "You're on the list!";
});

// Highlight today's hours
const rows = document.querySelectorAll('.hours tr');
const day = (new Date().getDay() + 6) % 7; // Monday = 0
rows[day]?.classList.add('today');

document.querySelector('.year').textContent = new Date().getFullYear();
