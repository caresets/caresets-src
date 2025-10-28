---
layout: glossary
title: Glossary
parent: Home
lang: fr
nav_order: 1

CodeSystem: "example"  # The dynamic part of the file name
#permalink: /en/
---
<div>
<b>Download this glossary</b><br>
<form id="downloadForm">
  <label for="language">Language:</label>
  <select id="language">
    <option value="nl">Dutch (NL)</option>
    <option value="fr">French (FR)</option>
    <option value="en">English (EN)</option>
    <option value="de">German (DE)</option>
  </select>

  <label for="format">Format:</label>
  <select id="format">
    <option value="xls">Excel (XLS)</option>
    <option value="pdf">PDF</option>
  </select>

  <button type="button" onclick="downloadPage()">Download</button>
</form>
</div>
{: .info-box .may}


<script>
  function downloadPage() {
    var language = document.getElementById('language').value;
    var format = document.getElementById('format').value;
    var pageUrl = window.location.pathname.replace(/\.html$/, ''); // Remove .html if present
    var fileName = pageUrl.split('/').pop() || 'page'; // Get last part of the URL or use "page"

    var downloadUrl = `${fileName}-${language}.${format}`;
    
    // Simulate download (modify this to suit your actual download logic)
    window.location.href = downloadUrl;
  }
</script>

