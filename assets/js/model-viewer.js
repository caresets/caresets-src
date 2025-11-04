(function() {
    var structureDefinition = null;
    var dataTable = null;
    var modelName = null;
  
    document.addEventListener('DOMContentLoaded', function() {
      // Get model name from URL parameter
      var urlParams = new URLSearchParams(window.location.search);
      modelName = urlParams.get('model');
      
      // Load available models for dropdown
      loadModelsList();
      
      if (modelName) {
        initializeModel();
      } else {
        document.getElementById('modelTitle').innerHTML = '<h1>Select a model from the dropdown above</h1>';
      }
      
      document.getElementById('expandAllBtn').addEventListener('click', expandAll);
      document.getElementById('collapseAllBtn').addEventListener('click', collapseAll);
      document.getElementById('downloadBtn').addEventListener('click', handleDownload);
      document.getElementById('modelSelector').addEventListener('change', handleModelSelection);
    });
  
    function loadModelsList() {
      var manifestUrl = window.SITE_CONFIG.baseUrl + '/_resources/models-manifest.json';
      
      fetch(manifestUrl)
        .then(function(response) {
          if (!response.ok) {
            throw new Error('Manifest not found');
          }
          return response.json();
        })
        .then(function(manifest) {
          populateModelSelector(manifest.models || []);
        })
        .catch(function(error) {
          console.log('No manifest found, trying fallback');
          // Fallback: try to use a pre-generated list if available
          var modelFiles = window.SITE_CONFIG.modelFiles || [];
          populateModelSelector(modelFiles);
        });
    }
  
    function populateModelSelector(modelFiles) {
      var selector = document.getElementById('modelSelector');
      
      if (modelFiles.length === 0) {
        selector.innerHTML = '<option value="">No models available</option>';
        return;
      }
      
      // Load metadata for each model to get titles
      var promises = modelFiles.map(function(modelFile) {
        var fileName = modelFile.replace('StructureDefinition-', '').replace('.json', '');
        var url = window.SITE_CONFIG.baseUrl + '/_resources/models/' + modelFile;
        
        return fetch(url)
          .then(function(response) {
            if (!response.ok) throw new Error('Failed to load');
            return response.json();
          })
          .then(function(data) {
            return {
              file: fileName,
              title: data.title || data.name || fileName
            };
          })
          .catch(function(error) {
            return {
              file: fileName,
              title: fileName
            };
          });
      });
      
      Promise.all(promises).then(function(models) {
        models.sort(function(a, b) {
          return a.title.localeCompare(b.title);
        });
        
        var options = '<option value="">-- Select a model --</option>';
        models.forEach(function(model) {
          var selected = model.file === modelName ? ' selected' : '';
          options += '<option value="' + model.file + '"' + selected + '>' + escapeHtml(model.title) + '</option>';
        });
        
        selector.innerHTML = options;
      });
    }
  
    function handleModelSelection(e) {
      var selectedModel = e.target.value;
      if (selectedModel) {
        // Update URL and reload model
        var newUrl = window.location.pathname + '?model=' + encodeURIComponent(selectedModel);
        window.history.pushState({}, '', newUrl);
        modelName = selectedModel;
        initializeModel();
      }
    }
  
    function initializeModel() {
      var url = window.SITE_CONFIG.baseUrl + '/_resources/models/StructureDefinition-' + modelName + '.json';
      
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
      
      // Update page title
      document.getElementById('modelTitle').innerHTML = '<h1>' + escapeHtml(sd.title || sd.name || modelName) + '</h1>';
      document.title = (sd.title || sd.name || modelName) + ' - Model Viewer';
      
      // Display description
      if (sd.description) {
        document.getElementById('modelDescription').innerHTML = '<p>' + escapeHtml(sd.description) + '</p>';
      }
      
      // Display metadata
      renderMetadata(sd);
      
      // Display elements
      var elements = sd.snapshot && sd.snapshot.element ? sd.snapshot.element : (sd.differential && sd.differential.element ? sd.differential.element : null);
      if (!elements || !Array.isArray(elements)) {
        showError('No elements found in snapshot or differential');
        return;
      }
      
      renderElements(elements);
    }
  
    function renderMetadata(sd) {
      var metadata = [
        { label: 'URL', value: sd.url },
        { label: 'Version', value: sd.version },
        { label: 'Status', value: sd.status },
        { label: 'Date', value: sd.date },
        { label: 'Publisher', value: sd.publisher },
        { label: 'Kind', value: sd.kind },
        { label: 'Abstract', value: sd.abstract ? 'Yes' : 'No' },
        { label: 'Type', value: sd.type },
        { label: 'Base Definition', value: sd.baseDefinition }
      ];
      
      var tbody = '';
      metadata.forEach(function(item) {
        if (item.value) {
          var displayValue = item.value.toString();
          
          // Format date to show only date part (no time)
          if (item.label === 'Date' && displayValue.indexOf('T') > -1) {
            displayValue = displayValue.split('T')[0];
          }
          
          // Handle long URLs
          var tdStyle = 'padding: 8px; border: 1px solid #ddd;';
          if (item.label === 'URL' || item.label === 'Base Definition') {
            tdStyle += ' word-break: break-all; max-width: 500px;';
          }
          
          tbody += '<tr><td style="padding: 8px; border: 1px solid #ddd; font-weight: bold; width: 200px;">' + 
                   escapeHtml(item.label) + 
                   '</td><td style="' + tdStyle + '">' + 
                   escapeHtml(displayValue) + 
                   '</td></tr>';
        }
      });
      
      document.querySelector('#metadataTable tbody').innerHTML = tbody;
    }
  
    function renderElements(elements) {
      var hierarchy = buildHierarchy(elements);
      var tableBody = renderHierarchy(hierarchy, 0);
      
      document.querySelector('#elementsTable tbody').innerHTML = tableBody;
      
      dataTable = $('#elementsTable').DataTable({
        pageLength: 50,
        paging: false,
        ordering: false,
        searching: true,
        info: false,
        dom: 'Bfrt',
        buttons: [
          {
            extend: 'excelHtml5',
            text: 'Excel',
            filename: 'model-' + modelName,
            className: 'hidden-button',
            exportOptions: { columns: ':visible' }
          },
          {
            extend: 'pdfHtml5',
            text: 'PDF',
            filename: 'model-' + modelName,
            title: structureDefinition && structureDefinition.title ? structureDefinition.title : modelName,
            className: 'hidden-button',
            orientation: 'landscape',
            pageSize: 'A4',
            exportOptions: { columns: ':visible' }
          },
          {
            extend: 'csvHtml5',
            text: 'CSV',
            filename: 'model-' + modelName,
            className: 'hidden-button',
            exportOptions: { columns: ':visible' }
          }
        ]
      });
      
      $('.dt-buttons').hide();
      
      $('.toggle-children').on('click', function(e) {
        e.preventDefault();
        var elementPath = $(this).data('path');
        toggleChildren(elementPath);
      });
      
      // Expand tree by default
      expandAll();
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
      
      var card = (element.min || '0') + '..' + (element.max || '*');
      
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
      
      var description = element.short || element.definition || '';
      
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
      
      var indent = depth * 20;
      var hasChildren = item.children.length > 0;
      var expandIcon = hasChildren ? 
        '<span class="toggle-children" data-path="' + escapeAttr(path) + '" style="cursor: pointer; margin-right: 5px;">▼</span>' : 
        '<span style="margin-right: 5px; visibility: hidden;">▼</span>';
      
      var elementCell = '<div style="padding-left: ' + indent + 'px;">' + 
                        expandIcon + 
                        '<span class="element-name" style="font-family: monospace; font-weight: ' + (depth === 0 ? 'bold' : 'normal') + ';">' + 
                        escapeHtml(name) + 
                        '</span></div>';
      
      var rowClass = 'element-row depth-' + depth + ' path-' + path.replace(/\./g, '-');
      if (depth > 0) {
        rowClass += ' child-row';
      }
      
      return '<tr class="' + rowClass + '" data-path="' + escapeAttr(path) + '" data-depth="' + depth + '">' +
             '<td>' + elementCell + '</td>' +
             '<td>' + escapeHtml(card) + '</td>' +
             '<td>' + escapeHtml(typeStr) + '</td>' +
             '<td>' + escapeHtml(description) + '</td>' +
             '<td>' + escapeHtml(binding) + '</td>' +
             '</tr>';
    }
  
    function toggleChildren(parentPath) {
      var icon = $('.toggle-children[data-path="' + parentPath.replace(/\./g, '\\.') + '"]');
      var isExpanded = icon.text() === '▼';
      
      var childRows = $('tr[data-path^="' + parentPath + '."]');
      
      if (isExpanded) {
        icon.text('▶');
        childRows.hide();
      } else {
        icon.text('▼');
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
      $('.element-row').show();
    }
  
    function collapseAll() {
      $('.toggle-children').text('▶');
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
        '<tr><td colspan="5" style="text-align:center; color: red;">' +
        '<b>Error loading model</b><br><br>' +
        escapeHtml(message) + '<br><br>' +
        'Model: ' + escapeHtml(modelName) +
        '</td></tr>';
    }
  
    function handleDownload(e) {
      e.preventDefault();
      
      if (!dataTable) {
        alert('Table not initialized yet. Please wait.');
        return;
      }
      
      var format = document.getElementById('downloadFormat').value;
      var fileName = 'model-' + modelName;
      
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
      content.push('# ' + (structureDefinition && structureDefinition.title ? structureDefinition.title : modelName));
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
      content.push('| Element | Card. | Type | Description | Binding |');
      content.push('|---------|-------|------|-------------|---------|');
      
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