/* The Concept tab of the model viewer: the model as a concept diagram.
 *
 * The model sits at the centre in amber; each of its elements is a box on a
 * ring around it, blue for data, grey for references, amber for a group
 * (BackboneElement) whose own elements sit on an outer ring pointing at it.
 * A dashed arrow runs from each element into the concept it belongs to,
 * labelled with the element's cardinality: red when required (min >= 1),
 * green when optional. A bound ValueSet is a green box beyond the element
 * that binds it, with a solid arrow from the element.
 *
 * Drawn as plain SVG with a radial layout computed here: the layered engine
 * behind the UML tab cannot place boxes around a centre. No library needed.
 *
 * Listens for  caresets:model-loaded  {sd} from model-viewer.js and for
 * caresets:view-shown  {view} from the tab code in model-uml.js, and draws
 * when the Concept tab is visible.
 */
(function () {
  'use strict';
  var NOISE = { id: 1, extension: 1, modifierExtension: 1 };
  var lang = (window.SITE_CONFIG && window.SITE_CONFIG.lang) || 'en';
  var SVG = 'http://www.w3.org/2000/svg';

  var COLORS = {
    concept:   { fill: '#FAC08F', stroke: '#E36C0A', text: '#000' },
    data:      { fill: '#B8CCE4', stroke: '#4F81BD', text: '#1F4E79' },
    reference: { fill: '#F2F2F2', stroke: '#808080', text: '#404040' },
    valueset:  { fill: '#C3D69B', stroke: '#77933C', text: '#385723' },
    required:  '#C00000',
    optional:  '#00B050',
    line:      '#7F7F7F'
  };

  var sd = null;
  var dirty = false;

  // ---------------------------------------------------------------- helpers
  function lastSeg(url) { return (url || '').split('|')[0].replace(/\/$/, '').split('/').pop(); }
  function relOf(e) { return e.path.split('.').slice(1).join('.'); }
  function card(el) { return (el.min == null ? 0 : el.min) + '..' + (el.max == null ? '1' : el.max); }
  function isRef(el) { return (el.type || []).some(function (t) { return (t.code || '') === 'Reference'; }); }
  function translated(obj, field) {
    var base = obj[field] || '';
    var ext = (obj['_' + field] || {}).extension || [];
    for (var i = 0; i < ext.length; i++) {
      if (ext[i].url !== 'http://hl7.org/fhir/StructureDefinition/translation') continue;
      var code = null, content = null;
      (ext[i].extension || []).forEach(function (sub) { if (sub.url === 'lang') code = sub.valueCode; if (sub.url === 'content') content = sub.valueString; });
      if (code === lang && content) return content;
    }
    return base;
  }
  function label(name) {
    // Category, RecordedDate -> "Recorded Date": readable, as in the hand-drawn diagrams
    var s = name.replace(/\[x\]$/, '').replace(/([a-z0-9])([A-Z])/g, '$1 $2');
    return s.charAt(0).toUpperCase() + s.slice(1);
  }

  // ---------------------------------------------------------------- model -> tree
  function buildTree(sd) {
    var root = { name: sd.name, kind: 'concept', children: [], el: null };
    var byRel = { '': root };
    var elements = ((sd.snapshot || {}).element || []).filter(function (e) {
      return e.path && e.path.indexOf('.') > 0 && !NOISE[e.path.split('.').pop()];
    });
    var hasChild = {};
    elements.forEach(function (e) { var p = relOf(e).split('.'); if (p.length > 1) hasChild[p.slice(0, -1).join('.')] = true; });
    elements.forEach(function (e) {
      var rel = relOf(e), parts = rel.split('.');
      var parent = byRel[parts.slice(0, -1).join('.')];
      if (!parent) return;
      var node = {
        name: parts[parts.length - 1] + (e.sliceName ? ':' + e.sliceName : ''),
        kind: hasChild[rel] ? 'concept' : (isRef(e) ? 'reference' : 'data'),
        card: card(e), required: (e.min || 0) >= 1,
        short: translated(e, 'short'),
        valueSet: (e.binding && e.binding.valueSet) ? lastSeg(e.binding.valueSet) : null,
        children: [], el: e
      };
      parent.children.push(node);
      byRel[rel] = node;
    });
    return root;
  }

  // ---------------------------------------------------------------- layout
  function textWidth(s, size) { return Math.max(48, s.length * size * 0.58 + 22); }

  function layout(root, opts) {
    var boxes = [], edges = [];
    var BOX_H = 38, VS_H = 40, VS_GAP = 96;
    function box(node, x, y, w, h) {
      var b = { node: node, x: x, y: y, w: w, h: h };
      boxes.push(b);
      return b;
    }
    var cw = textWidth(root.name, 12) + 40;
    var centre = box(root, -cw / 2, -34, cw, 68);

    // ring 1: the model's direct elements, evenly around the centre
    var n = root.children.length;
    if (!n) return { boxes: boxes, edges: edges };
    var slot = 150;                                   // room per box along the ring
    var r1 = Math.max(230, n * slot / (2 * Math.PI));
    var start = -Math.PI / 2;                          // first element at the top
    root.children.forEach(function (child, i) {
      var a = start + (2 * Math.PI * i) / n;
      var w = textWidth(label(child.name), 11);
      var cx = Math.cos(a) * r1, cy = Math.sin(a) * r1;
      var b = box(child, cx - w / 2, cy - BOX_H / 2, w, BOX_H);
      edges.push({ from: b, to: centre, card: child.card, required: child.required, dashed: true });
      var dir = { x: Math.cos(a), y: Math.sin(a) };

      // its ValueSet, further out along the same direction
      if (opts.valueSets && child.valueSet) {
        var vw = textWidth(child.valueSet, 10);
        var vx = cx + dir.x * (w / 2 + VS_GAP + vw / 2), vy = cy + dir.y * (BOX_H / 2 + VS_GAP / 2 + VS_H / 2) * 1.2;
        var vb = box({ name: child.valueSet, kind: 'valueset' }, vx - vw / 2, vy - VS_H / 2, vw, VS_H);
        edges.push({ from: b, to: vb, dashed: false });
      }

      // ring 2: a group's own elements, in a sector around the group
      if (child.children.length) {
        var k = child.children.length;
        var r2 = r1 + 190 + (opts.valueSets && child.valueSet ? 40 : 0);
        var spread = Math.min(Math.PI / 2, Math.max(0.35, k * 0.28));
        child.children.forEach(function (g, j) {
          var ga = k === 1 ? a : a - spread / 2 + (spread * j) / (k - 1);
          var gw = textWidth(label(g.name), 11);
          var gx = Math.cos(ga) * r2, gy = Math.sin(ga) * r2;
          var gb = box(g, gx - gw / 2, gy - BOX_H / 2, gw, BOX_H);
          edges.push({ from: gb, to: b, card: g.card, required: g.required, dashed: true });
          if (opts.valueSets && g.valueSet) {
            var gvw = textWidth(g.valueSet, 10);
            var gvx = gx + Math.cos(ga) * (gw / 2 + VS_GAP / 2 + gvw / 2), gvy = gy + Math.sin(ga) * (BOX_H + VS_H / 2 + 20);
            var gvb = box({ name: g.valueSet, kind: 'valueset' }, gvx - gvw / 2, gvy - VS_H / 2, gvw, VS_H);
            edges.push({ from: gb, to: gvb, dashed: false });
          }
        });
      }
    });
    return { boxes: boxes, edges: edges };
  }

  // ---------------------------------------------------------------- drawing
  function el(tag, attrs, text) {
    var e = document.createElementNS(SVG, tag);
    Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (text != null) e.textContent = text;
    return e;
  }
  function centreOf(b) { return { x: b.x + b.w / 2, y: b.y + b.h / 2 }; }
  // where a line from the box centre towards p leaves the box
  function borderPoint(b, p) {
    var c = centreOf(b), dx = p.x - c.x, dy = p.y - c.y;
    if (!dx && !dy) return c;
    var sx = (b.w / 2) / Math.abs(dx || 1e-9), sy = (b.h / 2) / Math.abs(dy || 1e-9);
    var s = Math.min(sx, sy);
    return { x: c.x + dx * s, y: c.y + dy * s };
  }

  function draw(g, opts) {
    var pad = 30;
    var minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    g.boxes.forEach(function (b) {
      minX = Math.min(minX, b.x); minY = Math.min(minY, b.y);
      maxX = Math.max(maxX, b.x + b.w); maxY = Math.max(maxY, b.y + b.h);
    });
    var W = maxX - minX + 2 * pad, H = maxY - minY + 2 * pad;
    var svg = el('svg', { xmlns: SVG, viewBox: [minX - pad, minY - pad, W, H].join(' '), width: W, height: H,
                          role: 'img', 'aria-label': 'Concept diagram of ' + sd.name,
                          'font-family': 'Segoe UI, Calibri, Arial, sans-serif' });
    var defs = el('defs');
    ['concept', 'valueset', 'line'].forEach(function (k) {
      var m = el('marker', { id: 'arrow-' + k, viewBox: '0 0 10 10', refX: 10, refY: 5, markerWidth: 9, markerHeight: 9, orient: 'auto' });
      m.appendChild(el('path', { d: 'M0,0 L10,5 L0,10 z', fill: k === 'line' ? COLORS.line : COLORS[k].stroke }));
      defs.appendChild(m);
    });
    svg.appendChild(defs);

    // edges first, so boxes sit on top
    g.edges.forEach(function (e) {
      var from = borderPoint(e.from, centreOf(e.to)), to = borderPoint(e.to, centreOf(e.from));
      var line = el('line', { x1: from.x, y1: from.y, x2: to.x, y2: to.y, stroke: COLORS.line, 'stroke-width': 1.2,
                              'marker-end': 'url(#arrow-' + (e.dashed ? 'line' : 'valueset') + ')' });
      if (e.dashed) line.setAttribute('stroke-dasharray', '5 4');
      svg.appendChild(line);
      if (e.card) {
        // the cardinality a third of the way from the element to its concept
        var t = 0.32, lx = from.x + (to.x - from.x) * t, ly = from.y + (to.y - from.y) * t;
        var bg = el('rect', { x: lx - 15, y: ly - 8, width: 30, height: 16, rx: 3, fill: '#fff', 'fill-opacity': 0.85 });
        svg.appendChild(bg);
        svg.appendChild(el('text', { x: lx, y: ly + 4, 'text-anchor': 'middle', 'font-size': 11, 'font-weight': 'bold',
                                     fill: e.required ? COLORS.required : COLORS.optional }, e.card));
      }
    });

    g.boxes.forEach(function (b) {
      var c = COLORS[b.node.kind];
      var group = el('g');
      if (b.node.short) group.appendChild(el('title', {}, b.node.short));
      group.appendChild(el('rect', { x: b.x, y: b.y, width: b.w, height: b.h, fill: c.fill, stroke: c.stroke, 'stroke-width': 1.4 }));
      if (b.node.kind === 'valueset') {
        group.appendChild(el('text', { x: b.x + b.w / 2, y: b.y + 15, 'text-anchor': 'middle', 'font-size': 9, fill: c.text }, "'ValueSet'"));
        group.appendChild(el('text', { x: b.x + b.w / 2, y: b.y + 30, 'text-anchor': 'middle', 'font-size': 10, 'font-weight': 'bold', fill: c.text }, b.node.name));
      } else {
        var isCentre = b.node === g.boxes[0].node;
        group.appendChild(el('text', { x: b.x + b.w / 2, y: b.y + b.h / 2 + 4, 'text-anchor': 'middle',
                                       'font-size': isCentre ? 12 : 11, 'font-weight': 'bold', fill: c.text },
                             isCentre ? b.node.name : label(b.node.name)));
      }
      svg.appendChild(group);
    });
    return svg;
  }

  // ---------------------------------------------------------------- wiring
  function visible() { var p = document.getElementById('panel-concept'); return p && !p.hidden; }
  function options() { return { valueSets: document.getElementById('cptValueSets').checked }; }

  function render() {
    if (!sd) return;
    var box = document.getElementById('conceptDiagram');
    box.innerHTML = '';
    try {
      box.appendChild(draw(layout(buildTree(sd), options()), options()));
      dirty = false;
    } catch (e) {
      box.textContent = 'Could not draw the diagram: ' + e.message;
      console.error(e);
    }
  }
  function downloadSvg() {
    var svg = document.querySelector('#conceptDiagram svg');
    if (!svg || !sd) return;
    var blob = new Blob(['<?xml version="1.0" encoding="UTF-8"?>\n' + svg.outerHTML], { type: 'image/svg+xml;charset=utf-8' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = sd.name + '-concept.svg';
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 0);
  }

  document.addEventListener('DOMContentLoaded', function () {
    if (!document.getElementById('panel-concept')) return;
    document.getElementById('cptValueSets').addEventListener('change', render);
    document.getElementById('btnDownloadConcept').addEventListener('click', downloadSvg);
    document.addEventListener('caresets:model-loaded', function (ev) {
      sd = ev.detail && ev.detail.sd; dirty = true;
      if (visible()) render();
    });
    document.addEventListener('caresets:view-shown', function (ev) {
      if (ev.detail && ev.detail.view === 'concept' && dirty) render();
    });
    if (visible() && sd) render();
  });
})();
