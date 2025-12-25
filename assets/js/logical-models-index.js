(function() {
    var baseUrl = window.SITE_CONFIG.baseUrl + '/_resources/models/';
    var modelsUrl = window.SITE_CONFIG.baseUrl + '/_resources/models/';
    var dataTable = null;

    // Detect language from URL path or html lang attribute
    var currentLang = (function() {
      var path = window.location.pathname;
      var match = path.match(/\/(en|fr|nl)\//);
      if (match) return match[1];
      return document.documentElement.lang || 'en';
    })();

    // Translations
    var translations = {
      en: {
        noModelsTitle: 'No models found',
        noModelsText1: 'No StructureDefinition files were found in',
        noModelsText2: 'Add your StructureDefinition JSON files to that directory and they will automatically appear here.'
      },
      fr: {
        noModelsTitle: 'Aucun modèle trouvé',
        noModelsText1: 'Aucun fichier StructureDefinition n\'a été trouvé dans',
        noModelsText2: 'Ajoutez vos fichiers JSON StructureDefinition dans ce répertoire et ils apparaîtront automatiquement ici.'
      },
      nl: {
        noModelsTitle: 'Geen modellen gevonden',
        noModelsText1: 'Geen StructureDefinition-bestanden gevonden in',
        noModelsText2: 'Voeg uw StructureDefinition JSON-bestanden toe aan die map en ze verschijnen automatisch hier.'
      }
    };

    var t = translations[currentLang] || translations.en;

    document.addEventListener('DOMContentLoaded', function() {
      discoverAndLoadModels();
    });
  
    function discoverAndLoadModels() {
      // Fetch the directory listing or manifest
      // Since we can't list directory contents directly in browser,
      // we'll try to load a models-manifest.json file
      var manifestUrl = window.SITE_CONFIG.baseUrl + '/_resources/models-manifest.json';
      
      fetch(manifestUrl)
        .then(function(response) {
          if (!response.ok) {
            throw new Error('Manifest not found. Using fallback discovery.');
          }
          return response.json();
        })
        .then(function(manifest) {
          loadModelsFromManifest(manifest.models);
        })
        .catch(function(error) {
          console.log('No manifest found, using Jekyll-generated list');
          // Fallback: use Jekyll to generate the list at build time
          loadModelsFromJekyllList();
        });
    }
  
    function loadModelsFromManifest(modelList) {
      var promises = modelList.map(function(modelFile) {
        var url = baseUrl + modelFile;
        return fetch(url)
          .then(function(response) {
            if (!response.ok) {
              throw new Error('Failed to load ' + modelFile);
            }
            return response.json();
          })
          .then(function(data) {
            return {
              file: modelFile.replace('StructureDefinition-', '').replace('.json', ''),
              title: data.title || data.name || modelFile,
              data: data
            };
          })
          .catch(function(error) {
            console.error('Error loading model:', modelFile, error);
            return null;
          });
      });
  
      Promise.all(promises).then(function(models) {
        var validModels = models.filter(function(m) { return m !== null; });
        renderModels(validModels);
      });
    }
  
    function loadModelsFromJekyllList() {
      // Jekyll will generate this list at build time
      var modelFiles = window.SITE_CONFIG.modelFiles || [];
  
      if (modelFiles.length === 0) {
        showNoModelsMessage();
        return;
      }
  
      loadModelsFromManifest(modelFiles);
    }
  
    function renderModels(models) {
      if (models.length === 0) {
        showNoModelsMessage();
        return;
      }
  
      // Sort models alphabetically by title
      models.sort(function(a, b) {
        return a.title.localeCompare(b.title);
      });
  
      var tableData = models.map(function(model) {
        return modelToTableRow(model);
      });
  
      // Destroy existing DataTable if it exists
      if (dataTable) {
        dataTable.destroy();
      }
  
      // Clear loading message and populate table
      var tbody = document.querySelector('#modelsTable tbody');
      tbody.innerHTML = '';
      
      tableData.forEach(function(rowData) {
        var row = tbody.insertRow();
        rowData.forEach(function(cellData) {
          var cell = row.insertCell();
          cell.innerHTML = cellData;
        });
      });
  
      // Initialize DataTable
      dataTable = $('#modelsTable').DataTable({
        pageLength: 25,
        order: [[0, 'asc']], // Sort by title
        columnDefs: [
          { width: '25%', targets: 0 }, // Title
          { width: '8%', targets: 1 },  // Status
          { width: '35%', targets: 2 }, // Description
          { width: '8%', targets: 3 },  // Version
          { width: '10%', targets: 4 }, // Date
          { width: '14%', targets: 5 }  // URL
        ]
      });
    }
  
    function modelToTableRow(model) {
      var sd = model.data;
      
      // Format date to show only date part (no time)
      var dateStr = sd.date || '';
      if (dateStr && dateStr.indexOf('T') > -1) {
        dateStr = dateStr.split('T')[0];
      }
  
      var pageUrl = window.SITE_CONFIG.baseUrl + '/' + currentLang + '/model-viewer/?model=' + encodeURIComponent(model.file);
      
      // Title with link
      var titleHtml = '<a href="' + pageUrl + '" style="color: #0366d6; text-decoration: none; font-weight: 500;">' + 
                      escapeHtml(model.title) + '</a>';
      
      // Status badge
      var statusClass = getStatusClass(sd.status);
      var statusHtml = '<span class="status-badge status-' + statusClass + '" style="display: inline-block; padding: 3px 8px; border-radius: 3px; font-size: 0.8em; font-weight: bold; white-space: nowrap;">' + 
                       escapeHtml((sd.status || 'unknown').toUpperCase()) + 
                       '</span>';
      
      // Description (truncated)
      var description = sd.description || '';
      if (description.length > 100) {
        description = description.substring(0, 100) + '...';
      }
      
      // Version
      var version = sd.version || '';
      
      // URL (clickable, truncated display)
      var urlHtml = '';
      if (sd.url) {
        var displayUrl = sd.url;
        if (displayUrl.length > 40) {
          displayUrl = displayUrl.substring(0, 37) + '...';
        }
        urlHtml = '<a href="' + escapeHtml(sd.url) + '" target="_blank" style="color: #0366d6; text-decoration: none; font-size: 0.85em;" title="' + escapeHtml(sd.url) + '">' + 
                  escapeHtml(displayUrl) + '</a>';
      }
      
      return [
        titleHtml,
        statusHtml,
        escapeHtml(description),
        escapeHtml(version),
        escapeHtml(dateStr),
        urlHtml
      ];
    }
  
    function showNoModelsMessage() {
      var tbody = document.querySelector('#modelsTable tbody');
      tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 40px;">' +
                        '<h3>' + t.noModelsTitle + '</h3>' +
                        '<p>' + t.noModelsText1 + ' <code>_resources/models/</code>.</p>' +
                        '<p>' + t.noModelsText2 + '</p>' +
                        '</td></tr>';
    }
  
    function getStatusClass(status) {
      if (!status) return 'unknown';
      switch (status.toLowerCase()) {
        case 'draft': return 'draft';
        case 'active': return 'active';
        case 'retired': return 'retired';
        default: return 'unknown';
      }
    }
  
    function escapeHtml(text) {
      if (!text) return '';
      var div = document.createElement('div');
      div.textContent = text.toString();
      return div.innerHTML;
    }
  })();