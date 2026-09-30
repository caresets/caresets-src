/* The UML tab of the model viewer: the selected model as a class diagram.
 *
 * model-viewer.js owns the model list and the loading; when a model is in,
 * it dispatches  caresets:model-loaded  on document with {sd, file}. This
 * script listens, and draws when the UML tab is (or becomes) visible:
 *   - one class for the model, one for each group (BackboneElement with
 *     children), attributes as  +name : Type [min..max]
 *   - composition from the whole to each group, 1 on the whole end and the
 *     group's cardinality on the part end
 *   - an association to a <reference> class for each Reference(X) element,
 *     labelled with the attribute and its cardinality
 *   - generalisation to the parent model; when the parent is one of ours it
 *     is a full class with only its own elements, and the child keeps only
 *     what it adds or constrains
 *   - optionally the bound ValueSet as a note beside the class
 * and renders with nomnoml.renderSvg (vendored, with graphre).
 *
 * It also runs the Tree / UML tabs, keeping the active one in the URL hash
 * (#uml) so a reload or a language switch lands on the same view.
 */
(function () {
  'use strict';
  var NOISE = { id: 1, extension: 1, modifierExtension: 1 };
  var TRIVIAL = { Base: 1, Element: 1, BackboneElement: 1, Resource: 1, DomainResource: 1 };
  var baseUrl = (window.SITE_CONFIG && window.SITE_CONFIG.baseUrl) || '';
  var lang = (window.SITE_CONFIG && window.SITE_CONFIG.lang) || 'en';

  var sd = null;         // the model shown
  var parentSd = null;   // the model sd specialises, when it is one of ours
  var source = '';
  var dirty = false;     // a model arrived while the tab was hidden
  var index = null;      // promise: {byUrl, byName} over the served models

  // ---------------------------------------------------------------- helpers
  function lastSeg(url) { return (url || '').split('|')[0].replace(/\/$/, '').split('/').pop(); }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function typeName(t) {
    var code = t.code || '';
    if (code.indexOf('http://hl7.org/fhirpath/System.') === 0) {
      var ext = (t.extension || []).filter(function (e) { return e.url === 'http://hl7.org/fhir/StructureDefinition/structuredefinition-fhir-type'; })[0];
      if (ext && ext.valueUrl) return ext.valueUrl;
      var s = code.split('.').pop();
      return s.charAt(0).toLowerCase() + s.slice(1);
    }
    if (code.indexOf('/') >= 0) code = lastSeg(code);
    return code;
  }
  function card(el) { return (el.min == null ? 0 : el.min) + '..' + (el.max == null ? '1' : el.max); }
  // nomnoml treats | ; [ ] as syntax inside a class; keep labels free of them
  function safe(s) { return String(s).replace(/[|\[\];]/g, ' ').replace(/\s+/g, ' ').trim(); }
  function relOf(e) { return e.path.split('.').slice(1).join('.'); }

  // ---------------------------------------------------------------- model -> classes
  function buildModel(sd, parent) {
    var root = { key: sd.name, name: sd.name, attrs: [], children: [], refs: [], bindings: [] };
    var byRel = { '': root };
    var elements = ((sd.snapshot || sd.differential || {}).element || []).filter(function (e) {
      return e.path && e.path.indexOf('.') > 0 && !NOISE[e.path.split('.').pop()];
    });
    // With a parent drawn as its own class, the child keeps only what it adds
    // or constrains: elements not in the parent's snapshot, plus inherited ones
    // the differential restates (those are constrained here, and drawn again).
    if (parent) {
      var inherited = {};
      ((parent.snapshot || {}).element || []).forEach(function (e) { if (e.path.indexOf('.') > 0) inherited[relOf(e)] = true; });
      var restated = {};
      ((sd.differential || {}).element || []).forEach(function (e) { if (e.path.indexOf('.') > 0) restated[relOf(e)] = true; });
      elements = elements.filter(function (e) { var r = relOf(e); return !inherited[r] || restated[r]; });
    }
    var hasChild = {};
    elements.forEach(function (e) { var p = relOf(e).split('.'); if (p.length > 1) hasChild[p.slice(0, -1).join('.')] = true; });

    elements.forEach(function (e) {
      var rel = relOf(e);
      var parts = rel.split('.');
      var name = parts[parts.length - 1].replace(/\[x\]$/, '') + (e.sliceName ? ':' + e.sliceName : '');
      var parentNode = byRel[parts.slice(0, -1).join('.')];
      if (!parentNode) return;
      var types = (e.type || []).map(typeName).filter(function (v, i, a) { return v && a.indexOf(v) === i; });
      var refTargets = [];
      (e.type || []).forEach(function (t) {
        if ((t.code || '') === 'Reference') (t.targetProfile || []).forEach(function (p) { refTargets.push(lastSeg(p)); });
      });
      if (hasChild[rel]) {
        var group = { key: sd.name + '.' + rel, name: name, card: card(e), attrs: [], children: [], refs: [], bindings: [] };
        parentNode.children.push(group);
        byRel[rel] = group;
        return;
      }
      var typeLabel = types.length ? types.join(' or ') : (e.contentReference ? 'see ' + lastSeg(e.contentReference.split('#').pop()) : '');
      if (refTargets.length) {
        typeLabel = 'Reference';
        refTargets.forEach(function (target) { parentNode.refs.push({ attr: name, target: target, card: card(e) }); });
      }
      parentNode.attrs.push({ name: name, type: typeLabel, card: card(e) });
      var vs = (e.binding || {}).valueSet;
      if (vs) parentNode.bindings.push({ attr: name, valueSet: lastSeg(vs), strength: e.binding.strength || '' });
    });
    return root;
  }

  // ---------------------------------------------------------------- classes -> nomnoml
  function classBox(node) {
    var attrs = node.attrs.map(function (a) { return '+' + safe(a.name) + ' : ' + safe(a.type) + ' \\[' + a.card + '\\]'; });
    return '[' + safe(node.name) + (attrs.length ? '|' + attrs.join(';') : '') + ']';
  }
  function ref(node) { return '[' + safe(node.name) + ']'; }

  function toNomnoml(root, opts) {
    var lines = [
      '#direction: ' + (opts.direction || 'right'),
      '#font: Segoe UI, Calibri, Arial, sans-serif',
      '#fontSize: 11',
      '#lineWidth: 1.4',
      '#padding: 8',
      '#spacing: 72',       // distance between boxes, i.e. the length of the connections
      '#gutter: 8',
      '#edges: rounded',
      '#ranker: tight-tree',
      '#fill: #FEFECE; #F3F3F3',
      '#stroke: #33322E',
      '#arrowSize: 0.9',
      '#.reference: fill=#D9D9D9 dashed',
      '#.valueset: fill=#C3D69B visual=note bold',   // first line (attribute · strength) reads as the caption
      ''
    ];
    var seen = {};
    function walk(node) {
      if (seen[node.key]) return;
      seen[node.key] = true;
      lines.push(classBox(node));
      node.children.forEach(function (child) {
        walk(child);
        lines.push(ref(node) + ' 1 +-> ' + child.card + ' ' + ref(child));
      });
      if (opts.references) {
        node.refs.forEach(function (r) {
          lines.push('[<reference> ' + safe(r.target) + ']');
          lines.push(ref(node) + ' ' + safe(r.attr) + ' ' + r.card + ' -> [<reference> ' + safe(r.target) + ']');
        });
      }
      if (opts.bindings) {
        // The attribute and strength go inside the note, not on the edge:
        // edge labels sit at the endpoints and drift away from the line.
        node.bindings.forEach(function (b) {
          var vsBox = '[<valueset> ' + safe(b.attr) + (b.strength ? ' · ' + safe(b.strength) : '') + ';' + safe(b.valueSet) + ']';
          lines.push(vsBox);
          lines.push(ref(node) + ' -- ' + vsBox);
        });
      }
    }
    walk(root);
    if (opts.parent) {
      var parentName = lastSeg(sd.baseDefinition || '');
      if (parentName && !TRIVIAL[parentName]) {
        if (parentSd) {
          var parentRoot = buildModel(parentSd, null);
          walk(parentRoot);
          lines.push(ref(parentRoot) + ' <:- ' + ref(root));
        } else {
          lines.push('[<reference> ' + safe(parentName) + ']');
          lines.push('[<reference> ' + safe(parentName) + '] <:- ' + ref(root));
        }
      }
    }
    return lines.join('\n');
  }

  // ---------------------------------------------------------------- the served models, for parents
  function modelIndex() {
    if (index) return index;
    var files = (window.SITE_CONFIG && window.SITE_CONFIG.modelFiles) || [];
    var byUrl = {}, byName = {};
    index = Promise.all(files.map(function (f) {
      var file = f.replace('StructureDefinition-', '').replace('.json', '');
      return fetch(baseUrl + '/_resources/models/' + f).then(function (r) { return r.ok ? r.json() : null; })
        .then(function (d) {
          if (d && d.url) byUrl[d.url.split('|')[0]] = file;
          if (d && d.name) byName[d.name] = file;
        }).catch(function () {});
    })).then(function () { return { byUrl: byUrl, byName: byName }; });
    return index;
  }

  function resolveParent(model) {
    var base = (model.baseDefinition || '').split('|')[0];
    if (!base || TRIVIAL[lastSeg(base)]) return Promise.resolve(null);
    return modelIndex().then(function (ix) {
      var file = ix.byUrl[base] || ix.byName[lastSeg(base)];
      if (!file) return null;
      return fetch(baseUrl + '/_resources/models/StructureDefinition-' + file + '.json')
        .then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; });
    });
  }

  // ---------------------------------------------------------------- rendering
  function options() {
    return {
      references: document.getElementById('optReferences').checked,
      parent: document.getElementById('optParent').checked,
      bindings: document.getElementById('optBindings').checked,
      direction: document.getElementById('optDirection').value
    };
  }
  function status(msg) { document.getElementById('umlStatus').textContent = msg || ''; }
  function umlVisible() { var p = document.getElementById('panel-uml'); return p && !p.hidden; }

  function render() {
    if (!sd) return;
    var box = document.getElementById('umlDiagram');
    try {
      var opts = options();
      source = toNomnoml(buildModel(sd, opts.parent ? parentSd : null), opts);
      document.getElementById('umlSource').textContent = source;
      box.innerHTML = window.nomnoml.renderSvg(source);
      var svg = box.querySelector('svg');
      if (svg) { svg.setAttribute('role', 'img'); svg.setAttribute('aria-label', 'UML class diagram of ' + sd.name); }
      dirty = false;
      status('');
    } catch (e) {
      box.innerHTML = '<p style="color:#b3261e">Could not draw the diagram: ' + esc(e.message) + '</p>';
      console.error(e);
    }
  }

  function onModelLoaded(ev) {
    sd = ev.detail && ev.detail.sd;
    parentSd = null;
    if (!sd) return;
    dirty = true;
    status('');
    resolveParent(sd).then(function (p) {
      parentSd = p;
      if (umlVisible()) render();
    });
  }

  function downloadSvg() {
    var svg = document.querySelector('#umlDiagram svg');
    if (!svg || !sd) return;
    var text = '<?xml version="1.0" encoding="UTF-8"?>\n' + svg.outerHTML;
    var blob = new Blob([text], { type: 'image/svg+xml;charset=utf-8' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = sd.name + '-uml.svg';
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 0);
  }
  function copySource() {
    if (!navigator.clipboard) { status('Copy not available; use the source box below'); return; }
    navigator.clipboard.writeText(source).then(function () { status('Diagram source copied'); },
                                               function () { status('Copy failed; use the source box below'); });
  }

  // ---------------------------------------------------------------- tabs
  function showView(view, pushHash) {
    document.querySelectorAll('.view-tabs [role="tab"]').forEach(function (tab) {
      var on = tab.dataset.view === view;
      tab.setAttribute('aria-selected', String(on));
      var panel = document.getElementById(tab.getAttribute('aria-controls'));
      if (panel) panel.hidden = !on;
    });
    if (pushHash) {
      var url = window.location.pathname + window.location.search + (view === 'tree' ? '' : '#' + view);
      try { window.history.replaceState({}, '', url); } catch (e) { /* file:// and sandboxed frames refuse; the tab still switches */ }
    }
    if (view === 'uml' && dirty) render();
    // other views (the Concept tab) draw themselves when shown
    document.dispatchEvent(new CustomEvent('caresets:view-shown', { detail: { view: view } }));
  }

  document.addEventListener('DOMContentLoaded', function () {
    if (!document.getElementById('panel-uml')) return;
    document.querySelectorAll('.view-tabs [role="tab"]').forEach(function (tab) {
      tab.addEventListener('click', function () { showView(tab.dataset.view, true); });
    });
    ['optReferences', 'optParent', 'optBindings', 'optDirection'].forEach(function (id) {
      document.getElementById(id).addEventListener('change', render);
    });
    document.getElementById('btnDownloadSvg').addEventListener('click', downloadSvg);
    document.getElementById('btnCopySource').addEventListener('click', copySource);
    document.addEventListener('caresets:model-loaded', onModelLoaded);
    var wanted = window.location.hash.replace('#', '');
    showView(document.querySelector('.view-tabs [data-view="' + wanted + '"]') ? wanted : 'tree', false);
  });
})();
