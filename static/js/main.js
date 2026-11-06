// Give the navbar a solid background once the user scrolls down
const nav = document.querySelector(".site-nav");

if (nav) {
  const updateNav = () => nav.classList.toggle("scrolled", window.scrollY > 10);
  updateNav();
  window.addEventListener("scroll", updateNav, { passive: true });
}
// Fade elements in when they scroll into view
const revealElements = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target); // animate only once
        }
      });
    },
    { threshold: 0.15 },
  );
  revealElements.forEach((el) => observer.observe(el));
} else {
  // Very old browsers: just show everything
  revealElements.forEach((el) => el.classList.add("visible"));
}
