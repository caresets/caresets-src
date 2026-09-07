# Definition quality checklist

Primary sources:

* **ISO 704:2022** — *Terminology work — Principles and methods* (clause 6: definitions; 6.5 deficient definitions)  
* **ISO/IEC Directives, Part 2 (2021)** — clause 16.5, rules for "Terms and definitions" in standards (freely available at iso.org/directives)  
* **ISO 10241-1** — layout of terminological entries in standards  
* Domain layer: **SNOMED International Editorial Guide** (textual definitions), for health terminology specifics

---

## 1\. Substitution test

**Rule:** The definition must be able to replace the term in a sentence without changing meaning or breaking grammar. Therefore it is a phrase, not a sentence — no "X is...", no "This term refers to...". **Ref:** ISO 704:2022, 6.3 (substitution principle); ISO/IEC Directives Part 2, 16.5.6.

* ❌ *medication statement* — "A medication statement is a record that documents that a patient is taking a medication."  
* ✅ *medication statement* — "record asserting that a patient is or has been taking a medication, as reported by the patient, a carer or a clinician"

Test: "The system stores each **medication statement**" → "The system stores each **record asserting that...**" — still reads correctly.

## 2\. Same grammatical category as the term

**Rule:** Nouns are defined by noun phrases, verbs by verb phrases, adjectives by adjectival phrases. **Ref:** ISO 704:2022, 6.3; ISO/IEC Directives Part 2, 16.5.6.

* ❌ *dispense (verb)* — "the supply of a medicinal product to a patient" (noun phrase for a verb)  
* ✅ *dispense (verb)* — "supply a medicinal product to a patient or carer in response to an order"

## **3\. Non-circularity**

**Rule:** The definition must not use the term itself, a derivative of it, or another term that is in turn defined by this one. **Ref:** ISO 704:2022, 6.5.2 (circular definitions); ISO/IEC Directives Part 2, 16.5.

* ❌ *care plan* — "plan describing the care planned for a patient"  
* ❌ Circular pair: *order* — "request recorded in an order entry system" / *order entry system* — "system used to record orders"  
* ✅ *care plan* — "set of intended activities and goals, organized over time, for managing one or more health conditions of a patient"

## **4\. Intensional structure: genus \+ differentiating characteristics**

**Rule:** Start from the nearest superordinate concept (record, process, statement, identifier, interaction...) and add only the characteristics that distinguish the concept from its siblings. **Ref:** ISO 704:2022, 6.3 (intensional definitions).

* ❌ *encounter* — "when a patient comes to the hospital" (no genus; excludes home care, telehealth)  
* ✅ *encounter* — "interaction between a patient and one or more healthcare providers for the purpose of providing healthcare services" (genus: *interaction*; differentia: parties \+ purpose)

## **5\. Positive formulation**

**Rule:** Say what the concept **is**, not what it is not. Negative definitions are acceptable only for intrinsically negative concepts (e.g. *absence of allergy*). **Ref:** ISO 704:2022, 6.5.4 (negative definitions).

* ❌ *unstructured data* — "data that is not structured" (negative **and** circular)  
* ✅ *unstructured data* — "data captured as free text, images or other formats without a predefined machine-processable schema"

## **6\. One concept per definition**

**Rule:** One entry defines exactly one concept. No "and/or" definitions covering two meanings; split homonyms into separate entries. **Ref:** ISO 704:2022, 6.2; ISO/IEC Directives Part 2, 16.5.

* ❌ *prescription* — "request by a clinician for a medication to be dispensed, or the paper/electronic document carrying that request"  
* ✅ Two entries: *prescription (act)* — "authorization by a qualified health professional for the supply and use of a medication for a specific patient"; *prescription document* — "artefact recording a prescription"

## **7\. No requirements, guidance or examples inside the definition**

**Rule:** Definitions describe; they do not prescribe. "Shall/should/must" and implementation detail belong in normative text; examples and clarifications go in a "Note to entry" or EXAMPLE. **Ref:** ISO/IEC Directives Part 2, 16.5 (definitions shall not contain requirements); ISO 10241-1 (notes to entry).

* ❌ *consent record* — "document capturing a patient's permissions, which shall be digitally signed and retained for at least 10 years"  
* ✅ *consent record* — "record of the permissions granted or withheld by a patient regarding the collection, use or disclosure of their health data" *Note to entry: Retention and signature requirements are specified in clause X.*

## **8\. Necessary and sufficient — neither too broad nor too narrow**

**Rule:** Every characteristic in the definition must be essential; together they must be enough to distinguish the concept from its neighbours. **Ref:** ISO 704:2022, 6.5.3 (inaccurate definitions).

* ❌ Too broad: *laboratory result* — "information produced by a laboratory" (includes invoices and staff rosters)  
* ❌ Too narrow: *laboratory result* — "numeric value obtained from a blood test" (excludes microbiology, urine, qualitative results)  
* ✅ *laboratory result* — "outcome of the analysis of a specimen, reported by a laboratory for use in the care of a patient"

## **9\. Defined or commonly understood terms only**

**Rule:** Every non-trivial word in a definition must be either understandable to the intended audience or itself defined in the same terminology; chains of definitions must bottom out. **Ref:** ISO 704:2022, 6.3 (definitions written in terms of concepts familiar to the target group).

* ❌ *resource* — "instantiation of a conformant informational entity graph per the reference information model"  
* ✅ *resource* — "unit of exchangeable content with a defined structure and identity, representing a clinical or administrative concept"

## **10\. Consistency with the concept system**

**Rule:** Sibling concepts share the same genus and parallel structure, so the hierarchy is visible from the definitions alone; the definition must not contradict the relations in the model. **Ref:** ISO 704:2022, 6.3.1 (definitions reflect the concept system).

* ❌ *medication request* — "order for a drug"; *service request* — "when a clinician wants a procedure done" (different genus, different register)  
* ✅ *medication request* — "record of a request for the supply and administration of a medication to a patient"; *service request* — "record of a request for a diagnostic or therapeutic service to be performed for a patient"

---

## **Smoke test**

Take a real sentence using the term and paste the definition in its place. If the result is ungrammatical, tautological, or reads as a requirement rather than a description, one of checks 1, 3 or 7 has been violated — these three catch the majority of defects in practice.