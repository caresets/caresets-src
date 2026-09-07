// Moved out of language-switcher.html so the site can drop 'unsafe-inline' from
// script-src. Page values arrive as JSON in #page-config, which is data,
// not script, and so is not subject to that directive.
(function() {
  const dropdown = document.getElementById('languageDropdown');
  if (!dropdown) return;
  
  const button = dropdown.querySelector('.language-current');
  
  // Toggle dropdown on click
  button.addEventListener('click', function(e) {
    e.stopPropagation();
    dropdown.classList.toggle('open');
    const isOpen = dropdown.classList.contains('open');
    button.setAttribute('aria-expanded', isOpen);
  });
  
  // Close dropdown when clicking outside
  document.addEventListener('click', function(e) {
    if (!dropdown.contains(e.target)) {
      dropdown.classList.remove('open');
      button.setAttribute('aria-expanded', 'false');
    }
  });
  
  // Close on escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && dropdown.classList.contains('open')) {
      dropdown.classList.remove('open');
      button.setAttribute('aria-expanded', 'false');
      button.focus();
    }
  });
})();
