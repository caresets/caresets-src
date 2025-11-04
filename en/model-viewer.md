---
layout: default
title: Model Viewer
parent: Logical Data Models
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
        <th>Element</th>
        <th>Card.</th>
        <th>Type</th>
        <th>Description</th>
        <th>Binding</th>
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

.elements-table th {
  padding: 6px 8px !important;
}

.element-name {
  font-family: 'Courier New', monospace;
}

.toggle-children {
  user-select: none;
  color: #5c5962;
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
</style>