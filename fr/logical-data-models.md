---
layout: default
title: Modèles de données logiques
nav_order: 3
has_children: true
lang: fr
---

# Modèles de données logiques

## Qu'est-ce qu'un modèle logique ?

Les modèles logiques en FHIR sont des représentations abstraites de structures de données qui définissent le contenu informationnel sans spécifier comment ce contenu est techniquement implémenté ou échangé. Ils servent de pont entre les exigences métier et l'implémentation technique.

Contrairement aux profils FHIR (qui contraignent des ressources FHIR existantes), les modèles logiques définissent des structures entièrement personnalisées qui représentent des concepts spécifiques au domaine. Ils sont particulièrement utiles pour :

- **Documenter les exigences** : Capturer les exigences métier et cliniques dans un format structuré et calculable
- **Modélisation multi-paradigme** : Définir des structures qui peuvent être mappées vers plusieurs technologies d'implémentation (FHIR, CDA, schémas de base de données, etc.)
- **Communication avec les parties prenantes** : Fournir une vue technologiquement neutre que les parties prenantes cliniques et métier peuvent comprendre

Pour plus de détails, voir la [spécification des modèles logiques FHIR](https://hl7.org/fhir/R4/structuredefinition.html#logical).

## Les modèles logiques comme types de données ou ancêtres

Une fonctionnalité puissante des modèles logiques FHIR est leur capacité à référencer d'autres modèles logiques de deux manières :

### Comme types de données

Un modèle logique peut utiliser un autre modèle logique comme type de données pour ses éléments. Cela permet la **composition** - construire des modèles complexes à partir de blocs de construction plus simples et réutilisables.

Par exemple, un modèle `Vaccination` pourrait utiliser un modèle `BodySite` comme type pour son élément `site`, plutôt que de définir les champs de localisation corporelle en ligne.

### Comme ancêtres (Spécialisation)

Un modèle logique peut étendre un autre modèle logique comme parent. Cela crée une relation de **spécialisation** où le modèle enfant hérite de tous les éléments du parent et peut en ajouter de nouveaux.

**Important** : Contrairement aux profils FHIR, l'héritage des modèles logiques représente une **spécialisation, pas une contrainte**. Le modèle enfant étend la structure du parent plutôt que de la restreindre. Cela signifie :

- Les modèles enfants peuvent ajouter de nouveaux éléments obligatoires
- Les modèles enfants peuvent étendre la cardinalité des éléments hérités
- Les modèles enfants représentent un concept plus spécifique, pas une vue restreinte

Cette distinction est cruciale : les profils contraignent les ressources pour des cas d'utilisation spécifiques, tandis que l'héritage des modèles logiques étend les définitions pour des domaines spécialisés.

---
