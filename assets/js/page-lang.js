// Sets the document language on <html> and <body>.
// Moved out of _includes/head_custom.html so script-src can drop 'unsafe-inline'.
// PAGE_LANG comes from the #page-config JSON block that
// _includes/head_custom.html emits; JSON is data, not script.
(function () {
  var cfgEl = document.getElementById('page-config');
  var PAGE_LANG = (cfgEl ? JSON.parse(cfgEl.textContent).lang : null) || 'en';

  // Set on html element immediately (this works in head)
  document.documentElement.lang = PAGE_LANG;

  // Set on body when it exists
  (function() {
    function setBodyLang() {
      if (document.body) {
        document.body.setAttribute('data-lang', PAGE_LANG);
      } else {
        setTimeout(setBodyLang, 10);
      }
    }
    setBodyLang();
  })();
})();
