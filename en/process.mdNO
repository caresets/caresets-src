---
layout: default
title: Process
nav_order: 3
parent: Governance
lang: en
---

# Data Modeling Process
{: .no_toc }

- TOC
{:toc}

This page describes how CareSets logical data models are developed and maintained through a collaborative, iterative process that emphasizes reusability and consistency.

---

## Overview

The CareSet modeling process transforms stakeholder input into standardized, reusable data models. The process is cyclical: models evolve based on feedback, new use cases, and changing requirements.

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   Stakeholder Input  ──►  Analysis  ──►  Data Model Creation   │
│          ▲                                       │              │
│          │                                       ▼              │
│          └───────  Maintenance & Feedback  ◄─────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Stakeholder Input

Stakeholders provide input at multiple stages of the process:

### Upfront Input
Before modeling begins, we gather requirements from:
- **Domain experts**: Clinicians, healthcare professionals who understand the clinical context
- **Technical stakeholders**: System implementers, software vendors who will use the models
- **Standards bodies**: Organizations defining terminology and interoperability requirements
- **Policy makers**: Regulatory requirements and governance constraints

### Ongoing Input
During elaboration and maintenance:
- **Feedback on drafts**: Stakeholders review proposed models and definitions
- **Change requests**: New requirements or corrections to existing models
- **Implementation experience**: Real-world usage reveals gaps or improvements
- **Cross-domain insights**: Patterns discovered in one CareSet may apply to others

---

## Analysis Phase

Before creating or modifying models, we analyze:

### Reusable Patterns
We identify common structures that appear across multiple use cases:
- **Information blocks**: Standardized groupings like BodySite, Reason/Indication
- **Data elements**: Common fields like identifiers, status, dates, roles
- **Relationships**: How entities reference each other

### Existing Definitions
We consult and maintain centralized resources:
- **Clinical Glossary**: Standardized terms and definitions for clinical concepts
- **Operational Glossary**: Terms for governance and project management
- **ConceptMaps**: Mappings between model elements and glossary terms

### Design Principles
Each model is evaluated against established principles:
- Consistency with existing CareSets
- Reuse of proven patterns
- Alignment with FHIR standards
- Support for multi-language requirements

---

## Data Model Creation

### Process Steps

1. **Define scope**: Identify what clinical or operational concept the model represents
2. **Map to glossary**: Link model elements to standardized definitions
3. **Identify reusable blocks**: Apply existing patterns (BodySite, identifiers, etc.)
4. **Define constraints**: Specify cardinality, required fields, and value sets
5. **Document**: Provide clear descriptions and examples
6. **Review**: Validate with stakeholders before publication

### Artifacts Produced
- **Logical Data Model**: FHIR StructureDefinition in JSON format
- **Glossary updates**: New or refined terms added to the clinical glossary
- **ConceptMap entries**: Links between model elements and glossary codes
- **Documentation**: Usage guidance and examples

---

## Maintaining Reusable Assets

### Glossaries
We maintain centralized glossaries that serve as the single source of truth:

| Glossary | Purpose | Location |
|----------|---------|----------|
| Clinical Glossary | Standardized clinical terms | `CodeSystem-glossary.json` |
| Operational Glossary | Project and governance terms | `CodeSystem-operational-glossary.json` |

**Maintenance activities:**
- Regular review of term definitions
- Addition of new terms as models evolve
- Multi-language translation (EN, FR, NL)
- Status tracking (draft, accepted, rejected)

### Reusable Patterns
Common patterns are documented and referenced across models:

| Pattern | Description | Used In |
|---------|-------------|---------|
| BodySite | Anatomical location | Observations, Procedures, Conditions |
| Identifier | Business identifier with namespace | All models |
| Reason/Indication | Why something was done | Medications, Procedures |
| Status | Record lifecycle state | All models |
| Roles | Author, Performer, Asserter | Clinical records |

### ConceptMaps
We maintain mappings between:
- Model element paths and glossary codes
- Different terminology systems
- Version transitions

---

## Consultation and Reuse

When creating new models or reviewing existing ones:

1. **Check the glossary first**: Does a definition already exist for this concept?
2. **Look for existing patterns**: Can we reuse BodySite, Identifier, or other blocks?
3. **Review related models**: How do similar CareSets handle this?
4. **Propose additions**: If new terms are needed, follow the definition guidelines

This ensures:
- **Consistency**: Same concepts defined the same way across all models
- **Efficiency**: No duplication of effort in defining common elements
- **Quality**: Reviewed and approved definitions used throughout
- **Interoperability**: Aligned terminology enables data exchange

---

## Summary

The CareSet modeling process is built on collaboration and reuse:

| Phase | Key Activities |
|-------|----------------|
| **Input** | Gather requirements from stakeholders upfront and continuously |
| **Analyze** | Identify patterns, consult glossaries, apply design principles |
| **Create** | Build models using standardized definitions and reusable blocks |
| **Maintain** | Keep glossaries current, document patterns, track changes |
| **Consult** | Reference existing assets before creating new definitions |

This approach ensures that CareSets remain consistent, interoperable, and aligned with stakeholder needs throughout their lifecycle.

---

## CareSet publication deliverables

The publication of a CareSet consists of a coherent set of normative deliverables, which go beyond the FHIR specification alone.

### Business Analysis Document

- description of the context and objectives;
- actors and roles;
- usage scenarios;
- functional scope of the CareSet.

### Business Rules

- functional and business rules associated with the CareSet;
- constraints that cannot — or cannot fully — be expressed in the FHIR specification;
- rules of consistency, dependency or temporality.

### FHIR Specification

- FHIR profiles required to represent the CareSet;
- cardinalities, bindings, invariants and technical constraints;
- alignment with international standards.

### Value Sets

- lists of codes and terminologies to be used;
- national and/or international reference sets;
- rules for using codes within the context of the CareSet.

Together, these elements make up the official deliverables of a CareSet.
