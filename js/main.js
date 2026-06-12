/* Summit Social – shared scripts */

document.addEventListener('DOMContentLoaded', () => {
  const header = document.querySelector('.site-header');
  const nav = document.querySelector('.main-nav');
  const navLinks = nav ? nav.querySelectorAll('a[href^="#"]') : [];
  const sections = document.querySelectorAll('.page-section[id]');

  // Mobile nav toggle
  const toggle = document.querySelector('.nav-toggle');
  if (toggle && nav) {
    toggle.addEventListener('click', () => nav.classList.toggle('open'));
    nav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => nav.classList.remove('open'));
    });
  }

  // Smooth scroll for in-page anchor links
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', e => {
      const hash = link.getAttribute('href');
      if (!hash || hash === '#') return;

      const target = document.querySelector(hash);
      if (!target) return;

      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth' });
      history.pushState(null, '', hash);
      setActiveNav(hash);
    });
  });

  function setActiveNav(hash) {
    navLinks.forEach(link => {
      link.classList.toggle('active', link.getAttribute('href') === hash);
    });
  }

  // Highlight nav item based on scroll position
  if (sections.length && navLinks.length) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          setActiveNav(`#${entry.target.id}`);
        }
      });
    }, {
      rootMargin: `-${header ? header.offsetHeight + 20 : 90}px 0px -55% 0px`,
      threshold: 0
    });

    sections.forEach(section => observer.observe(section));
  }

  // Solid header background after scrolling past hero
  if (header) {
    const onScroll = () => {
      header.classList.toggle('scrolled', window.scrollY > 40);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // Scroll to hash on initial load
  if (window.location.hash) {
    const target = document.querySelector(window.location.hash);
    if (target) {
      requestAnimationFrame(() => {
        target.scrollIntoView({ behavior: 'smooth' });
        setActiveNav(window.location.hash);
      });
    }
  }

  // Form submissions (prevent default, show feedback)
  document.querySelectorAll('form[data-form]').forEach(form => {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const btn = form.querySelector('[type="submit"]');
      const original = btn.textContent;
      btn.textContent = 'Submitted!';
      btn.disabled = true;
      setTimeout(() => {
        btn.textContent = original;
        btn.disabled = false;
        form.reset();
      }, 2500);
    });
  });
});
