---
layout: default
title: Feuille de route
nav_order: 1
parent: Governance
lang: fr
---

# Feuille de route des CareSets

Cette feuille de route décrit l'état actuel et le développement planifié des CareSets. Chaque CareSet représente une collection de modèles de données logiques spécifiques à un domaine.

## Définitions des statuts

- **Published**: Disponible à l'utilisation, documenté et validé
- **In Progress**: Actuellement en cours de développement et de révision
- **Planned**: Planifié pour un développement futur

<div id="roadmapTableContainer" style="margin: 30px 0;">
  <table id="roadmapTable" class="display" style="width:100%;">
    <thead>
      <tr>
        <th>Nom du CareSet</th>
        <th>Statut</th>
        <th>Description</th>
        <th>Date cible</th>
        <th>Priorité</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td colspan="5" style="text-align: center; padding: 40px; color: #666;">
          Chargement des données de la feuille de route...
        </td>
      </tr>
    </tbody>
  </table>
</div>

<script type="text/javascript" src="{{ site.baseurl }}/assets/js/roadmap-loader.js"></script>

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
