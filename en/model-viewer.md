---
layout: default
title: Model Viewer
parent: Logical Models
nav_order: 1
---

<main id="modelViewerMain">
  <div style="margin-bottom: 20px;">
    <label for="modelSelector" style="font-weight: bold; margin-right: 10px;">Select Model:</label>
    <select id="modelSelector" style="padding: 8px; min-width: 300px; border: 1px solid #ddd; border-radius: 4px;">
      <option value="">Loading models...</option>
    </select>
  </div>

  <div id="modelTitle">
    <h1>Loading model...</h1>
  </div>

  <div id="modelDescription" style="margin: 20px 0;">
    <!-- Description will be inserted here -->
  </div>

  <h2>Metadata</h2>
  <table id="metadataTable" class="metadata-table" style="width: 100%; margin: 20px 0; border-collapse: collapse;">
    <tbody>
      <!-- Metadata will be dynamically inserted here -->
    </tbody>
  </table>

  <div id="downloadSection" style="margin: 20px 0; padding: 15px; background: #f5f6fa; border-radius: 6px;">
    <b>Download this model</b><br>
    <form id="downloadForm" style="margin-top: 10px;">
      <label for="downloadFormat">Format:</label>
      <select id="downloadFormat" style="margin: 0 10px; padding: 5px;">
        <option value="xlsx">Excel (XLSX)</option>
        <option value="pdf">PDF</option>
        <option value="md">Markdown (MD)</option>
        <option value="csv">CSV</option>
      </select>
      <button type="button" id="downloadBtn" style="padding: 5px 15px; background: #5c5962; color: white; border: none; border-radius: 4px; cursor: pointer;">Download</button>
    </form>
  </div>

  <h2>Element Structure</h2>
  
  <div style="margin: 10px 0;">
    <button id="expandAllBtn" style="padding: 5px 15px; margin-right: 10px; background: #5c5962; color: white; border: none; border-radius: 4px; cursor: pointer;">Expand All</button>
    <button id="collapseAllBtn" style="padding: 5px 15px; background: #5c5962; color: white; border: none; border-radius: 4px; cursor: pointer;">Collapse All</button>
  </div>
  
  <table id="elementsTable" class="display elements-table" style="width:100%; margin-top: 10px;">
    <thead>
      <tr>
        <th style="width: 25%;">Element</th>
        <th style="width: 8%;">Card.</th>
        <th style="width: 12%;">Type</th>
        <th style="width: 30%;">Description</th>
        <th style="width: 15%;">Glossary</th>
        <th style="width: 10%;">Binding</th>
      </tr>
    </thead>
    <tbody>
      <!-- Elements will be dynamically inserted here -->
    </tbody>
  </table>
</main>

<script type="text/javascript">
  // Configuration object for Jekyll variables
  window.SITE_CONFIG = {
    baseUrl: '{{ site.baseurl }}',
    modelFiles: [
      {% for file in site.static_files %}
        {% if file.path contains '/_resources/models/StructureDefinition-' and file.extname == '.json' %}
          '{{ file.name }}'{% unless forloop.last %},{% endunless %}
        {% endif %}
      {% endfor %}
    ]
  };
</script>

<script type="text/javascript" src="{{ site.baseurl }}/assets/js/model-viewer.js"></script>

<style>
.metadata-table td {
  border: 1px solid #ddd;
  padding: 6px;
}

.metadata-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.elements-table {
  font-size: 0.9em;
}

.elements-table td {
  vertical-align: top;
  padding: 4px 8px !important;
}

.elements-table td.element-col {
  position: relative;
}

.elements-table th {
  padding: 6px 8px !important;
}

.element-name {
  font-family: 'Courier New', monospace;
}

.element-cell {
  position: relative;
}

/* Tree connector styles - positioned relative to td cell */
.tree-connector {
  pointer-events: none;
}

/* Branch connector (├─) - vertical line goes through entire cell */
.tree-branch::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 1px;
  background: #ccc;
}

.tree-branch::after {
  content: '';
  position: absolute;
  left: 0;
  top: 10px;
  width: 20px;
  height: 1px;
  background: #ccc;
}

/* Corner connector (└─) - vertical line goes to middle only */
.tree-corner::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 1px;
  height: 10px;
  background: #ccc;
}

.tree-corner::after {
  content: '';
  position: absolute;
  left: 0;
  top: 10px;
  width: 20px;
  height: 1px;
  background: #ccc;
}

.toggle-children {
  user-select: none;
  color: #5c5962;
  flex-shrink: 0;
}

.toggle-children:hover {
  color: #000;
}

.dt-buttons { 
  display: none !important; 
}

.hidden-button { 
  display: none !important; 
}

.child-row {
  display: none;
}

/* Highlight style for linked elements from glossary */
.highlighted-element {
  background-color: #ffffcc !important;
  border: 2px solid #ffcc00 !important;
  animation: pulse-highlight 2s ease-in-out;
}

@keyframes pulse-highlight {
  0%, 100% { background-color: #ffffcc; }
  50% { background-color: #ffee88; }
}

/* Make sure highlighted row is visible even in striped tables */
.highlighted-element td {
  background-color: inherit !important;
}
</style>