// Smooth scroll for nav links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    document.querySelector(this.getAttribute('href'))
      .scrollIntoView({ behavior: 'smooth' });
  });
});

// Quote form submission
document.getElementById('quoteForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const formData = new FormData(this);
  
  const response = await fetch('/submit-quote', {
    method: 'POST',
    body: formData
  });
  
  const result = await response.json();
  if (result.status === 'success') {
    document.getElementById('quoteForm').style.display = 'none';
    document.getElementById('success').style.display = 'block';
  }
});