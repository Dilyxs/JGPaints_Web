document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener('click', function (e) {
    const targetId = this.getAttribute('href');
    const targetElement = document.querySelector(targetId);
    if (targetElement) {
      e.preventDefault();
      targetElement.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

const nav = document.querySelector('nav');
window.addEventListener('scroll', () => {
  if (nav) {
    nav.classList.toggle('scrolled', window.scrollY > 60);
  }
});

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const delay = Number(entry.target.dataset.delay || 0);
        setTimeout(() => entry.target.classList.add('visible'), delay);
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
);

document.querySelectorAll('.reveal, .reveal-left, .reveal-right').forEach((el) => {
  const parent = el.parentElement;
  if (parent && (parent.classList.contains('services-grid') || parent.classList.contains('process-grid') || parent.classList.contains('pricing-grid'))) {
    const idx = Array.from(parent.children).indexOf(el);
    el.dataset.delay = String(idx * 90);
  }
  revealObserver.observe(el);
});

const quoteForm = document.getElementById('quoteForm');
const formLoadedAt = document.getElementById('formLoadedAt');
if (formLoadedAt) {
  formLoadedAt.value = String(Date.now());
}

if (quoteForm) {
  quoteForm.addEventListener('submit', async function (e) {
    e.preventDefault();
    const btn = this.querySelector('button[type="submit"]');
    if (!btn) return;

    const formData = new FormData(this);
    const honeypotValue = (formData.get('company') || '').toString().trim();
    const loadedAtValue = Number(formData.get('form_loaded_at') || 0);
    const timeOnPage = Date.now() - loadedAtValue;

    if (honeypotValue || Number.isNaN(loadedAtValue) || timeOnPage < 3000) {
      return;
    }

    const originalText = btn.innerText;
    btn.innerText = btn.dataset.sending || 'Sending request...';
    btn.disabled = true;

    try {
      const response = await fetch('/submit-quote', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('Server error');
      }

      quoteForm.style.display = 'none';
      const success = document.getElementById('success');
      if (success) {
        success.style.display = 'block';
      }
      if (typeof gtag !== 'undefined') {
        gtag('event', 'generate_lead', {
          event_category: 'form',
          event_label: 'quote_request_qualified'
        });
      }
    } catch (err) {
      alert('Error: Please call us at 438-864-9123.');
      btn.innerText = originalText;
      btn.disabled = false;
    }
  });
}

document.querySelectorAll('.pair-shot img').forEach((img) => {
  img.style.opacity = '0';
  img.style.transition = 'opacity 0.4s ease';
  const show = () => {
    img.style.opacity = '1';
  };
  if (img.complete) {
    show();
  } else {
    img.addEventListener('load', show);
  }
});
