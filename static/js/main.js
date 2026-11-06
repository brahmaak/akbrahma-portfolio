// Give the navbar a solid background once the user scrolls down
const nav = document.querySelector(".site-nav");

if (nav) {
  const updateNav = () => nav.classList.toggle("scrolled", window.scrollY > 10);
  updateNav();
  window.addEventListener("scroll", updateNav, { passive: true });
}
