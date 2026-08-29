// Publishes the page's Jekyll values as window.SITE_CONFIG.
//
// These used to be written as an inline <script> in four different places.
// They now arrive in the #page-config JSON block, which is data rather than
// script, so script-src no longer needs 'unsafe-inline'. Loaded before the
// scripts that read it; deferred scripts run in document order.
(function () {
  var el = document.getElementById('page-config');
  var cfg = {};
  try {
    cfg = el ? JSON.parse(el.textContent) : {};
  } catch (e) {
    console.error('page-config is not valid JSON:', e);
  }
  window.SITE_CONFIG = {
    baseUrl: cfg.baseUrl || '',
    lang: cfg.lang || 'en',
    exports: cfg.exports || { excel: false, pdf: false, csv: true },
    modelFiles: cfg.modelFiles || []
  };
})();
