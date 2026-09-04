---
layout: default
title: Glossary
# parent: Home
nav_order: 2

---

The glossary contains the definitions used across the Belgian CareSets. It makes sure that everyone working with CareSets uses the same terms in the same way. This avoids misunderstandings between healthcare providers, software vendors and policy makers.  


The Glossary is organised into the following sections:

[Clinical Glossary](glossary_clinical.html): Definitions of clinical concepts and terms used in the CareSets
[Operational Glossary](glossary_operational.html): Definitions of operational concepts and terms when designing and understanding the Belgian eHealth ecosystem


## Why a shared glossary matters

A definition written once and used everywhere is worth more than the sum of the
places it appears.

**Reuse.** A concept defined once can be reused across models. A new CareSet is
assembled from parts that already have an agreed meaning, rather than restating
what a patient, a recorder or an administration date is each time. That is
faster to design and easier to review.

**Consistent rules.** A rule written against a concept applies everywhere the
concept appears. Retention, validation, consent and quality rules can be stated
once for *the recorder of a CareSet* and hold across every model that has one.
Where each model names the same idea differently, every rule has to be restated
per model, and the copies drift apart.

**Access control.** Authorisation policies are written against concepts, not
against field names. A policy such as *a patient may see who recorded their
data* only works if the element called *recorder* in one model, *author* in another
and *recorded by* in a third are recognisably the same concept. Where they are not, a policy silently covers some models and
misses others — and a policy that fails silently is worse than one that fails
loudly.

**Auditability.** *Who is the recorder of any CareSet?* is a question about the
whole ecosystem, not about one model. It can only be answered once, across
everything, because every model points its recording element at the same
glossary term. Without that link it is as many separate questions as there are
models, with as many separate answers, and no way to know the list is complete.

**Traceability.** When a definition changes, the models affected can be
identified rather than guessed at. The same link that answers a question about
the data answers a question about the consequences of changing it.

### How the link is made

Each element of a logical model may be linked to a glossary concept. The link
is recorded in the model itself, not only in the documentation, so the elements
that mean *recorder* across every model can be listed rather than looked for by
reading each model in turn.

Not every element is linked. Many are specific to one model and have no
glossary concept; an element without one is not an omission.
