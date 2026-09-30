/* UML view of a logical model, drawn as a class diagram in the browser.
 *
 * From a StructureDefinition (kind = logical) it builds nomnoml source:
 *   - one class for the model, one for each group (BackboneElement with
 *     children), attributes as  +name : Type [min..max]
 *   - composition from the whole to each group, labelled with the group's
 *     cardinality on the part end and 1 on the whole end
 *   - an association to a <reference> class for each Reference(X) element,
 *     labelled with the element's cardinality
 *   - generalisation to the parent model when baseDefinition is a model
 *   - optionally, the bound ValueSet as a note-like class beside the attribute
 * and renders it with nomnoml.renderSvg (vendored, with graphre).
 *
 * The inherited id / extension / modifierExtension elements are already
 * stripped from the served models; the [x] choice marker is dropped for
 * display, as the table view does.
 */
(function () {
  'use strict';
  var NOISE = { id: 1, extension: 1, modifierExtension: 1 };
  var TRIVIAL = { Base: 1, Element: 1, BackboneElement: 1, Resource: 1, DomainResource: 1 };
  var baseUrl = (window.SITE_CONFIG && window.SITE_CONFIG.baseUrl) || '';
  var lang = (window.SITE_CONFIG && window.SITE_CONFIG.lang) || 'en';

  var sd = null;
  var parentSd = null;   // the model sd specialises, when it is one of ours
  var source = '';
  var byUrl = {};        // canonical url -> file, from the model list
  var byName = {};       // name -> file

  // ---------------------------------------------------------------- helpers
  function lastSeg(url) { return (url || '').split('|')[0].replace(/\/$/, '').split('/').pop(); }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function translated(obj, field) {
    var base = obj[field] || '';
    var ext = (obj['_' + field] || {}).extension || [];
    for (var i = 0; i < ext.length; i++) {
      if (ext[i].url !== 'http://hl7.org/fhir/StructureDefinition/translation') continue;
      var code = null, content = null;
      (ext[i].extension || []).forEach(function (sub) {
        if (sub.url === 'lang') code = sub.valueCode;
        if (sub.url === 'content') content = sub.valueString;
      });
      if (code === lang && content) return content;
    }
    return base;
  }
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

  // ---------------------------------------------------------------- model -> classes
  function relOf(e) { return e.path.split('.').slice(1).join('.'); }

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
    // which rels have children
    var rels = elements.map(function (e) { return e.path.split('.').slice(1).join('.'); });
    var hasChild = {};
    rels.forEach(function (r) { var p = r.split('.'); if (p.length > 1) hasChild[p.slice(0, -1).join('.')] = true; });

    elements.forEach(function (e) {
      var rel = e.path.split('.').slice(1).join('.');
      var parts = rel.split('.');
      var name = parts[parts.length - 1].replace(/\[x\]$/, '') + (e.sliceName ? ':' + e.sliceName : '');
      var parentRel = parts.slice(0, -1).join('.');
      var parent = byRel[parentRel];
      if (!parent) return; // parent was noise or not drawn
      var types = (e.type || []).map(typeName).filter(function (v, i, a) { return v && a.indexOf(v) === i; });
      var refTargets = [];
      (e.type || []).forEach(function (t) {
        if ((t.code || '') === 'Reference') (t.targetProfile || []).forEach(function (p) { refTargets.push(lastSeg(p)); });
      });
      if (hasChild[rel]) {
        var group = { key: sd.name + '.' + rel, name: name, card: card(e), attrs: [], children: [], refs: [], bindings: [],
                      short: translated(e, 'short') };
        parent.children.push(group);
        byRel[rel] = group;
        return;
      }
      var typeLabel = types.length ? types.join(' or ') : (e.contentReference ? 'see ' + lastSeg(e.contentReference.split('#').pop()) : '');
      if (refTargets.length) {
        typeLabel = 'Reference';
        refTargets.forEach(function (target) { parent.refs.push({ attr: name, target: target, card: card(e) }); });
      }
      parent.attrs.push({ name: name, type: typeLabel, card: card(e) });
      var vs = (e.binding || {}).valueSet;
      if (vs) parent.bindings.push({ attr: name, valueSet: lastSeg(vs), strength: e.binding.strength || '' });
    });
    return root;
  }

  // ---------------------------------------------------------------- classes -> nomnoml
  function classBox(node, isRoot) {
    var attrs = node.attrs.map(function (a) { return '+' + safe(a.name) + ' : ' + safe(a.type) + ' \\[' + a.card + '\\]'; });
    var title = isRoot ? safe(node.name) : safe(node.name);
    return '[' + title + (attrs.length ? '|' + attrs.join(';') : '') + ']';
  }
  function ref(node) { return '[' + safe(node.name) + ']'; }

  function toNomnoml(root, opts) {
    var lines = [
      '#direction: ' + (opts.direction || 'right'),
      '#font: Segoe UI, Calibri, Arial, sans-serif',
      '#fontSize: 11',
      '#lineWidth: 1.4',
      '#padding: 8',
      '#spacing: 36',
      '#edges: rounded',
      '#ranker: tight-tree',
      '#fill: #FEFECE; #F3F3F3',
      '#stroke: #33322E',
      '#arrowSize: 0.9',
      '#.reference: fill=#D9D9D9 dashed',
      '#.valueset: fill=#C3D69B visual=note',
      ''
    ];
    var seen = {};
    function walk(node, isRoot) {
      if (seen[node.key]) return;
      seen[node.key] = true;
      lines.push(classBox(node, isRoot));
      node.children.forEach(function (child) {
        walk(child, false);
        lines.push(ref(node) + ' 1 +-> ' + child.card + ' ' + ref(child));
      });
      if (opts.references) {
        node.refs.forEach(function (r) {
          lines.push('[<reference> ' + safe(r.target) + ']');
          lines.push(ref(node) + ' ' + safe(r.attr) + ' ' + r.card + ' -> [<reference> ' + safe(r.target) + ']');
        });
      }
      if (opts.bindings) {
        node.bindings.forEach(function (b) {
          var vsBox = '[<valueset> ' + safe(b.valueSet) + ']';
          lines.push(vsBox);
          lines.push(ref(node) + ' ' + safe(b.attr) + ' ' + safe(b.strength) + ' -- ' + vsBox);
        });
      }
    }
    walk(root, true);
    if (opts.parent) {
      var parentName = lastSeg(sd.baseDefinition || '');
      if (parentName && !TRIVIAL[parentName]) {
        if (parentSd) {
          // one of our models: a full class with its own elements and groups
          var parentRoot = buildModel(parentSd, null);
          walk(parentRoot, false);
          lines.push(ref(parentRoot) + ' <:- ' + ref(root));
        } else {
          lines.push('[<reference> ' + safe(parentName) + ']');
          lines.push('[<reference> ' + safe(parentName) + '] <:- ' + ref(root));
        }
      }
    }
    return lines.join('\n');
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

  function render() {
    if (!sd) return;
    var box = document.getElementById('umlDiagram');
    try {
      source = toNomnoml(buildModel(sd, options().parent ? parentSd : null), options());
      document.getElementById('umlSource').textContent = source;
      box.innerHTML = window.nomnoml.renderSvg(source);
      var svg = box.querySelector('svg');
      if (svg) {
        svg.setAttribute('role', 'img');
        svg.setAttribute('aria-label', 'UML class diagram of ' + sd.name);
      }
      status('');
    } catch (e) {
      box.innerHTML = '<p style="color:#b3261e">Could not draw the diagram: ' + esc(e.message) + '</p>';
      console.error(e);
    }
  }

  function downloadSvg() {
    var svg = document.querySelector('#umlDiagram svg');
    if (!svg) return;
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

  // ---------------------------------------------------------------- model list + selection
  function sanitize(name) { return (name || '').replace(/[^A-Za-z0-9._-]/g, ''); }
  function currentModel() { return sanitize(new URLSearchParams(window.location.search).get('model')); }

  function loadList() {
    var files = (window.SITE_CONFIG && window.SITE_CONFIG.modelFiles) || [];
    var sel = document.getElementById('modelSelector');
    return Promise.all(files.map(function (f) {
      var file = f.replace('StructureDefinition-', '').replace('.json', '');
      return fetch(baseUrl + '/_resources/models/' + f).then(function (r) { return r.ok ? r.json() : null; })
        .then(function (d) {
          if (!d) return null;
          if (d.url) byUrl[d.url.split('|')[0]] = file;
          if (d.name) byName[d.name] = file;
          return { file: file, title: translated(d, 'title') || d.name || file };
        })
        .catch(function () { return null; });
    })).then(function (list) {
      list = list.filter(Boolean).sort(function (a, b) { return a.title.localeCompare(b.title); });
      sel.innerHTML = '<option value="">—</option>' + list.map(function (m) {
        return '<option value="' + esc(m.file) + '">' + esc(m.title) + '</option>';
      }).join('');
      return list;
    });
  }

  function loadModel(file) {
    if (!file) {
      document.getElementById('modelTitle').innerHTML = '<h1>Select a model</h1>';
      document.getElementById('umlDiagram').innerHTML = '';
      return;
    }
    status('Loading…');
    fetch(baseUrl + '/_resources/models/StructureDefinition-' + file + '.json')
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
      .then(function (data) {
        sd = data;
        parentSd = null;
        var base = (sd.baseDefinition || '').split('|')[0];
        var parentFile = byUrl[base] || byName[lastSeg(base)];
        if (parentFile && !TRIVIAL[lastSeg(base)]) {
          return fetch(baseUrl + '/_resources/models/StructureDefinition-' + parentFile + '.json')
            .then(function (r) { return r.ok ? r.json() : null; })
            .then(function (pd) { parentSd = pd; return data; })
            .catch(function () { return data; });
        }
        return data;
      })
      .then(function (data) {
        document.getElementById('modelTitle').innerHTML = '<h1>' + esc(translated(sd, 'title') || sd.name) + '</h1>' +
          '<div style="color:#5c5962;font-size:0.9em">' + esc(sd.name) + ' · ' + esc(sd.version || '') + ' · ' + esc(sd.status || '') + '</div>';
        document.getElementById('modelDescription').textContent = translated(sd, 'description') || '';
        var tree = document.getElementById('treeViewLink');
        if (tree) tree.href = tree.getAttribute('href').split('?')[0] + '?model=' + encodeURIComponent(file);
        render();
      })
      .catch(function (e) { status('Could not load the model: ' + e.message); });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var sel = document.getElementById('modelSelector');
    loadList().then(function () {
      var m = currentModel();
      if (m) { sel.value = m; }
      loadModel(m);
    });
    sel.addEventListener('change', function () {
      var file = sel.value;
      window.history.pushState({}, '', window.location.pathname + (file ? '?model=' + encodeURIComponent(file) : ''));
      loadModel(file);
    });
    ['optReferences', 'optParent', 'optBindings', 'optDirection'].forEach(function (id) {
      document.getElementById(id).addEventListener('change', render);
    });
    document.getElementById('btnDownloadSvg').addEventListener('click', downloadSvg);
    document.getElementById('btnCopySource').addEventListener('click', copySource);
  });
})();
