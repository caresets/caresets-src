---
layout: default
title: Logical Data Models
nav_order: 2
has_children: true
lang: en
---

# Logical Data Models

## What are Logical Models?

Logical models in FHIR are abstract representations of data structures that define the information content without specifying how that content is technically implemented or exchanged. They serve as a bridge between business requirements and technical implementation.

Unlike FHIR profiles (which constrain existing FHIR resources), logical models define completely custom structures that represent domain-specific concepts. They are particularly useful for:

- **Documenting requirements**: Capturing business and clinical requirements in a structured, computable format
- **Cross-paradigm modeling**: Defining structures that can be mapped to multiple implementation technologies (FHIR, CDA, database schemas, etc.)
- **Stakeholder communication**: Providing a technology-neutral view that clinical and business stakeholders can understand

For more details, see the [FHIR Logical Models specification](https://hl7.org/fhir/logical.html).

## Logical Models as Data Types or Ancestors

One powerful feature of FHIR logical models is their ability to reference other logical models in two ways:

### As Data Types

A logical model can use another logical model as a data type for its elements. This enables **composition** - building complex models from simpler, reusable building blocks.

For example, a `Vaccination` model might use a `BodySite` model as the type for its `site` element, rather than defining body site fields inline.

### As Ancestors (Specialization)

A logical model can extend another logical model as its parent. This creates a **specialization** relationship where the child model inherits all elements from the parent and can add new ones.

**Important**: Unlike FHIR profiles, logical model inheritance represents **specialization, not constraint**. The child model extends the parent's structure rather than restricting it. This means:

- Child models can add new required elements
- Child models can extend the cardinality of inherited elements
- Child models represent a more specific concept, not a restricted view

This distinction is crucial: profiles constrain resources for specific use cases, while logical model inheritance expands definitions for specialized domains.

---
