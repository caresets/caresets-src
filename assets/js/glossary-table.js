// The glossary table: loads the CodeSystem, renders it, wires the
// download menu. Moved out of _layouts/glossary.html so script-src can
// drop 'unsafe-inline'; its Jekyll values arrive as JSON in
// #glossary-config, which is data, not script.
(function() {
  var cfgEl = document.getElementById('glossary-config');
  var pageConfig = cfgEl ? JSON.parse(cfgEl.textContent) : {};
  
  console.log('Loading CodeSystem from:', pageConfig.dataSource);
  
  var dataTable = null;
  var targetConceptCode = null;

  document.addEventListener('DOMContentLoaded', function() {
    // Get concept code from URL fragment (e.g., #identifier)
    if (window.location.hash) {
      targetConceptCode = decodeURIComponent(window.location.hash.substring(1));
      console.log('Target concept code from URL:', targetConceptCode);
    }

    initializeGlossary();

    if (pageConfig.showDownload) {
      initializeDownload();
    }
  });

  // When the user clicks a concept-link in the same table, the URL fragment
  // changes but no page reload happens — re-trigger the highlight/scroll.
  window.addEventListener('hashchange', function() {
    if (!dataTable) return;
    targetConceptCode = window.location.hash
      ? decodeURIComponent(window.location.hash.substring(1))
      : null;
    if (targetConceptCode) {
      navigateToAndHighlightConcept();
    }
  });

  function initializeGlossary() {
    var url = pageConfig.dataSource;
    
    fetch(url)
      .then(function(response) {
        if (!response.ok) {
          throw new Error('HTTP ' + response.status + ': ' + response.statusText);
        }
        return response.json();
      })
      .then(function(data) {
        console.log('CodeSystem loaded:', data);
        processCodeSystem(data);
      })
      .catch(function(error) {
        console.error('Error loading CodeSystem:', error);
        showError(error.message);
      });
  }

  function processCodeSystem(data) {
    if (!data.concept || !Array.isArray(data.concept)) {
      showError('Invalid CodeSystem: missing "concept" array');
      return;
    }
    
    var concepts = data.concept;
    var tableBody = '';
    var hasDesignations = false;
    var hasDisplay = false;
    
    // Check structure of first concept
    if (concepts.length > 0) {
      hasDesignations = concepts[0].designation && Array.isArray(concepts[0].designation);
      hasDisplay = typeof concepts[0].display === 'string';
    }
    
    console.log('CodeSystem structure:', {
      conceptCount: concepts.length,
      hasDesignations: hasDesignations,
      hasDisplay: hasDisplay
    });

    concepts.forEach(function(concept) {
      var code = concept.code || 'N/A';
      var currentLangValue = '';
      var otherLangValues = {};
      var statusProperty = 'Unknown';
      
      // Get status
      if (concept.property && Array.isArray(concept.property)) {
        var statusProp = concept.property.find(function(p) { return p.code === 'status'; });
        if (statusProp) {
          statusProperty = statusProp.valueCode || statusProp.valueString || 'Unknown';
        }
      }
      
      // Try to get definitions in different languages
      if (hasDesignations && concept.designation && Array.isArray(concept.designation)) {
        // Standard FHIR with designation array
        var currentLangDesignation = concept.designation.find(function(d) { 
          return d.language === pageConfig.currentLang; 
        });
        
        if (currentLangDesignation) {
          currentLangValue = currentLangDesignation.value || currentLangDesignation.use?.display || '';
        } else if (concept.display) {
          // Fallback to display if no designation for current language
          currentLangValue = concept.display;
        }
        
        // Get other languages
        concept.designation.forEach(function(d) {
          if (d.language && d.language !== pageConfig.currentLang) {
            otherLangValues[d.language] = d.value || '';
          }
        });
        
      } else if (hasDisplay && concept.display) {
        // Simple format with just display
        currentLangValue = concept.display;
        
      } else if (concept.definition) {
        // Some CodeSystems use definition instead
        currentLangValue = concept.definition;
      }
      
      // Build row with data-code attribute for anchor targeting.
      // The Code cell is a self-anchor link so users can deep-link to a concept.
      var codeCell = '<a class="concept-link" href="#' + escapeAttr(code) + '">' + escapeHtml(code) + '</a>';
      var row = '<tr data-code="' + escapeAttr(code) + '"><td>' + codeCell + '</td><td>' + escapeHtml(currentLangValue) + '</td>';
      
      // Add other language columns (if using designation structure)
      if (hasDesignations) {
        // Get expected languages from site data
        (pageConfig.otherLangs || []).forEach(function (langCode) {
          var langValue = otherLangValues[langCode] || '';
          row += '<td>' + escapeHtml(langValue) + '</td>';
        });
      }
      
      if (pageConfig.showStatus) {
        var statusCell;
        var statusKey = (statusProperty || 'unknown').toLowerCase().replace(/[^a-z0-9_-]+/g, '-');
        var statusClass = 'glossary-status glossary-status--' + statusKey;
        if (pageConfig.linkStatus && statusProperty && statusProperty !== 'Unknown') {
          var statusAnchor = pageConfig.statusLinkBase + '#' + escapeAttr(statusProperty);
          statusCell = '<a class="' + statusClass + '" href="' + statusAnchor + '">' + escapeHtml(statusProperty) + '</a>';
        } else {
          statusCell = '<span class="' + statusClass + '">' + escapeHtml(statusProperty) + '</span>';
        }
        row += '<td>' + statusCell + '</td>';
      }
      row += '</tr>';
      tableBody += row;
    });

    document.querySelector('#codeSystemTable tbody').innerHTML = tableBody;
    
    dataTable = $('#codeSystemTable').DataTable({
      pageLength: 25,
      dom: 'Bfrtip',
      buttons: (function () {
        var flags = pageConfig.exports || { excel: false, pdf: false, csv: true };
        var list = [];
        if (flags.excel) { list.push({ extend: 'excelHtml5',
          text: 'Excel',
          filename: 'glossary-' + pageConfig.currentLang,
          className: 'hidden-button',
          exportOptions: { columns: ':visible' } }); }
        if (flags.pdf) { list.push({ extend: 'pdfHtml5',
          text: 'PDF',
          filename: 'glossary-' + pageConfig.currentLang,
          title: pageConfig.title,
          className: 'hidden-button',
          orientation: 'landscape',
          pageSize: 'A4',
          exportOptions: { columns: ':visible' } }); }
        if (flags.csv) { list.push({ extend: 'csvHtml5',
          text: 'CSV',
          filename: 'glossary-' + pageConfig.currentLang,
          className: 'hidden-button',
          exportOptions: { columns: ':visible' } }); }
        return list;
      })(),
      language: pageConfig.dtLanguage || {},
      drawCallback: function() {
        // After any draw, reapply highlight if we have a target code
        if (targetConceptCode) {
          applyHighlight();
        }
      }
    });
    
    $('.dt-buttons').hide();
    createColumnToggles();
    
    // Initial highlight and navigation to target concept
    if (targetConceptCode) {
      navigateToAndHighlightConcept();
    }
  }

  function applyHighlight() {
    // Simple function to just add highlight class to matching row
    // Does NOT trigger any navigation or scrolling
    $('#codeSystemTable tbody tr').removeClass('highlighted-concept');

    // Try exact match first, then case-insensitive match
    var targetRow = $('#codeSystemTable tbody tr[data-code="' + targetConceptCode + '"]');

    if (targetRow.length === 0) {
      // Try case-insensitive match
      var lowerCode = targetConceptCode.toLowerCase();
      $('#codeSystemTable tbody tr').each(function() {
        var rowCode = $(this).attr('data-code');
        if (rowCode && rowCode.toLowerCase() === lowerCode) {
          targetRow = $(this);
          return false; // break
        }
      });
    }

    if (targetRow.length > 0) {
      targetRow.addClass('highlighted-concept');
    }
  }

  function navigateToAndHighlightConcept() {
    // One-time function called on initial load to navigate to the concept
    var targetRow = $('#codeSystemTable tbody tr[data-code="' + targetConceptCode + '"]');

    // Try case-insensitive match if exact match fails
    if (targetRow.length === 0) {
      var lowerCode = targetConceptCode.toLowerCase();
      $('#codeSystemTable tbody tr').each(function() {
        var rowCode = $(this).attr('data-code');
        if (rowCode && rowCode.toLowerCase() === lowerCode) {
          targetRow = $(this);
          console.log('Found case-insensitive match:', rowCode, 'for', targetConceptCode);
          return false; // break
        }
      });
    }

    if (targetRow.length > 0) {
      console.log('Navigating to concept:', targetConceptCode);

      // Add highlight
      targetRow.addClass('highlighted-concept');

      // Calculate which page the row is on
      var rowIndex = dataTable.row(targetRow).index();
      var pageLength = dataTable.page.len();
      var targetPage = Math.floor(rowIndex / pageLength);
      var currentPage = dataTable.page();

      // Navigate to page if needed (this will trigger drawCallback which reapplies highlight)
      if (currentPage !== targetPage) {
        dataTable.page(targetPage).draw('page');
      }

      // Scroll to the row
      setTimeout(function() {
        if (targetRow.length > 0 && targetRow[0]) {
          targetRow[0].scrollIntoView({
            behavior: 'smooth',
            block: 'center'
          });
        }
      }, 300);
    } else {
      console.log('Concept not found:', targetConceptCode);
    }
  }

  function escapeHtml(text) {
    if (!text) return '';
    var div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  function escapeAttr(text) {
    if (!text) return '';
    return text.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function showError(message) {
    document.querySelector('#codeSystemTable tbody').innerHTML = 
      '<tr><td colspan="100%" style="text-align:center; color: red;">' +
      '<b>Error loading glossary</b><br><br>' +
      escapeHtml(message) + '<br><br>' +
      'Source: ' + escapeHtml(pageConfig.dataSource) + '<br><br>' +
      '<details><summary>Troubleshooting</summary>' +
      '<ul style="text-align: left; margin: 10px auto; max-width: 600px;">' +
      '<li>Check browser console (F12) for details</li>' +
      '<li>Verify the URL is accessible</li>' +
      '<li>Check if the JSON structure matches FHIR CodeSystem format</li>' +
      '<li>Try loading the URL directly in your browser</li>' +
      '</ul></details>' +
      '</td></tr>';
  }

  function createColumnToggles() {
    var container = document.getElementById('columnToggles');
    if (!container || !dataTable) return;
    
    dataTable.columns().every(function(index) {
      var column = this;
      var header = $(column.header()).text();
      
      var label = document.createElement('label');
      label.style.display = 'flex';
      label.style.alignItems = 'center';
      label.style.gap = '5px';
      label.style.cursor = 'pointer';
      label.style.fontSize = '0.9em';
      
      var checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.checked = column.visible();
      
      checkbox.addEventListener('change', function() {
        column.visible(this.checked);
      });
      
      label.appendChild(checkbox);
      label.appendChild(document.createTextNode(header));
      container.appendChild(label);
    });
  }

  function initializeDownload() {
    var downloadBtn = document.getElementById('downloadBtn');
    if (!downloadBtn) return;
    downloadBtn.addEventListener('click', handleDownload);
  }

  function handleDownload(e) {
    e.preventDefault();
    
    if (!dataTable) {
      alert('Table not initialized yet. Please wait.');
      return;
    }
    
    var format = document.getElementById('downloadFormat').value;
    var fileName = 'glossary-' + pageConfig.currentLang;
    
    try {
      if (format === 'xlsx') {
        dataTable.button('.buttons-excel').trigger();
      } else if (format === 'pdf') {
        dataTable.button('.buttons-pdf').trigger();
      } else if (format === 'csv') {
        dataTable.button('.buttons-csv').trigger();
      } else if (format === 'md') {
        exportToMarkdown(dataTable, fileName);
      }
    } catch (error) {
      console.error('Export error:', error);
      alert('Export failed: ' + error.message);
    }
  }

  function exportToMarkdown(table, fileName) {
    var visibleColumns = [];
    table.columns().every(function(index) {
      if (this.visible()) visibleColumns.push(index);
    });
    
    var headers = [];
    visibleColumns.forEach(function(colIndex) {
      headers.push($(table.column(colIndex).header()).text());
    });
    
    var data = table.rows({ search: 'applied' }).data();
    var content = [];
    content.push('# ' + pageConfig.title);
    content.push('');
    content.push('| ' + headers.join(' | ') + ' |');
    content.push('|' + headers.map(function() { return '---'; }).join('|') + '|');
    
    data.each(function(row) {
      var rowData = [];
      visibleColumns.forEach(function(colIndex) {
        var cell = (row[colIndex] || '').toString().replace(/\|/g, '\\|').replace(/\n/g, '<br>');
        rowData.push(cell);
      });
      content.push('| ' + rowData.join(' | ') + ' |');
    });
    
    downloadFile(content.join('\n'), fileName + '.md', 'text/markdown;charset=utf-8;');
  }

  function downloadFile(content, fileName, mimeType) {
    var blob = new Blob([content], { type: mimeType });
    var link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = fileName;
    link.style.display = 'none';
    
    document.body.appendChild(link);
    link.click();
    
    setTimeout(function() {
      document.body.removeChild(link);
      URL.revokeObjectURL(link.href);
    }, 100);
  }
})();
