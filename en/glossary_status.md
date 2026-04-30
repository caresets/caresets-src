---
layout: glossary
title: Concept Status
parent: Glossary
nav_order: 3
lang: en
CodeSystem: "glossary-status"
---

A glossary concept moves through the following lifecycle states:

@startuml
'left to right direction
hide empty description
state accepted #aec
[*] -r-> draft : created
draft -r-> proposed : submitted for review
proposed -l-> draft : revisions requested
proposed -r-> accepted : approved by governance
accepted -r-> deprecated : retired
deprecated -r-> [*]
@enduml

Click any status in the main glossary tables to jump back here.
