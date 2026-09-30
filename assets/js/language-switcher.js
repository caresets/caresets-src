// Moved out of language-switcher.html so the site can drop 'unsafe-inline' from
// script-src. Page values arrive as JSON in #page-config, which is data,
// not script, and so is not subject to that directive.
(function() {
  const dropdown = document.getElementById('languageDropdown');
  if (!dropdown) return;
  
  const button = dropdown.querySelector('.language-current');

  // The option links are built at site-build time from the page path alone,
  // so they lose whatever the page holds in its query string - on the model
  // viewer that is the selected model (?model=...). Carry the query string
  // and hash over, at the moment of the click, so a language switch shows the
  // same model in the other language.
  dropdown.querySelectorAll('a.language-option').forEach(function(link) {
    link.addEventListener('click', function() {
      const target = new URL(link.getAttribute('href'), window.location.href);
      target.search = window.location.search;
      target.hash = window.location.hash;
      link.href = target.href;
    });
  });
  
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
