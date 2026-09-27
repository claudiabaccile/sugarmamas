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
