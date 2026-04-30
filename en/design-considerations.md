---
layout: default
title: Design Considerations
nav_order: 4
parent: Logical Data Models
lang: en
---

# Design patterns
{: .no_toc }

- TOC
{:toc}

This page outlines some design principles and patterns used across CareSets to ensure **consistency**, **reusability**, and **interoperability**.


## Definition and implementation of a CareSet

A clear distinction must be made between the **definition** of a CareSet and its **implementation**.

### CareSet Definition

- cross-cutting specification, led by the INAMI/RIZIV;
- grounded in business needs and use cases;
- normative and shared across the entire ecosystem.

### CareSet Implementation

- carried out by business software, vaults and other components of the ecosystem;
- consists of making these systems capable of producing, consuming, storing and exchanging CareSets that comply with the published definition.

The definition is the reference; implementations must conform to it.

---



## Reusable Information Blocks

Reusable information blocks are common data structures that appear across multiple CareSets. By standardizing these blocks, we:

- Reduce redundancy in model definitions
- Ensure consistency in how common concepts are captured
- Simplify implementation by reusing the same patterns
- Enable easier data aggregation and analysis


### BodySite

The BodySite model captures anatomical location information and is used in multiple contexts:

**Used in:**
- Observations (where a measurement was taken)
- Procedures (where a procedure was performed)
- Conditions (location of a problem/diagnosis)
- Specimens (collection site)

**Structure:**
```
BodySite {
  bodyLocation: CodeableConcept     // Anatomical site
  bodyLaterality: CodeableConcept   // Left/right/bilateral
  bodyTopography: CodeableConcept   // Specific topography
}
```

**Example:** Recording blood pressure on the left arm:
- bodyLocation: "Upper arm" (SNOMED CT: 40983000)
- bodyLaterality: "Left" (SNOMED CT: 7771000)


### Reason and Indication

Capturing why something was done or requested:

**Structure:**
```
Reason {
  reasonCode: CodeableConcept         // Coded reason
  reasonReference: Reference(Condition)  // Link to condition/problem
}
```

**Used in:**
- Medications (indication for prescribing)
- Procedures (reason for performing)
- Observations (reason for measurement)

<!-- ### Design Principles for Reusable Blocks

1. **Single Responsibility**: Each block should represent one cohesive concept
2. **Context Independence**: Blocks should work across different use cases
3. **Backward Compatibility**: Changes should not break existing implementations
4. **Standard Terminologies**: Use established code systems where possible
5. **Optional Where Appropriate**: Not all contexts need all elements -->

### Usage

CareSets reuse these information blocks in the following way:

1. **Reference the standard definition**, instead of redefining locally
2. **Document context-specific constraints or extensions**: Special rules may apply to each use case
3. **Use consistent naming**: Keep element names consistent across models
4. **Provide examples**: Show how the block is used in your specific context
5. **Test across use cases**: Ensure the block works in all intended scenarios



---


## Identifiers

CareSets use Business Identifiers, which uniquely identify healthcare entities (patients, observations, procedures, etc.) across different systems.

* Entities are expected to have one "main" identifier. 
  * When the CareSet is being created and submitted to its main system of record, the "main" identifier is not known yet. In this situation, another identifier should be sent, for easy tracking back to the original submitter record. An example is when a medication prescription is first created in GP software and is being sent to Recip-e to create the official entry in that system.
* Business identifiers are assigned by different organisations. The same object may have different identifiers. For example, for a Patient, the identifiers are NISS number, refugee case number, passport number, etc.  


CareSets use FHIR Identifier data types which consist of:

- **System (Namespace)**: URI indicating which organization issued the identifier
- **Value**: The actual identifier string

The **system** helps assign different business identifiers to a CareSet instance. For example, the National Insurance Social Security number (NISS/INSZ) is Belgium's primary patient identifier:

- **System**: `https://www.ehealth.fgov.be/standards/fhir/core/NamingSystem/ssin`
- **Format**: 11 digits (YYMMDD-XXX-CC) without punctuation
- **Example value**: `85070512345`

