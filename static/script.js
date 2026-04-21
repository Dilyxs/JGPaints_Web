// ── SMOOTH SCROLL ──
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const targetId = this.getAttribute('href');
    const targetElement = document.querySelector(targetId);
    if (targetElement) {
      e.preventDefault();
      targetElement.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// ── NAV SHRINK ON SCROLL ──
const nav = document.querySelector('nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 60);
});

// ── SCROLL REVEAL ──
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const delay = entry.target.dataset.delay || 0;
      setTimeout(() => entry.target.classList.add('visible'), parseInt(delay));
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.reveal, .reveal-left, .reveal-right').forEach((el, i) => {
  const parent = el.parentElement;
  if (parent && (parent.classList.contains('services-grid') || parent.classList.contains('why-grid'))) {
    const idx = Array.from(parent.children).indexOf(el);
    el.dataset.delay = idx * 120;
  }
  revealObserver.observe(el);
});

// ── FORM SUBMISSION ──
const quoteForm = document.getElementById('quoteForm');
if (quoteForm) {
  quoteForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    const btn = this.querySelector('button');
    const originalText = btn.innerText;
    btn.innerText = "Sending... / Envoi...";
    btn.disabled = true;

    try {
      const response = await fetch('/submit-quote', {
        method: 'POST',
        body: new FormData(this)
      });
      if (response.ok) {
        quoteForm.style.display = 'none';
        document.getElementById('success').style.display = 'block';
        if (typeof gtag !== 'undefined') {
          gtag('event', 'generate_lead', { event_category: 'form', event_label: 'quote_request' });
        }
      } else {
        throw new Error('Server error');
      }
    } catch (err) {
      alert("Error / Erreur: Please call us at 438-864-9123!");
      btn.innerText = originalText;
      btn.disabled = false;
    }
  });
}

// ── GALLERY IMAGE FADE IN ──
document.querySelectorAll('.gallery-item img').forEach(img => {
  img.style.opacity = '0';
  img.style.transition = 'opacity 0.5s ease';
  const show = () => img.style.opacity = '1';
  img.complete ? show() : img.addEventListener('load', show);
});
