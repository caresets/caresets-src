/* The "?" beside the Element Structure heading opens and closes the
   "How to read this table" panel (see _includes/model-legend.html).
   A file, not an inline script: the site's Content Security Policy is
   script-src 'self', which blocks inline scripts. */
(function () {
  var toggle = document.getElementById('legendToggle');
  var box = document.getElementById('modelLegend');
  var close = document.getElementById('legendClose');
  if (!toggle || !box) { return; }
  function set(open) {
    box.hidden = !open;
    toggle.setAttribute('aria-expanded', String(open));
  }
  toggle.addEventListener('click', function () { set(box.hidden); });
  if (close) { close.addEventListener('click', function () { set(false); }); }
})();
