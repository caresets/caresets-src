// Glossary download functionality
(function() {
    'use strict';
    
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', init);
    } else {
      init();
    }
    
    function init() {
      var downloadBtn = document.getElementById('downloadBtn');
      if (!downloadBtn) {
        console.warn('Download button not found');
        return;
      }
      
      downloadBtn.addEventListener('click', handleDownload);
      console.log('Download functionality initialized');
    }
    
    function handleDownload(e) {
      e.preventDefault();
      
      var languageSelect = document.getElementById('language');
      var formatSelect = document.getElementById('format');
      
      if (!languageSelect || !formatSelect) {
        console.error('Form elements not found');
        return;
      }
      
      var language = languageSelect.value;
      var format = formatSelect.value;
      
      // Get the current page name
      var pageUrl = window.location.pathname;
      var fileName = pageUrl.split('/').pop().replace(/\.html$/, '') || 'glossary';
      
      // Build download URL
      var downloadUrl = fileName + '-' + language + '.' + format;
      
      console.log('Downloading:', downloadUrl);
      
      // Try to download the file
      var link = document.createElement('a');
      link.href = downloadUrl;
      link.download = fileName + '-' + language + '.' + format;
      link.style.display = 'none';
      
      document.body.appendChild(link);
      link.click();
      
      // Clean up
      setTimeout(function() {
        document.body.removeChild(link);
      }, 100);
    }
  })();