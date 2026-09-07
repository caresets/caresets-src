---
layout: default
title: Glossary
# parent: Home
nav_order: 2

---

The glossary contains the definitions used across the Belgian CareSets. It makes sure that everyone working with CareSets uses the same terms in the same way. This avoids misunderstandings between healthcare providers, software vendors and policy makers.  


## Why a shared glossary matters

When a new CareSet is defined, most of what it contains is not new. The same
handful of concepts recur in nearly every one: the person the record is about,
who recorded it and when, its status, its identifier. Agreeing them once and
reusing them is what makes a set of CareSets coherent, rather than a collection
of similar-looking structures that turn out to differ in detail.

Consistency here is not only a matter of reading well. The CareSets and this
glossary are the common specification: what is agreed here is what the FHIR
profiles express and what systems then implement, so a concept settled once
carries down to every profile and every implementation. Left unsettled, the
reconciliation does not disappear — it moves down to each profile and each
system, where everyone does it again, and differently. The risks that follow are
concrete: a query assembling a patient's record can miss what one model calls
*subject* and another calls *patient*, and an access rule written about the
recorder may not reach a model that calls it *author*.

### The same concepts, under different names

A few of the concepts that recur, across the mapped models today:

| Concept | Appears in | Written as |
|---|---|---|
| Patient — the person the record is about | 25 models | *patient*, *subject* |
| RecordedDate — when the record was entered | 19 models | *recordedDate*, *recorded*, *creationDate* |
| Recorder — who entered it | 16 models | *recorder*, *author* |
| BusinessIdentifier — the record's identifier | 22 models | *identifier*, *businessIdentifier* |

Each row is one concept. The glossary is what says so, and the link from each
model to it is what lets software know.

### How the link is made

Each element of a logical model may be linked to a glossary concept. The link
is recorded in a published mapping alongside the models, not only in the
documentation, so the elements that mean *recorder* across every model can be
listed rather than looked for by reading each model in turn.

Not every element is linked. Many are specific to one model and have no
glossary concept; an element without one is not an omission.

## The two glossaries

[Clinical Glossary](glossary_clinical.html) — definitions of the clinical concepts and terms used in the CareSets.

[Operational Glossary](glossary_operational.html) — definitions of the operational concepts and terms used in designing and understanding the Belgian eHealth ecosystem.
