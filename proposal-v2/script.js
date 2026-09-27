// Mobile nav toggle
const menuButton = document.querySelector('.menu-button');
const siteNav = document.getElementById('site-nav');
if (menuButton && siteNav) {
  menuButton.addEventListener('click', () => {
    const isOpen = siteNav.classList.toggle('open');
    menuButton.setAttribute('aria-expanded', String(isOpen));
  });
  siteNav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      siteNav.classList.remove('open');
      menuButton.setAttribute('aria-expanded', 'false');
    });
  });
}

// Portfolio filter tabs
const filterTabs = document.querySelectorAll('.filter-tab');
const portfolioItems = document.querySelectorAll('.portfolio-item');
filterTabs.forEach((tab) => {
  tab.addEventListener('click', () => {
    filterTabs.forEach((t) => t.classList.remove('is-active'));
    tab.classList.add('is-active');
    const filter = tab.dataset.filter;
    portfolioItems.forEach((item) => {
      const show = filter === 'all' || item.dataset.category === filter;
      item.classList.toggle('is-hidden', !show);
    });
  });
});

// Occasion icons: jump to the portfolio pre-filtered to that category
const occasionLinks = document.querySelectorAll('.occasion[data-filter]');
occasionLinks.forEach((link) => {
  link.addEventListener('click', () => {
    const tab = document.querySelector(`.filter-tab[data-filter="${link.dataset.filter}"]`);
    if (tab) tab.click();
  });
});

// Quote form: prototype-only submit feedback (no data is actually sent)
const quoteForm = document.querySelector('.quote form');
if (quoteForm) {
  quoteForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const message = quoteForm.querySelector('.form-message');
    if (message) message.textContent = "Thanks! This is a design proposal, so nothing was actually sent — connect the form before launch.";
  });
}

// Newsletter form: same prototype-only behavior
const newsletterForm = document.querySelector('.newsletter-form');
if (newsletterForm) {
  newsletterForm.addEventListener('submit', (event) => {
    event.preventDefault();
    newsletterForm.querySelector('input').value = '';
  });
}
