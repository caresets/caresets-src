---
layout: glossary
title: Statut du concept
parent: Glossaire
nav_order: 3
lang: fr
CodeSystem: "glossary-status"
---

Un concept du glossaire passe par les états de cycle de vie suivants :

@startuml
left to right direction
hide empty description
state accepted
[*] -r-> draft : créé
draft -r-> proposed : soumis pour revue
proposed -l-> draft : révisions demandées
proposed -r-> accepted : approuvé par la gouvernance
accepted -r-> deprecated : retiré
deprecated -r-> [*]
@enduml

Cliquez sur un statut dans les tableaux du glossaire principal pour revenir ici.
