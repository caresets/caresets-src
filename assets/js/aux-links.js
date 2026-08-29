// Moved out of aux_links_custom.html so the site can drop 'unsafe-inline' from
// script-src. Page values arrive as JSON in #page-config, which is data,
// not script, and so is not subject to that directive.
(function() {
  const dropdown = document.getElementById('languageDropdownAux');
  if (!dropdown) return;
  
  const button = dropdown.querySelector('.language-current');
  
  button.addEventListener('click', function(e) {
    e.stopPropagation();
    dropdown.classList.toggle('open');
    button.setAttribute('aria-expanded', dropdown.classList.contains('open'));
  });
  
  document.addEventListener('click', function(e) {
    if (!dropdown.contains(e.target)) {
      dropdown.classList.remove('open');
      button.setAttribute('aria-expanded', 'false');
    }
  });
  
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && dropdown.classList.contains('open')) {
      dropdown.classList.remove('open');
      button.setAttribute('aria-expanded', 'false');
      button.focus();
    }
  });
})();
