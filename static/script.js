// Safe Smooth Scroll
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

// Robust Form Submission
const quoteForm = document.getElementById('quoteForm');
if (quoteForm) {
  quoteForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    
    // Change the button text to show "sending"
    const btn = this.querySelector('button');
    const originalText = btn.innerText;
    btn.innerText = "Sending... / Envoi...";
    btn.disabled = true;

    try {
      const response = await fetch('/submit-quote', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        quoteForm.style.display = 'none';
        document.getElementById('success').style.display = 'block';
        // Log a custom event to Google Analytics
        gtag('event', 'generate_lead', { 'event_category': 'form', 'event_label': 'quote_request' });
      } else {
        throw new Error('Server Error');
      }
    } catch (err) {
      alert("Error / Erreur: Please call us at 438-864-9123 instead!");
      btn.innerText = originalText;
      btn.disabled = false;
    }
  });
}