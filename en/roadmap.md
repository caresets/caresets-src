---
layout: default
title: Roadmap
nav_order: 1
parent: About
lang: en
---

# CareSets Roadmap

This roadmap outlines the current status and planned development of CareSets. Each CareSet represents a domain-specific collection of logical data models.

## Status Definitions

- **Published**: Available for use, documented, and validated
- **In Progress**: Currently under development and review
- **Planned**: Scheduled for future development

<div id="roadmapTableContainer" style="margin: 30px 0;">
  <table id="roadmapTable" class="display" style="width:100%;">
    <thead>
      <tr>
        <th>CareSet Name</th>
        <th>Status</th>
        <th>Description</th>
        <th>Target Date</th>
        <th>Priority</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td colspan="5" style="text-align: center; padding: 40px; color: #666;">
          Loading roadmap data...
        </td>
      </tr>
    </tbody>
  </table>
</div>

<script type="text/javascript">
(function() {
  // Configuration
  var csvUrl = '{{ site.baseurl }}/_resources/data/caresets-roadmap.csv';

  // Load and parse CSV
  fetch(csvUrl)
    .then(function(response) {
      if (!response.ok) {
        throw new Error('Failed to load roadmap data');
      }
      return response.text();
    })
    .then(function(csvText) {
      var rows = parseCSV(csvText);
      populateRoadmapTable(rows);
    })
    .catch(function(error) {
      document.querySelector('#roadmapTable tbody').innerHTML =
        '<tr><td colspan="5" style="text-align: center; padding: 40px; color: #d33;">' +
        'Error loading roadmap data: ' + error.message + '</td></tr>';
    });

  function parseCSV(text) {
    var lines = text.trim().split('\n');
    var headers = lines[0].split(',');
    var rows = [];

    for (var i = 1; i < lines.length; i++) {
      var values = lines[i].split(',');
      var row = {};
      for (var j = 0; j < headers.length; j++) {
        row[headers[j].trim()] = values[j] ? values[j].trim() : '';
      }
      rows.push(row);
    }

    return rows;
  }

  function populateRoadmapTable(rows) {
    var tbody = '';

    rows.forEach(function(row) {
      var statusClass = 'status-' + row.status.toLowerCase().replace(/\s+/g, '-');

      tbody += '<tr>' +
        '<td><strong>' + escapeHtml(row.name) + '</strong></td>' +
        '<td><span class="status-badge ' + statusClass + '">' + escapeHtml(row.status) + '</span></td>' +
        '<td>' + escapeHtml(row.description) + '</td>' +
        '<td>' + escapeHtml(row.target_date) + '</td>' +
        '<td>' + escapeHtml(row.priority) + '</td>' +
        '</tr>';
    });

    document.querySelector('#roadmapTable tbody').innerHTML = tbody;

    // Initialize DataTable if available
    if (typeof jQuery !== 'undefined' && jQuery.fn.DataTable) {
      jQuery('#roadmapTable').DataTable({
        paging: false,
        searching: true,
        order: [[3, 'asc']], // Sort by target date
        language: {
          search: 'Filter:'
        }
      });
    }
  }

  function escapeHtml(text) {
    var map = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
  }
})();
</script>

<style>
.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85em;
  font-weight: 500;
  text-transform: uppercase;
  white-space: nowrap;
}

.status-published {
  background-color: #28a745;
  color: white;
}

.status-in-progress {
  background-color: #ffc107;
  color: #000;
}

.status-planned {
  background-color: #6c757d;
  color: white;
}

#roadmapTable {
  font-size: 0.9em;
}

#roadmapTable td {
  vertical-align: top;
  padding: 10px !important;
}

#roadmapTable th {
  padding: 12px 10px !important;
  background-color: #f8f9fa;
}
</style>