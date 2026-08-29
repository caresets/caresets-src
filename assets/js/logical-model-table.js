// The logical-model table. Moved out of _layouts/logical-model.html so
// script-src can drop 'unsafe-inline'; Jekyll values arrive as JSON in
// #logical-model-config, which is data, not script.
(function() {
  var cfgEl = document.getElementById('logical-model-config');
  var pageConfig = cfgEl ? JSON.parse(cfgEl.textContent) : {};

  console.log('Loading StructureDefinition from:', pageConfig.dataSource);

  var dataTable = null;
  var structureDefinition = null;
  var targetElementPath = null;

  // Build glossary URL relative to current site and language
  function getGlossaryUrl(conceptCode) {
    var baseUrl = (pageConfig.baseUrl || '');
    return baseUrl + '/' + pageConfig.currentLang + '/' + pageConfig.glossaryPage + '#' + conceptCode;
  }

  document.addEventListener('DOMContentLoaded', function() {
    // Get element path from URL fragment (e.g., #Patient.identifier)
    if (window.location.hash) {
      targetElementPath = window.location.hash.substring(1); // Remove the #
      console.log('Target element path from URL:', targetElementPath);
    }

    initializeModel();

    if (pageConfig.showDownload) {
      initializeDownload();
    }

    document.getElementById('expandAllBtn').addEventListener('click', expandAll);
    document.getElementById('collapseAllBtn').addEventListener('click', collapseAll);
  });

  function initializeModel() {
    var url = pageConfig.dataSource;
    
    fetch(url)
      .then(function(response) {
        if (!response.ok) {
          throw new Error('HTTP ' + response.status + ': ' + response.statusText);
        }
        return response.json();
      })
      .then(function(data) {
        console.log('StructureDefinition loaded:', data);
        structureDefinition = data;
        processStructureDefinition(data);
      })
      .catch(function(error) {
        console.error('Error loading StructureDefinition:', error);
        showError(error.message);
      });
  }

  function processStructureDefinition(sd) {
    if (sd.resourceType !== 'StructureDefinition') {
      showError('Invalid resource: expected StructureDefinition, got ' + sd.resourceType);
      return;
    }
    
    // Display description
    if (sd.description) {
      document.getElementById('modelDescription').innerHTML = 
        '<p>' + escapeHtml(sd.description) + '</p>';
    }
    
    // Display metadata
    renderMetadata(sd);
    
    // Display elements
    var elements = sd.snapshot?.element || sd.differential?.element;
    if (!elements || !Array.isArray(elements)) {
      showError('No elements found in snapshot or differential');
      return;
    }
    
    renderElements(elements);
  }

  function renderMetadata(sd) {
    var tbody = '';

    // First row: URL
    if (sd.url) {
      tbody += '<tr><td style="padding: 6px; border: 1px solid #ddd; font-weight: bold; width: 150px;">URL</td>' +
               '<td style="padding: 6px; border: 1px solid #ddd;" colspan="5">' + escapeHtml(sd.url) + '</td></tr>';
    }

    // Second row: Version, Status, Date in one row (3 columns each)
    tbody += '<tr>';
    if (sd.version) {
      tbody += '<td style="padding: 6px; border: 1px solid #ddd; font-weight: bold; width: 150px;">Version</td>' +
               '<td style="padding: 6px; border: 1px solid #ddd;">' + escapeHtml(sd.version) + '</td>';
    }
    if (sd.status) {
      tbody += '<td style="padding: 6px; border: 1px solid #ddd; font-weight: bold; width: 150px;">Status</td>' +
               '<td style="padding: 6px; border: 1px solid #ddd;">' + escapeHtml(sd.status) + '</td>';
    }
    if (sd.date) {
      tbody += '<td style="padding: 6px; border: 1px solid #ddd; font-weight: bold; width: 150px;">Date</td>' +
               '<td style="padding: 6px; border: 1px solid #ddd;">' + escapeHtml(sd.date) + '</td>';
    }
    tbody += '</tr>';

    // Third row: Publisher and Type
    tbody += '<tr>';
    if (sd.publisher) {
      tbody += '<td style="padding: 6px; border: 1px solid #ddd; font-weight: bold; width: 150px;">Publisher</td>' +
               '<td style="padding: 6px; border: 1px solid #ddd;" colspan="2">' + escapeHtml(sd.publisher) + '</td>';
    }
    if (sd.type) {
      tbody += '<td style="padding: 6px; border: 1px solid #ddd; font-weight: bold; width: 150px;">Type</td>' +
               '<td style="padding: 6px; border: 1px solid #ddd;" colspan="2">' + escapeHtml(sd.type) + '</td>';
    }
    tbody += '</tr>';

    // Fourth row: Base Definition as link
    if (sd.baseDefinition) {
      var baseName = sd.baseDefinition.split('/').pop();
      tbody += '<tr><td style="padding: 6px; border: 1px solid #ddd; font-weight: bold; width: 150px;">Base Definition</td>' +
               '<td style="padding: 6px; border: 1px solid #ddd;" colspan="5">' +
               '<a href="' + escapeAttr(sd.baseDefinition) + '" target="_blank" rel="noopener noreferrer">' +
               escapeHtml(baseName) + '</a></td></tr>';
    }

    document.querySelector('#metadataTable tbody').innerHTML = tbody;
  }

  function renderElements(elements) {
    // Build hierarchy
    var hierarchy = buildHierarchy(elements);
    var tableBody = renderHierarchy(hierarchy, 0);
    
    document.querySelector('#elementsTable tbody').innerHTML = tableBody;
    
    // Initialize DataTable
    dataTable = $('#elementsTable').DataTable({
      pageLength: 50,
      paging: false,
      ordering: false,
      searching: true,
      info: false,
      autoWidth: false,
      columnDefs: [
        { width: '25%', targets: 0 },  // Element
        { width: '8%', targets: 1 },   // Card.
        { width: '12%', targets: 2 },  // Type
        { width: '30%', targets: 3 },  // Description
        { width: '15%', targets: 4 },  // Glossary
        { width: '10%', targets: 5 }   // Binding
      ],
      drawCallback: function() {
        // After any draw, reapply highlight if we have a target path
        if (targetElementPath) {
          applyHighlight();
        }
      },
      dom: 'Bfrt',
      buttons: (function () {
        var flags = pageConfig.exports || { excel: false, pdf: false, csv: true };
        var list = [];
        if (flags.excel) { list.push({ extend: 'excelHtml5',
          text: 'Excel',
          filename: 'model-' + pageConfig.title.replace(/[^a-z0-9]/gi, '_'),
          className: 'hidden-button',
          exportOptions: { columns: ':visible' } }); }
        if (flags.pdf) { list.push({ extend: 'pdfHtml5',
          text: 'PDF',
          filename: 'model-' + pageConfig.title.replace(/[^a-z0-9]/gi, '_'),
          title: pageConfig.title,
          className: 'hidden-button',
          orientation: 'landscape',
          pageSize: 'A4',
          exportOptions: { columns: ':visible' } }); }
        if (flags.csv) { list.push({ extend: 'csvHtml5',
          text: 'CSV',
          filename: 'model-' + pageConfig.title.replace(/[^a-z0-9]/gi, '_'),
          className: 'hidden-button',
          exportOptions: { columns: ':visible' } }); }
        return list;
      })()
    });
    
    $('.dt-buttons').hide();
    
    // Add click handlers for expand/collapse
    $('.toggle-children').on('click', function(e) {
      e.preventDefault();
      var elementPath = $(this).data('path');
      toggleChildren(elementPath);
    });

    // Initial highlight and navigation to target element
    if (targetElementPath) {
      navigateToAndHighlightElement();
    }
  }

  function applyHighlight() {
    // Simple function to just add highlight class to matching row
    // Does NOT trigger any navigation or scrolling
    $('#elementsTable tbody tr').removeClass('highlighted-element');
    var targetRow = $('#elementsTable tbody tr[data-path="' + targetElementPath + '"]');
    if (targetRow.length > 0) {
      targetRow.addClass('highlighted-element');
    }
  }

  function navigateToAndHighlightElement() {
    // One-time function called on initial load to navigate to the element
    var targetRow = $('#elementsTable tbody tr[data-path="' + targetElementPath + '"]');

    if (targetRow.length > 0) {
      console.log('Navigating to element:', targetElementPath);

      // Add highlight
      targetRow.addClass('highlighted-element');

      // Make sure the element is visible (expand parents if needed)
      expandParentsOfElement(targetElementPath);

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
      console.log('Element not found:', targetElementPath);
    }
  }

  function expandParentsOfElement(elementPath) {
    // Expand all parent elements to make the target visible
    var parts = elementPath.split('.');
    for (var i = 1; i < parts.length; i++) {
      var parentPath = parts.slice(0, i).join('.');
      var parentRow = $('#elementsTable tbody tr[data-path="' + parentPath + '"]');
      if (parentRow.length > 0) {
        var icon = parentRow.find('.toggle-children');
        if (icon.length > 0 && icon.text() === '▶') {
          // Parent is collapsed, expand it
          icon.text('▼');
          parentRow.removeClass('collapsed');
          var childRows = $('tr[data-path^="' + parentPath + '."]');
          var directChildren = childRows.filter(function() {
            var path = $(this).data('path');
            var childParts = path.split('.');
            var parentParts = parentPath.split('.');
            return childParts.length === parentParts.length + 1;
          });
          directChildren.show();
        }
      }
    }
  }

  function buildHierarchy(elements) {
    var hierarchy = [];
    var elementMap = {};
    
    elements.forEach(function(element) {
      var path = element.path;
      var parts = path.split('.');
      var depth = parts.length - 1;
      
      var item = {
        element: element,
        path: path,
        depth: depth,
        children: [],
        parent: null
      };
      
      elementMap[path] = item;
      
      if (depth === 0) {
        hierarchy.push(item);
      } else {
        var parentPath = parts.slice(0, -1).join('.');
        var parent = elementMap[parentPath];
        if (parent) {
          item.parent = parent;
          parent.children.push(item);
        } else {
          // Orphan element, add to root
          hierarchy.push(item);
        }
      }
    });
    
    return hierarchy;
  }

  function renderHierarchy(items, depth) {
    var html = '';
    
    items.forEach(function(item) {
      html += renderElement(item, depth);
      if (item.children.length > 0) {
        html += renderHierarchy(item.children, depth + 1);
      }
    });
    
    return html;
  }

  function renderElement(item, depth) {
    var element = item.element;
    var path = element.path;
    var parts = path.split('.');
    var name = parts[parts.length - 1];
    
    // Cardinality
    var card = (element.min || '0') + '..' + (element.max || '*');
    
    // Type
    var types = [];
    if (element.type && Array.isArray(element.type)) {
      types = element.type.map(function(t) { 
        var typeStr = t.code || '';
        if (t.profile && t.profile.length > 0) {
          typeStr += ' (' + t.profile[0].split('/').pop() + ')';
        }
        return typeStr;
      });
    }
    var typeStr = types.join(', ') || (element.contentReference ? 'See ' + element.contentReference : '');
    
    // Description
    var description = element.short || element.definition || '';

    // Check for glossary concept
    var glossary = '';
    if (element.code && Array.isArray(element.code)) {
      element.code.forEach(function(coding) {
        if (coding.system === pageConfig.glossarySystem && coding.code) {
          var display = coding.display || coding.code;
          var conceptUrl = getGlossaryUrl(coding.code);
          glossary = '<a href="' + escapeAttr(conceptUrl) + '" target="_blank" rel="noopener noreferrer">' +
                     escapeHtml(display) + '</a>';
        }
      });
    }

    // Binding
    var binding = '';
    if (element.binding) {
      var strength = element.binding.strength || '';
      var valueSet = element.binding.valueSet || '';
      binding = strength;
      if (valueSet) {
        var vsName = valueSet.split('/').pop();
        binding += ': ' + vsName;
      }
    }
    
    // Indentation and expand/collapse icon
    var indent = depth * 20;
    var hasChildren = item.children.length > 0;
    var expandIcon = hasChildren ?
      '<span class="toggle-children" data-path="' + escapeAttr(path) + '" style="cursor: pointer; margin-right: 5px;">▼</span>' :
      '<span style="margin-right: 5px; visibility: hidden;">▼</span>';

    var hasChildrenClass = hasChildren ? ' has-children' : '';
    
    var elementCell = '<div class="element-cell" style="padding-left: ' + indent + 'px; --line-left: ' + indent + 'px; display: flex; align-items: center;">' +
                      expandIcon +
                      '<span class="element-name" style="font-family: monospace; font-weight: ' + (depth === 0 ? 'bold' : 'normal') + ';">' +
                      escapeHtml(name) +
                      '</span></div>';
    
    var rowClass = 'element-row depth-' + depth + ' path-' + path.replace(/\./g, '-');
    if (depth > 0) {
      rowClass += ' child-row';
    }
    rowClass += hasChildrenClass;

    return '<tr class="' + rowClass + '" data-path="' + escapeAttr(path) + '" data-depth="' + depth + '" style="--row-indent: ' + indent + 'px;">' +
           '<td>' + elementCell + '</td>' +
           '<td>' + escapeHtml(card) + '</td>' +
           '<td>' + escapeHtml(typeStr) + '</td>' +
           '<td>' + escapeHtml(description) + '</td>' +
           '<td>' + glossary + '</td>' +
           '<td>' + escapeHtml(binding) + '</td>' +
           '</tr>';
  }

  function toggleChildren(parentPath) {
    var icon = $('.toggle-children[data-path="' + parentPath.replace(/\./g, '\\.') + '"]');
    var parentRow = icon.closest('tr');
    var isExpanded = icon.text() === '▼';

    // Find all child rows
    var childRows = $('tr[data-path^="' + parentPath + '."]');

    if (isExpanded) {
      // Collapse
      icon.text('▶');
      parentRow.addClass('collapsed');
      childRows.hide();
    } else {
      // Expand only direct children
      icon.text('▼');
      parentRow.removeClass('collapsed');
      var directChildren = childRows.filter(function() {
        var path = $(this).data('path');
        var parts = path.split('.');
        var parentParts = parentPath.split('.');
        return parts.length === parentParts.length + 1;
      });
      directChildren.show();
    }
  }

  function expandAll() {
    $('.toggle-children').text('▼');
    $('.toggle-children').closest('tr').removeClass('collapsed');
    $('.element-row').show();
  }

  function collapseAll() {
    $('.toggle-children').text('▶');
    $('.toggle-children').closest('tr').addClass('collapsed');
    $('.child-row').hide();
  }

  function escapeHtml(text) {
    if (!text) return '';
    var div = document.createElement('div');
    div.textContent = text.toString();
    return div.innerHTML;
  }

  function escapeAttr(text) {
    if (!text) return '';
    return text.toString()
      .replace(/&/g, '&amp;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  function showError(message) {
    document.querySelector('#elementsTable tbody').innerHTML =
      '<tr><td colspan="6" style="text-align:center; color: red;">' +
      '<b>Error loading model</b><br><br>' +
      escapeHtml(message) + '<br><br>' +
      'Source: ' + escapeHtml(pageConfig.dataSource) +
      '</td></tr>';
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
    var fileName = 'model-' + pageConfig.title.replace(/[^a-z0-9]/gi, '_');
    
    try {
      if (format === 'xlsx') {
        dataTable.button('.buttons-excel').trigger();
      } else if (format === 'pdf') {
        dataTable.button('.buttons-pdf').trigger();
      } else if (format === 'csv') {
        dataTable.button('.buttons-csv').trigger();
      } else if (format === 'md') {
        exportToMarkdown(fileName);
      }
    } catch (error) {
      console.error('Export error:', error);
      alert('Export failed: ' + error.message);
    }
  }

  function exportToMarkdown(fileName) {
    var content = [];
    content.push('# ' + pageConfig.title);
    content.push('');
    
    if (structureDefinition.description) {
      content.push(structureDefinition.description);
      content.push('');
    }
    
    content.push('## Metadata');
    content.push('');
    content.push('| Property | Value |');
    content.push('|----------|-------|');
    
    var metadata = [
      ['URL', structureDefinition.url],
      ['Version', structureDefinition.version],
      ['Status', structureDefinition.status],
      ['Date', structureDefinition.date]
    ];
    
    metadata.forEach(function(row) {
      if (row[1]) {
        content.push('| ' + row[0] + ' | ' + row[1] + ' |');
      }
    });
    
    content.push('');
    content.push('## Elements');
    content.push('');
    content.push('| Element | Card. | Type | Description | Glossary | Binding |');
    content.push('|---------|-------|------|-------------|----------|---------|');
    
    var visibleRows = $('#elementsTable tbody tr:visible');
    visibleRows.each(function() {
      var cells = $(this).find('td');
      var rowData = [];
      cells.each(function() {
        var text = $(this).text().trim().replace(/\|/g, '\\|').replace(/\n/g, ' ');
        rowData.push(text);
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
