---
layout: default
title: Logische datamodellen
nav_order: 2
lang: nl
---

<h1>Logische modellen</h1>

<p>Blader door de logische modellen.</p>

<div id="modelsContainer" style="margin: 30px 0;">
  <table id="modelsTable" class="display" style="width:100%;">
    <thead>
      <tr>
        <th>Titel</th>
        <th>Status</th>
        <th>Beschrijving</th>
        <th>Versie</th>
        <th>Datum</th>
        <th>URL</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td colspan="6" style="text-align: center; padding: 40px; color: #666;">
          Modellen aan het ontdekken...
        </td>
      </tr>
    </tbody>
  </table>
</div>

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

<script type="text/javascript" src="{{ site.baseurl }}/assets/js/logical-models-index.js"></script>

<style>
#modelsTable {
  font-size: 0.9em;
}

#modelsTable td {
  vertical-align: top;
  padding: 8px !important;
}

#modelsTable th {
  padding: 10px 8px !important;
}

.status-badge {
  text-transform: uppercase;
  font-size: 0.8em;
  white-space: nowrap;
}

.status-active {
  background-color: #28a745;
  color: white;
}

.status-draft {
  background-color: #ffc107;
  color: #000;
}

.status-retired {
  background-color: #6c757d;
  color: white;
}

.status-unknown {
  background-color: #e1e4e8;
  color: #586069;
}
</style>
