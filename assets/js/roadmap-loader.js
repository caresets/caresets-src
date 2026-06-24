(function() {
  // Configuration
  var baseUrl = window.SITE_CONFIG && window.SITE_CONFIG.baseUrl ? window.SITE_CONFIG.baseUrl : '';
  var csvUrl = baseUrl + '/_resources/data/caresets-roadmap.csv';

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
