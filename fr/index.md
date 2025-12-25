---
layout: default
title: Home
has_children: true
nav_order: 1
lang: fr
---

# Bienvenue dans CareSets

## Qu'est-ce qu'un CareSet?

Un **CareSet** est une collection standardisée de modèles de données logiques conçus pour faciliter l'interopérabilité et l'échange de données dans l'écosystème des soins de santé belge. Chaque CareSet définit un domaine ou un cas d'utilisation spécifique dans les soins de santé, fournissant une structure cohérente pour capturer, partager et analyser les informations de santé.

### Caractéristiques clés

**Modèles standardisés**: Les CareSets utilisent des modèles logiques basés sur FHIR qui définissent la structure et la sémantique des données de santé de manière standardisée.

**Spécifiques au domaine**: Chaque CareSet se concentre sur un domaine de soins de santé spécifique (par exemple, observations, médicaments, plans de soins) pour garantir la pertinence et l'applicabilité pratique.

**Interopérables**: Construits sur des normes internationales (FHIR) tout en intégrant les exigences et la terminologie spécifiques à la Belgique.

**Réutilisables**: Les éléments de données et les modèles communs sont conçus pour être réutilisés dans plusieurs CareSets, favorisant la cohérence et réduisant la redondance.

### Objectif

Les CareSets visent à:

- **Améliorer la qualité des données** en fournissant des définitions claires et non ambiguës des éléments de données de santé
- **Permettre l'interopérabilité sémantique** entre différents systèmes informatiques de santé
- **Soutenir la prise de décision clinique** grâce à des données standardisées et comparables
- **Faciliter l'analyse et la recherche de données** en garantissant une capture de données cohérente
- **Réduire la charge de mise en œuvre** en fournissant des modèles prêts à l'emploi et validés

### Structure

Chaque CareSet contient:

- **Modèles de données logiques**: StructureDefinitions FHIR qui définissent la structure des données
- **Liaisons terminologiques**: Liens vers des systèmes de codes standard (SNOMED CT, LOINC, etc.)
- **Glossaire**: Définitions des concepts et termes clés utilisés dans le CareSet
- **Documentation**: Directives d'utilisation, exemples et conseils de mise en œuvre

Parcourez les [Modèles de données logiques](logical-data-models) pour explorer les CareSets disponibles, ou consultez la [Feuille de route](roadmap) pour voir ce qui arrive ensuite.

```plantuml!
@startuml

'skinparam linetype ortho
skinparam linetype polyline
hide circle
hide stereotype
hide methods


skinparam class<<BU>> {
 BorderColor #909050
 BackgroundColor BUSINESS
 HeaderBackgroundColor #dd4
}

Package "Glossary" as glossary {

class "**Glossary**" as G<<BU>> {
  |_ title 1..1
  |_ notes 1..1   
  |_ date 1..1
  |_ scope 1..1
  |_ status 1..1
  |_ owner 1..1
  |_ concept 1..*   
}

class "**Concept**" as C<<BU>> {
  |_ code 1..1
  |_ designation 1..*  
  |_ definition 1..1
  |_ description 0..1
  |_ status 1..1
  |_ owner 1..1
  |_ source 0..1    
}

C - C : "Related to:\n - is-a     \n - part-of\n - has-a  \n ...     "

}
G *-r- C:  "            "  
@enduml

```


