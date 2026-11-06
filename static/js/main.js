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
// Project filter buttons (only runs on the Projects page)
const filterButtons = document.querySelectorAll("[data-filter]");
const projectItems = document.querySelectorAll("[data-tech]");
const noProjectsMessage = document.querySelector("#no-projects");
const projectCount = document.querySelector("#project-count");

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const filter = button.dataset.filter;

    // Highlight the clicked button only
    filterButtons.forEach((btn) => {
      const isActive = btn === button;
      btn.classList.toggle("active", isActive);
      btn.setAttribute("aria-pressed", isActive);
    });

    // Show matching projects, hide the rest
    let shown = 0;
    projectItems.forEach((item) => {
      const techs = item.dataset.tech.split("|");
      const matches = filter === "all" || techs.includes(filter);
      item.classList.toggle("d-none", !matches);
      if (matches) {
        item.classList.add("visible"); // make sure the fade-in has run
        shown++;
      }
    });

    if (noProjectsMessage)
      noProjectsMessage.classList.toggle("d-none", shown > 0);
    if (projectCount)
      projectCount.textContent = `${shown} project${shown === 1 ? "" : "s"}`;
  });
});
