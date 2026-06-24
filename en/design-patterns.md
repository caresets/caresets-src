---
layout: default
title: Design Considerations
nav_order: 4
parent: Logical Data Models
lang: en
published: false   # temporarily removed
---

{: .no_toc }

Patterns are reusable, common data structures that appear across multiple CareSets. By standardizing these patterns, we:

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

<div class="info-box may" markdown="1">

**Structure:**

@startuml
hide empty members
hide circle
class BodySite {
  bodyLocation : CodeableConcept
  bodyLaterality : CodeableConcept
  bodyTopography : CodeableConcept
}
note right of BodySite::bodyLocation
  Anatomical site
end note
note right of BodySite::bodyLaterality
  Left / right / bilateral
end note
note right of BodySite::bodyTopography
  Specific topography
end note
@enduml

</div>

**Example:** Recording blood pressure on the left arm:
- bodyLocation: "Upper arm" (SNOMED CT: 40983000)
- bodyLaterality: "Left" (SNOMED CT: 7771000)


### Reason and Indication

Capturing why something was done or requested:

<div class="info-box may" markdown="1">

**Structure:**

@startuml
hide empty members
hide circle
class Reason {
  reasonCode : CodeableConcept
  reasonReference : Reference(Condition)
}
note right of Reason::reasonCode
  Coded reason
end note
note right of Reason::reasonReference
  Link to condition / problem
end note
@enduml

</div>

**Used in:**
- Medications (indication for prescribing)
- Procedures (reason for performing)
- Observations (reason for measurement)


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

Identifiers consist of:

- **System (Namespace)**: indicating which organization issues the identifier
- **Value**: The actual identifier string

The **system** helps assign different business identifiers to a CareSet instance. For example, the National Insurance Social Security number (NISS/INSZ) is Belgium's primary patient identifier:

- **System**: `https://www.ehealth.fgov.be/standards/fhir/core/NamingSystem/ssin`
- **Format**: 11 digits (YYMMDD-XXX-CC) without punctuation
- **Example value**: `85070512345`

