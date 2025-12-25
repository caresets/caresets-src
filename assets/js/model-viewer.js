(function() {
    var structureDefinition = null;
    var dataTable = null;
    var modelName = null;
    var targetElementPath = null;
    var modelsMap = {}; // Map of URL -> {name, file, title}

    // Glossary configuration - read from data attributes set by Jekyll in HTML
    function getGlossaryConfig() {
      // Default values
      var config = {
        system: 'http://example.org/CodeSystem/BeSafeShareGlossary',
        page: 'glossary_official'
      };

      // Try to read from data attributes in this order:
      // 1. body element
      // 2. main element
      // 3. any element with .model-viewer class
      // 4. any element with #model-viewer id

      var sources = [
        document.body,
        document.querySelector('main'),
        document.querySelector('.model-viewer'),
        document.getElementById('modelViewerMain'),
        document.querySelector('[data-glossary-system]') // Any element with the attribute
      ];

      for (var i = 0; i < sources.length; i++) {
        var element = sources[i];
        if (element && element.dataset && element.dataset.glossarySystem) {
          config.system = element.dataset.glossarySystem;
          config.page = element.dataset.glossaryPage || config.page;
          break;
        }
      }

      return config;
    }

    // Get current language from URL path (e.g., /en/, /fr/, etc.)
    function getCurrentLanguage() {
      var pathParts = window.location.pathname.split('/').filter(function(p) { return p !== ''; });
      // Assume first part is language code if it's 2-3 characters
      if (pathParts.length > 0 && pathParts[0].length >= 2 && pathParts[0].length <= 3) {
        return pathParts[0];
      }
      return 'en';  // Default to English
    }

    // Extract translated text from FHIR translation extension
    // element: the FHIR element (e.g., from snapshot.element[])
    // field: the field name (e.g., 'short', 'definition')
    // Returns: translated text if available, or the default text
    function getTranslatedText(element, field) {
      if (!element) return '';

      var defaultText = element[field] || '';
      var currentLang = getCurrentLanguage();

      // If current language is English or no translation field exists, return default
      if (currentLang === 'en' || !element['_' + field]) {
        return defaultText;
      }

      // Look for translation extension
      var translationField = element['_' + field];
      if (translationField && translationField.extension) {
        // Find translation for current language
        for (var i = 0; i < translationField.extension.length; i++) {
          var ext = translationField.extension[i];
          if (ext.url === 'http://hl7.org/fhir/StructureDefinition/translation' && ext.extension) {
            var lang = null;
            var content = null;

            // Extract lang and content from nested extensions
            for (var j = 0; j < ext.extension.length; j++) {
              var subExt = ext.extension[j];
              if (subExt.url === 'lang') {
                lang = subExt.valueCode || subExt.valueString;
              } else if (subExt.url === 'content') {
                content = subExt.valueString;
              }
            }

            // If we found a matching language, return the translated content
            if (lang === currentLang && content) {
              return content;
            }
          }
        }
      }

      // No translation found, return default
      return defaultText;
    }

    // Build glossary URL relative to current site and language
    function getGlossaryUrl(conceptCode) {
      var config = getGlossaryConfig();
      var baseUrl = window.SITE_CONFIG && window.SITE_CONFIG.baseUrl ? window.SITE_CONFIG.baseUrl : '';
      var language = getCurrentLanguage();
      return baseUrl + '/' + language + '/' + config.page + '#' + conceptCode;
    }

    document.addEventListener('DOMContentLoaded', function() {
      // Get model name from URL parameter
      var urlParams = new URLSearchParams(window.location.search);
      modelName = urlParams.get('model');

      // Get element path from URL fragment (e.g., #Patient.identifier)
      if (window.location.hash) {
        targetElementPath = window.location.hash.substring(1); // Remove the #
        console.log('Target element path from URL:', targetElementPath);
      }

      // Load available models for dropdown, then initialize if we have a model
      loadModelsList().then(function() {
        if (modelName) {
          initializeModel();
        } else {
          document.getElementById('modelTitle').innerHTML = '<h1>Select a model from the dropdown above</h1>';
        }
      });

      document.getElementById('expandAllBtn').addEventListener('click', expandAll);
      document.getElementById('collapseAllBtn').addEventListener('click', collapseAll);
      document.getElementById('downloadBtn').addEventListener('click', handleDownload);
      document.getElementById('modelSelector').addEventListener('change', handleModelSelection);
    });
  
    function loadModelsList() {
      var manifestUrl = window.SITE_CONFIG.baseUrl + '/_resources/models-manifest.json';

      return fetch(manifestUrl)
        .then(function(response) {
          if (!response.ok) {
            throw new Error('Manifest not found');
          }
          return response.json();
        })
        .then(function(manifest) {
          return populateModelSelector(manifest.models || []);
        })
        .catch(function(error) {
          console.log('No manifest found, trying fallback');
          // Fallback: try to use a pre-generated list if available
          var modelFiles = window.SITE_CONFIG.modelFiles || [];
          return populateModelSelector(modelFiles);
        });
    }
  
    function populateModelSelector(modelFiles) {
      var selector = document.getElementById('modelSelector');

      if (modelFiles.length === 0) {
        selector.innerHTML = '<option value="">No models available</option>';
        return Promise.resolve();
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
            // Store model in map by URL
            if (data.url) {
              modelsMap[data.url] = {
                file: fileName,
                name: data.name || fileName,
                title: data.title || data.name || fileName
              };
            }
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

      return Promise.all(promises).then(function(models) {
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
      
      // Update page title with translated text
      var title = getTranslatedText(sd, 'title') || sd.name || modelName;
      document.getElementById('modelTitle').innerHTML = '<h1>' + escapeHtml(title) + '</h1>';
      document.title = title + ' - Model Viewer';

      // Display description with translated text
      var description = getTranslatedText(sd, 'description');
      if (description) {
        document.getElementById('modelDescription').innerHTML = '<p>' + escapeHtml(description) + '</p>';
      }
      
      // Display metadata
      renderMetadata(sd);

      // Load and display custom markdown content for this model
      loadModelDocumentation(sd);

      // Display elements
      var elements = sd.snapshot && sd.snapshot.element ? sd.snapshot.element : (sd.differential && sd.differential.element ? sd.differential.element : null);
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
                 '<td style="padding: 6px; border: 1px solid #ddd; word-break: break-all;" colspan="5">' + escapeHtml(sd.url) + '</td></tr>';
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
        var dateValue = sd.date.toString();
        // Format date to show only date part (no time)
        if (dateValue.indexOf('T') > -1) {
          dateValue = dateValue.split('T')[0];
        }
        tbody += '<td style="padding: 6px; border: 1px solid #ddd; font-weight: bold; width: 150px;">Date</td>' +
                 '<td style="padding: 6px; border: 1px solid #ddd;">' + escapeHtml(dateValue) + '</td>';
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

    // Load custom markdown documentation for a model
    // Looks for files like: StructureDefinition-be-model-bodysite.md
    // With language support: StructureDefinition-be-model-bodysite-fr.md or fr/StructureDefinition-be-model-bodysite.md
    function loadModelDocumentation(sd) {
      if (!sd || !sd.id) return;

      var baseUrl = window.SITE_CONFIG && window.SITE_CONFIG.baseUrl ? window.SITE_CONFIG.baseUrl : '';
      var currentLang = getCurrentLanguage();
      var modelType = sd.resourceType || 'StructureDefinition';
      var modelId = sd.id;

      // Build possible documentation file paths (try language-specific first, then default)
      var paths = [
        baseUrl + '/_resources/model-docs/' + currentLang + '/' + modelType + '-' + modelId + '.md',
        baseUrl + '/_resources/model-docs/' + modelType + '-' + modelId + '-' + currentLang + '.md',
        baseUrl + '/_resources/model-docs/' + modelType + '-' + modelId + '.md'
      ];

      // Try each path until we find one that works
      function tryNextPath(index) {
        if (index >= paths.length) {
          // No documentation found, that's okay
          return;
        }

        fetch(paths[index])
          .then(function(response) {
            if (!response.ok) {
              throw new Error('Not found');
            }
            return response.text();
          })
          .then(function(markdown) {
            displayModelDocumentation(markdown);
          })
          .catch(function() {
            // Try next path
            tryNextPath(index + 1);
          });
      }

      tryNextPath(0);
    }

    // Display model documentation as HTML
    function displayModelDocumentation(markdown) {
      var container = document.getElementById('modelDocumentation');
      if (!container) {
        // Create container if it doesn't exist
        var metadataTable = document.getElementById('metadataTable');
        if (metadataTable && metadataTable.parentNode) {
          container = document.createElement('div');
          container.id = 'modelDocumentation';
          container.style.marginTop = '20px';
          container.style.marginBottom = '20px';
          container.style.padding = '15px';
          container.style.background = '#f8f9fa';
          container.style.borderRadius = '6px';
          container.style.borderLeft = '4px solid #5c5962';
          metadataTable.parentNode.insertBefore(container, metadataTable.nextSibling);
        }
      }

      if (container) {
        // Simple markdown-to-HTML conversion (basic support)
        var html = convertMarkdownToHtml(markdown);
        container.innerHTML = html;
        container.style.display = 'block';
      }
    }

    // Basic markdown to HTML converter
    function convertMarkdownToHtml(markdown) {
      var html = markdown;

      // Headers
      html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
      html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
      html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

      // Bold
      html = html.replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>');

      // Italic
      html = html.replace(/\*(.*?)\*/gim, '<em>$1</em>');

      // Links
      html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/gim, '<a href="$2">$1</a>');

      // Line breaks
      html = html.replace(/\n\n/gim, '</p><p>');
      html = '<p>' + html + '</p>';

      // Lists (simple)
      html = html.replace(/<p>- (.*?)<\/p>/gim, '<ul><li>$1</li></ul>');

      return html;
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
        autoWidth: false,
        dom: 'Bfrt',
        drawCallback: function() {
          // After any draw, reapply highlight if we have a target path
          if (targetElementPath) {
            applyHighlight();
          }
        },
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
            title: getTranslatedText(structureDefinition, 'title') || structureDefinition.name || modelName,
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

      // Apply vertical line backgrounds
      applyVerticalLineBackgrounds();

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
  
    function applyVerticalLineBackgrounds() {
      $('#elementsTable tbody td.element-col').each(function() {
        var $cell = $(this);
        var vlines = $cell.data('vlines');
        
        if (vlines && vlines !== '') {
          var levels = vlines.toString().split(',').filter(function(v) { return v !== ''; });
          
          if (levels.length > 0) {
            // Cell has 8px left padding, need to account for that
            var cellPadding = 8;
            
            // Build multiple background gradients for vertical lines
            var backgrounds = levels.map(function(level) {
              // Line should be at parent's connector position (one level to the left)
              // Parent's connector is at (level - 1) * 20 from content start
              // Add spacing to move the children's line to the right
              var pos = ((parseInt(level) - 1) * 20) + cellPadding + 0; // vertical line position with extra spacing to align with parent
              // Create a 2px wide vertical line using horizontal gradient
              return 'linear-gradient(to right, transparent ' + pos + 'px, #999 ' + pos + 'px, #999 ' + (pos + 2) + 'px, transparent ' + (pos + 2) + 'px)';
            });
            
            // Apply all backgrounds - will fill full cell height automatically
            $cell.css({
              'background-image': backgrounds.join(', '),
              'background-size': '100% 100%',
              'background-repeat': 'no-repeat'
            });
          }
        }
      });
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
      var hasHtmlInTypes = false;
      if (element.type && Array.isArray(element.type)) {
        types = element.type.map(function(t) {
          var typeStr = t.code || '';

          // Check if the code itself is a URL pointing to a model in our collection
          if (typeStr && modelsMap[typeStr]) {
            var modelInfo = modelsMap[typeStr];
            var modelViewerUrl = window.location.pathname + '?model=' + encodeURIComponent(modelInfo.file);
            typeStr = '<a href="' + escapeAttr(modelViewerUrl) + '" title="View ' + escapeAttr(modelInfo.title) + ' model">' +
                      escapeHtml(modelInfo.name) + '</a>';
            hasHtmlInTypes = true;
            return typeStr;
          }

          // Check for targetProfile (for Reference types)
          if (t.targetProfile && t.targetProfile.length > 0) {
            var targetUrl = t.targetProfile[0];
            var modelInfo = modelsMap[targetUrl];

            if (modelInfo) {
              // Create a link to the model viewer for this target
              var modelViewerUrl = window.location.pathname + '?model=' + encodeURIComponent(modelInfo.file);
              typeStr = '<a href="' + escapeAttr(modelViewerUrl) + '" title="View ' + escapeAttr(modelInfo.title) + ' model">' +
                        escapeHtml(modelInfo.name) + '</a>';
              hasHtmlInTypes = true;
            } else {
              // Target model not found in our models, show the URL fragment
              typeStr += ' (' + targetUrl.split('/').pop() + ')';
            }
          } else if (t.profile && t.profile.length > 0) {
            // Check if profile URL is in our models map
            var profileUrl = t.profile[0];
            var modelInfo = modelsMap[profileUrl];

            if (modelInfo) {
              // Create a link to the model viewer for this profile
              var modelViewerUrl = window.location.pathname + '?model=' + encodeURIComponent(modelInfo.file);
              typeStr = '<a href="' + escapeAttr(modelViewerUrl) + '" title="View ' + escapeAttr(modelInfo.title) + ' model">' +
                        escapeHtml(modelInfo.name) + '</a>';
              hasHtmlInTypes = true;
            } else {
              // Profile not found in our models, show the URL fragment
              typeStr += ' (' + profileUrl.split('/').pop() + ')';
            }
          }

          return typeStr;
        });
      }
      var typeStr = types.join(', ') || (element.contentReference ? 'See ' + element.contentReference : '');

      // Get translated description based on current language
      var description = getTranslatedText(element, 'short') || getTranslatedText(element, 'definition') || '';

      // Check for glossary concept
      var glossary = '';
      if (element.code && Array.isArray(element.code)) {
        var config = getGlossaryConfig();
        element.code.forEach(function(coding) {
          if (coding.system === config.system && coding.code) {
            var display = coding.display || coding.code;
            var conceptUrl = getGlossaryUrl(coding.code);
            glossary = '<a href="' + escapeAttr(conceptUrl) + '" target="_blank" rel="noopener noreferrer">' +
                       escapeHtml(display) + '</a>';
          }
        });
      }

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
      
      // Determine if this is the last child of its parent
      var isLastChild = false;
      if (item.parent) {
        var siblings = item.parent.children;
        isLastChild = siblings[siblings.length - 1] === item;
      }
      
      // Build list of ancestor levels that need vertical lines
      var verticalLineLevels = [];
      var currentItem = item.parent;
      var currentDepth = depth - 1;
      
      while (currentItem && currentDepth > 0) {
        var ancestorIsLast = false;
        if (currentItem.parent) {
          var ancestorSiblings = currentItem.parent.children;
          ancestorIsLast = ancestorSiblings[ancestorSiblings.length - 1] === currentItem;
        }
        
        if (!ancestorIsLast) {
          verticalLineLevels.push(currentDepth);
        }
        
        currentItem = currentItem.parent;
        currentDepth--;
      }
      
      var expandIcon = hasChildren ? 
        '<span class="toggle-children" data-path="' + escapeAttr(path) + '" style="cursor: pointer; margin-right: 5px; position: relative; left: -5px; top: 2px;">▼</span>' : 
        '<span style="margin-right: 5px; visibility: hidden; width: 16px; display: inline-block;"></span>';
      
      // Build connector for this element - positioned relative to td cell (accounting for cell padding)
      var connectorHtml = '';
      if (depth > 0) {
        // Position relative to td cell, accounting for 8px cell padding
        var connectorLeft = ((depth - 1) * 20) + 8;
        var connectorClass = isLastChild ? 'tree-corner' : 'tree-branch';
        connectorHtml = '<span class="tree-connector ' + connectorClass + '" style="position: absolute; left: ' + connectorLeft + 'px; top: 0; bottom: 0; width: 20px; height: 100%; z-index: 1;"></span>';
      }
      
      var elementCell = '<div class="element-cell" style="padding-left: ' + indent + 'px; position: relative; min-height: 20px; z-index: 2;">' +
                        '<div style="position: relative; display: flex; align-items: center;">' +
                        expandIcon +
                        '<span class="element-name" style="font-family: monospace; font-weight: ' + (depth === 0 ? 'bold' : 'normal') + ';">' +
                        escapeHtml(name) +
                        '</span></div></div>';
      
      var rowClass = 'element-row depth-' + depth + ' path-' + path.replace(/\./g, '-');
      if (depth > 0) {
        rowClass += ' child-row';
      }
      if (hasChildren) {
        rowClass += ' has-children';
      }
      
      // Store vertical line levels as data attribute
      var vlineData = verticalLineLevels.join(',');

      return '<tr class="' + rowClass + '" data-path="' + escapeAttr(path) + '" data-depth="' + depth + '" data-vlines="' + vlineData + '" style="--parent-indent: ' + indent + 'px;">' +
             '<td class="element-col" data-vlines="' + vlineData + '" style="position: relative;">' + connectorHtml + elementCell + '</td>' +
             '<td>' + escapeHtml(card) + '</td>' +
             '<td>' + (hasHtmlInTypes ? typeStr : escapeHtml(typeStr)) + '</td>' +
             '<td>' + escapeHtml(description) + '</td>' +
             '<td>' + glossary + '</td>' +
             '<td>' + escapeHtml(binding) + '</td>' +
             '</tr>';
    }
  
    function toggleChildren(parentPath) {
      var icon = $('.toggle-children[data-path="' + parentPath.replace(/\./g, '\\.') + '"]');
      var parentRow = icon.closest('tr');
      var isExpanded = icon.text() === '▼';

      var childRows = $('tr[data-path^="' + parentPath + '."]');

      if (isExpanded) {
        icon.text('▶');
        parentRow.addClass('collapsed');
        childRows.hide();
      } else {
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
        '<tr><td colspan="6" style="text-align:center; color: red;">' +
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
      var title = getTranslatedText(structureDefinition, 'title') || structureDefinition.name || modelName;
      content.push('# ' + title);
      content.push('');

      var description = getTranslatedText(structureDefinition, 'description');
      if (description) {
        content.push(description);
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