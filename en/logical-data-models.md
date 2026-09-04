---
layout: default
title: Logical Data Models
nav_order: 3
has_children: true
lang: en
---


Logical models are abstract representations of data structures that define the information content without specifying how that content is technically implemented or exchanged. They serve as a bridge between business requirements and technical implementation.

Unlike FHIR profiles (which constrain existing FHIR resources), logical models define completely custom structures that represent domain-specific concepts. They are particularly useful for:

- **Documenting requirements**: Capturing business and clinical requirements in a structured, computable format
- **Cross-paradigm modeling**: Defining structures that can be mapped to multiple implementation technologies (FHIR, CDA, database schemas, etc.)
- **Stakeholder communication**: Providing a technology-neutral view that clinical and business stakeholders can understand

---

## Binding to the glossary

Where an element of a model means something the glossary already defines, it
carries that concept's code. An element called *recorder* in one model, *author*
in another and *recorded by* in a third all point at the glossary term
**Recorder**, so they
are recognisably the same thing to a person reading the model and to software
reading it.

This is what makes a question like *who is the recorder of any CareSet?*
answerable once across every model, rather than model by model. It also lets a
rule about retention, consent or access be written against the concept and hold
wherever the concept appears — see
[why a shared glossary matters](glossary.html#why-a-shared-glossary-matters).

Not every element maps. Many are specific to one model and correctly have no
glossary concept; an element with no code is not an omission.

---
