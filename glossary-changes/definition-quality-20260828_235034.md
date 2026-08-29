# Definition quality review - Glossaire v1 — status Active

- Generated: 2026-08-29 14:17:29
- Source: `input/Glossaire CareSets V1 28-08-2026.xlsx`, sheet `Glossaire v1`
- EN source: `input/ClinicalGlossary.csv`, `input/OperationalGlossary.csv`
- Checklist: `input/Definition quality checklist.md`
- Terms reviewed: **24** / Findings: **83** (FR 24 / NL 24 / EN 22 / cross-cutting 13)

All 23 Active items were checked in FR, NL and EN against the ten rules in
`input/Definition quality checklist.md`. **Every Active term has at least one finding.**

The headline problems:

- **Seven terms have no English definition at all** — `Business Identifier`,
  `Implantable Device`, `Lot Number`, `Originating Request`, `Series Number`, `Statut`,
  `Used device` — and `Note` has no Dutch definition. Each of those eight is a finding
  carrying proposed wording.
- **Circularity is the most common single defect** (rule 3): definitions that restate the
  term, often as a straight translation of it — « N° de lot » for *Lot Number*,
  « l'endroit du corps » for *BodyLocation*, « Lot Nummer » for the Dutch.
- **Examples, value lists and implementation instructions sit inside definitions**
  (rule 7), mostly in EN — where FR and NL already keep exactly that material in the
  `Description` column. Most of those fixes are a move, not a rewrite.
- **The three languages sometimes define different concepts.** `Category` in EN is a
  context of use; in FR and NL it is a classification attribute. `BodyLaterality` in NL
  (« zijdelingse oriëntatie ») is the body's orientation, not which side is meant.
- **Three rows still carry `<CareSet>` template placeholders**, two of them with
  unbalanced brackets, and two rows (`Author`, `VerificationStatus`) carry a
  `Description` copied from a different entry.

Only one language of one term passed with nothing to report: the EN definition of `Note`.
The EN definition of `Patient` is sound apart from a leading article, which is not
reported separately.

The proposed wordings are drafting suggestions, not domain rulings — where a fix needed a
fact that is not in the workbook, the models or the CSVs, the finding says so in a
**Note**.

## How to review this file

For every finding, edit its `decision` block:

- `status: accept` - take the proposed wording as it stands.
- `status: revise` - put **your** wording on the `fr:`, `nl:` and/or `en:` line;
  it is used verbatim, nothing is rewritten on top of it.
- `status: reject` - leave the current definition alone.
- `status: pending` - undecided; nothing is applied.

Anything on `comment:` is read back but never written into the glossary. Nothing
outside these blocks is parsed, so notes in the margins are safe.

When you are done, hand the file back: it is read with `collect_decisions.py`,
then applied to a **new copy** of the workbook - the source `.xlsx` is never
edited in place.

## Findings by rule

Severity: **major** 64 / **missing** 11 / **minor** 8

| Rule | | Findings |
|------|--|----------|
| 1 | substitution | 23 |
| 3 | non-circularity | 29 |
| 4 | genus + differentia | 13 |
| 5 | positive formulation | 1 |
| 6 | one concept | 12 |
| 7 | no requirements/examples | 18 |
| 8 | necessary and sufficient | 21 |
| 9 | understandable terms | 15 |
| 10 | concept-system consistency | 17 |

## Summary

| ID | Term | Row | Lang | Rules | Severity | Issue |
|----|------|-----|------|-------|----------|-------|
| F-001 | (template placeholders) |  | cross-cutting | 9 | major | Angle-bracket template markers have been left inside definition text in at least three... |
| F-002 | (body-site items) |  | cross-cutting | 8, 10 | major | `BodyLocation` (« l'endroit du corps ») and `BodyTopoGraphy` (« la localisation ou la p... |
| F-003 | (item naming) |  | cross-cutting | 10 | minor | Three naming conventions coexist in the same column: closed CamelCase (`AdministrationD... |
| F-004 | (status-like items) |  | cross-cutting | 10 | minor | `Statut` (row 22), `ClinicalStatus` (row 10) and `VerificationStatus` (row 24) are sibl... |
| F-081 | Device | None | FR | 4, 9 | missing | Device is used as the genus of both `Implantable Device` (row 12) and `Used device` (ro... |
| F-082 | Device | None | NL | 4, 9 | missing | Device is used as the genus of both `Implantable Device` (row 12) and `Used device` (ro... |
| F-083 | Device | None | EN | 4, 9 | missing | Device is used as the genus of both `Implantable Device` (row 12) and `Used device` (ro... |
| F-005 | AdministrationDate | 2 | FR | 1 | minor | Reads as a column label rather than a substitutable noun phrase: initial capital, final... |
| F-006 | AdministrationDate | 2 | NL | 1 | minor | Same form issues as FR — initial capital, final full stop, slash-joined pair. The subst... |
| F-007 | AdministrationDate | 2 | EN | 1, 7 | major | The second sentence is a note to entry — an allowance about what may be recorded when t... |
| F-008 | Asserter | 3 | FR | 8 | major | « l'information » is unbounded — any information at all. Nothing ties the person to the... |
| F-009 | Asserter | 3 | NL | 8, 10 | major | Same unbounded « de informatie », plus a divergence from FR: « verstrekt » (supplies, p... |
| F-010 | Asserter | 3 | EN | 7, 8 | major | The parenthesised list is an example inside the definition. It is also doing the work t... |
| F-011 | Author | 4 | cross-cutting | 8, 10 | major | `Description FR` and `Description NL` for Author are a verbatim copy of `Asserter`'s (r... |
| F-012 | Author | 4 | cross-cutting | 6, 10 | major | Row 4 declares `Recorder` a synonym of `Author`, while `RecordedDate` (row 19) says the... |
| F-013 | Author | 4 | FR | 3, 6 | major | « encode … contenu encodé » defines the term partly by repeating itself. The definition... |
| F-014 | Author | 4 | NL | 3, 6 | major | Mirrors the French: « invoert … ingevoerde inhoud » repeats itself, and the same two ch... |
| F-015 | Author | 4 | EN | 10 | minor | The cleanest of the three, but it drops the data-entry characteristic that FR and NL bo... |
| F-016 | BodyLaterality | 5 | FR | 3, 4 | major | Circular: the term is restated as its own definition. It gives no genus beyond the term... |
| F-017 | BodyLaterality | 5 | NL | 3, 9, 10 | major | « zijdelingse oriëntatie » means sideways orientation — how the body is turned — not wh... |
| F-018 | BodyLaterality | 5 | EN | 1, 3, 7 | major | Verb-initial, so it cannot replace the term in a sentence; it restates the term as its... |
| F-019 | BodyLocation | 6 | FR | 3, 4, 8 | major | The term translated, not a definition: no differentia, and no link to the record it qua... |
| F-020 | BodyLocation | 6 | NL | 3, 4, 8 | major | A bare noun repeating the term. No differentia, nothing tying it to the record. |
| F-021 | BodyLocation | 6 | EN | 1, 3, 7 | major | Verb-initial, restates the term, and carries examples inline that FR and NL keep in the... |
| F-022 | BodyTopoGraphy | 7 | cross-cutting | 10 | minor | Internal capital G in the middle of a word, unlike its siblings `BodyLocation` and `Bod... |
| F-023 | BodyTopoGraphy | 7 | FR | 6, 8, 10 | major | Two concepts joined by « ou » — a location and a relative position — the first of which... |
| F-024 | BodyTopoGraphy | 7 | NL | 6, 8, 10 | major | Same two-concepts-in-one as FR, same overlap with `BodyLocation`, and the cell ends on... |
| F-025 | BodyTopoGraphy | 7 | EN | 1, 6, 7 | major | Verb-initial, two concepts joined by “or”, and the examples sit inside the definition. |
| F-026 | Business Identifier | 8 | cross-cutting | 6, 8 | major | The definition asserts uniqueness, the cardinality allows many (`Max = *`), and the Des... |
| F-027 | Business Identifier | 8 | FR | 3, 8 | major | « Identifiant métier » is the term itself in French, so the definition restates rather... |
| F-028 | Business Identifier | 8 | NL | 3, 8, 9 | major | « functie-ID » is not a rendering of « identifiant métier » — it reads as the identifie... |
| F-029 | Business Identifier | 8 | EN | - | missing | No EN definition exists: the term is absent from both `ClinicalGlossary.csv` and `Opera... |
| F-030 | Category | 9 | FR | 1, 7, 8 | major | Opens with an article and runs to a full clause; « défini par une ValueSet standardisée... |
| F-031 | Category | 9 | NL | 1, 7, 8 | major | A faithful translation of a definition that breaches rules 1, 7 and 8 — so it breaches... |
| F-032 | Category | 9 | EN | 8, 10 | major | Says something else entirely: FR and NL define a classification attribute used for grou... |
| F-033 | ClinicalStatus | 10 | FR | 1, 3 | major | Verb-initial, so it fails the substitution test, and it defines *ClinicalStatus* as « l... |
| F-034 | ClinicalStatus | 10 | NL | 1, 3 | major | Verb construction that cannot substitute for the term, and it defines *ClinicalStatus*... |
| F-035 | ClinicalStatus | 10 | EN | 1, 3, 7 | major | Verb-initial, restates the term, and carries its value list inside the definition. |
| F-036 | Code | 11 | FR | 1, 4 | major | Verb-initial and therefore not substitutable, and it has no genus: it says what the ele... |
| F-037 | Code | 11 | NL | 1, 4 | major | Same as FR — a verb phrase describing the element's function rather than a noun phrase... |
| F-038 | Code | 11 | EN | 1, 4 | major | Same as FR and NL — verb-initial, no genus. |
| F-039 | Implantable Device | 12 | FR | 6, 7, 8 | major | Three things in one cell: the concept, an inline example list, and an implementation in... |
| F-040 | Implantable Device | 12 | NL | 6, 7, 8 | major | The cell is truncated mid-clause, opens with a stray double quote, and the rest of the... |
| F-041 | Implantable Device | 12 | EN | - | missing | No EN definition exists in either glossary CSV for this active term. |
| F-042 | Lot Number | 13 | FR | 3, 4 | major | The definition is the term translated. No genus, no differentia, nothing saying who ass... |
| F-043 | Lot Number | 13 | NL | 3, 4 | major | The cell repeats the term, in English word order. It is not a definition. |
| F-044 | Lot Number | 13 | EN | - | missing | No EN definition exists in either glossary CSV for this active term. |
| F-045 | Note | 14 | cross-cutting | 5, 7 | major | The Description says a note contains no sensitive data and then offers, as examples, ex... |
| F-046 | Note | 14 | FR | 1, 8 | minor | « relative » does not agree with « Informations » (should be « relatives »), and « en f... |
| F-047 | Note | 14 | NL | - | missing | `Définition NL` and `Description NL` are both empty for an active term. |
| F-048 | Originating Request | 15 | FR | 3, 8 | major | Restates the term (« Originating Request » → « la demande … à l'origine ») without addi... |
| F-049 | Originating Request | 15 | NL | 3, 8 | major | Same restatement of the term as FR, and « van CareSet » is likewise missing its article. |
| F-050 | Originating Request | 15 | EN | - | missing | No EN definition exists in either glossary CSV for this active term. |
| F-051 | PartOf | 16 | FR | 3, 7 | major | Defines *PartOf* with « fait partie », restates the same thing a second way after « soi... |
| F-052 | PartOf | 16 | NL | 3 | major | Circular in the same way as FR, and the clause after « oftewel » only repeats the first... |
| F-053 | PartOf | 16 | EN | 3, 7 | major | Circular, restated after “i.e.”, and closes with an example inside the definition. |
| F-054 | Patient | 17 | FR | 9 | major | The angle-bracket placeholder `<CareSet>` is a template marker left in the text, and «... |
| F-055 | Patient | 17 | NL | 9 | minor | Same leftover `<CareSet>` placeholder; otherwise a faithful and well-formed rendering. |
| F-056 | Performer | 18 | FR | 8, 9 | major | Two unbalanced `<` template markers make the cell read as broken template text. « en fo... |
| F-057 | Performer | 18 | NL | 9 | major | The same leftover template markers, here wrapping the whole predicate, and « op basis v... |
| F-058 | Performer | 18 | EN | 7 | major | The parenthesised examples belong in a note to entry, not in the definition; “according... |
| F-059 | RecordedDate | 19 | FR | 6, 10 | major | « l'Author ou le Recorder » offers two roles as alternatives, but row 4 declares `Recor... |
| F-060 | RecordedDate | 19 | NL | 6, 9, 10 | major | Same Author/Recorder contradiction. « het record » is also an anglicism where the rest... |
| F-061 | RecordedDate | 19 | EN | 1, 7 | major | The second sentence explains what the field enables — historisation through the Busines... |
| F-062 | Route | 20 | FR | 1, 3 | major | Opens with « Est la » — a sentence predicate, which fails the substitution test outrigh... |
| F-063 | Route | 20 | NL | 1, 3 | major | Opens with « Dit is de … », the same substitution failure as FR, and restates the term... |
| F-064 | Route | 20 | EN | 3, 7 | major | Defines *Route* as “the route of administration”, and closes with a pointer to a ValueS... |
| F-065 | Series Number | 21 | cross-cutting | 9, 10 | major | A *series number* names a series; what both definitions and the note describe is the ma... |
| F-066 | Series Number | 21 | FR | 3, 4 | major | The term restated. No genus, nothing about who assigns the number, and — critically — n... |
| F-067 | Series Number | 21 | NL | 3, 4 | major | The term restated, with the same missing differentia against `Lot Number`. |
| F-068 | Series Number | 21 | EN | - | missing | No EN definition exists in either glossary CSV for this active term. |
| F-069 | Statut | 22 | cross-cutting | 10 | major | The item name is in French while every other item in the sheet is named in English. A s... |
| F-070 | Statut | 22 | FR | 1, 3 | major | Verb-initial, so not substitutable; defines *Statut* as « le statut »; and the two halv... |
| F-071 | Statut | 22 | NL | 1, 3 | major | Same verb construction, same restatement of the term, same comma splice as the French. |
| F-072 | Statut | 22 | EN | - | missing | No EN definition exists in either glossary CSV for this active term. |
| F-073 | Used device | 23 | FR | 7, 9 | major | Leftover `<CareSet>` placeholder, and « utilisé pour » simply restates the term. The De... |
| F-074 | Used device | 23 | NL | 9 | major | Broken placeholder — an unclosed `<CareSet.` — and the same restatement of the term as FR. |
| F-075 | Used device | 23 | EN | - | missing | No EN definition exists in either glossary CSV for this active term. |
| F-076 | VerificationStatus | 24 | cross-cutting | 10 | major | `Description FR` and `Description NL` for VerificationStatus contain blood-pressure com... |
| F-077 | VerificationStatus | 24 | cross-cutting | 6 | major | Verification status (confirmed / refuted / entered-in-error) and certainty (how confide... |
| F-078 | VerificationStatus | 24 | FR | 1, 3 | major | Verb-initial. It also defines a *verification* status as a *certainty* level — the syno... |
| F-079 | VerificationStatus | 24 | NL | 1, 3, 9 | major | Verb construction that cannot substitute for the term, and « opname » in a health conte... |
| F-080 | VerificationStatus | 24 | EN | 1, 7 | major | Verb-initial, with the value list inside the definition. The values themselves (“confir... |

## Findings

---

### F-001 - `(template placeholders)` - cross-cutting

**Rules:** 9 (understandable terms) / **Severity:** major

**Current**

> Patient (row 17): « l'enregistrement (<CareSet>) » · Performer (row 18): « qui a <fait l'action en fonction du <CareSet> » · Used device (row 23): « utilisé pour <CareSet>. »

**Problem**

Angle-bracket template markers have been left inside definition text in at least three active rows, two of them with unbalanced brackets. They are meaningless to a reader and would be published as they stand.

**Proposed**

> Sweep the whole sheet — not only the Active rows — for `<` and `>` in the Definition and Description columns and resolve each one into real text.

**Note:** The per-language findings for rows 17, 18 and 23 already propose placeholder-free wording.

```decision F-001
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Sweep approved. The Patient row 17 wording drafted here has moved to F-054, which is the finding that writes to the cell; rows 18 and 23 are decided on their own findings.
```

---

### F-002 - `(body-site items)` - cross-cutting

**Rules:** 8 (necessary and sufficient), 10 (concept-system consistency) / **Severity:** major

**Problem**

`BodyLocation` (« l'endroit du corps ») and `BodyTopoGraphy` (« la localisation ou la position relative sur l'endroit corps ») overlap: the first half of the second definition is the whole of the first. Nothing in the pair tells an implementer which element to use.

**Proposed**

> Separate them explicitly — `BodyLocation` names the body part, `BodyTopoGraphy` names the position *within* that part. The per-language proposals below are written to that split.

```decision F-002
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Split approved. It matches StructureDefinition-BeModelBodySite.json, where bodyLocation, bodyLaterality and bodyTopography are already three sibling 0..1 elements. Wording lands via F-019/F-020/F-021 and F-023/F-024/F-025.
```

---

### F-003 - `(item naming)` - cross-cutting

**Rules:** 10 (concept-system consistency) / **Severity:** minor

**Problem**

Three naming conventions coexist in the same column: closed CamelCase (`AdministrationDate`, `ClinicalStatus`, `PartOf`), spaced Title Case (`Business Identifier`, `Lot Number`, `Implantable Device`) and spaced lower case (`Used device`). Sibling concepts should be recognisable as siblings from their names alone.

**Proposed**

> Pick one convention for the whole sheet and apply it — closed CamelCase is the majority and matches the element names in `DataDictionary`.

```decision F-003
status: revise        # accept | reject | revise
fr:
nl:
en:
comment: Reviewer's variant, not the proposal as drafted. Standardise the Item column on spaced Title Case as the human label (Administration Date, Body Topography, Used Device), and derive the CodeSystem code from it by removing the spaces, so codes stay CamelCase. Existing GlossaryCode values in glossary_mappings.csv (AdministrationDate, BusinessIdentifier, LotNumber) keep working unchanged. Requires a change to generate_glossary.py, which today uses Term verbatim as the code.
```

---

### F-004 - `(status-like items)` - cross-cutting

**Rules:** 10 (concept-system consistency) / **Severity:** minor

**Problem**

`Statut` (row 22), `ClinicalStatus` (row 10) and `VerificationStatus` (row 24) are siblings but are written with three different genera and three different openings (« Indique le statut de l'enregistrement… », « Indique le statut de la pertinance… », « Indique le niveau de certitude… »). The hierarchy is not visible from the definitions.

**Proposed**

> Give all three the same genus (« état … » / « toestand … » / “state …”) and let the differentia carry the distinction — lifecycle, clinical currency, verification. The per-language proposals below are written to do that.

**Note:** `Description FR` for ClinicalStatus lists “completed” among its values; that is a lifecycle value and belongs to `Statut`.

```decision F-004
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Approved by the reviewer. All three status items take a parallel genus; the differentia carries lifecycle vs clinical currency vs verification.
```

---

### F-081 - `Device` - FR

**Rules:** 4 (genus + differentia), 9 (understandable terms) / **Severity:** missing

**Problem**

Device is used as the genus of both `Implantable Device` (row 12) and `Used device` (row 23), and both Descriptions point at « une ressource Device » - but the term is defined nowhere: not in the sheet at any status, and not in either glossary CSV. The definition chain does not bottom out, and the genus of two active entries sits outside the concept system.

**Proposed**

> instrument, appareil, équipement, logiciel ou autre article destiné par son fabricant à être utilisé à des fins médicales chez l'être humain

**Note:** New term, raised by the reviewer. Wording follows EU MDR 2017/745 art. 2(1), trimmed to a glossary entry. Needs a new Active row in the sheet, so it has no row number yet.

```decision F-081
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Approved by the reviewer: Device is added as an Active term so both Implantable Device and Used device have a defined genus. New row in the sheet plus a row in ClinicalGlossary.csv - no script writes it, since the term has no row yet.
```

### F-082 - `Device` - NL

**Rules:** 4 (genus + differentia), 9 (understandable terms) / **Severity:** missing

**Problem**

Device is used as the genus of both `Implantable Device` (row 12) and `Used device` (row 23), and both Descriptions point at « une ressource Device » - but the term is defined nowhere: not in the sheet at any status, and not in either glossary CSV. The definition chain does not bottom out, and the genus of two active entries sits outside the concept system.

**Proposed**

> instrument, toestel, apparaat, software of ander artikel dat door de fabrikant bestemd is om bij de mens voor medische doeleinden te worden gebruikt

```decision F-082
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Approved by the reviewer: Device is added as an Active term so both Implantable Device and Used device have a defined genus. New row in the sheet plus a row in ClinicalGlossary.csv - no script writes it, since the term has no row yet.
```

### F-083 - `Device` - EN

**Rules:** 4 (genus + differentia), 9 (understandable terms) / **Severity:** missing

**Problem**

Device is used as the genus of both `Implantable Device` (row 12) and `Used device` (row 23), and both Descriptions point at « une ressource Device » - but the term is defined nowhere: not in the sheet at any status, and not in either glossary CSV. The definition chain does not bottom out, and the genus of two active entries sits outside the concept system.

**Proposed**

> instrument, apparatus, appliance, software or other article intended by its manufacturer to be used for medical purposes in human beings

```decision F-083
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Approved by the reviewer: Device is added as an Active term so both Implantable Device and Used device have a defined genus. New row in the sheet plus a row in ClinicalGlossary.csv - no script writes it, since the term has no row yet.
```

---

### F-005 - `AdministrationDate` (row 2) - FR

**Rules:** 1 (substitution) / **Severity:** minor

**Current**

> Date d’administration du produit / vaccin par le Performer.

**Problem**

Reads as a column label rather than a substitutable noun phrase: initial capital, final full stop, and a slash-joined pair standing in for “or”. The content is sound; only the form breaches the substitution and layout conventions.

**Proposed**

> date à laquelle un produit ou un vaccin est administré au patient par le Performer

```decision F-005
status: accept        # accept | reject | revise
fr:
nl:
en:
comment:
```

### F-006 - `AdministrationDate` (row 2) - NL

**Rules:** 1 (substitution) / **Severity:** minor

**Current**

> Datum waarop het product/vaccin door de Performer is toegediend.

**Problem**

Same form issues as FR — initial capital, final full stop, slash-joined pair. The substance matches the French.

**Proposed**

> datum waarop een product of vaccin door de Performer aan de patiënt is toegediend

```decision F-006
status: accept        # accept | reject | revise
fr:
nl:
en:
comment:
```

### F-007 - `AdministrationDate` (row 2) - EN

**Rules:** 1 (substitution), 7 (no requirements/examples) / **Severity:** major

**Current**

> Date of administration of the vaccine or product. For vaccines, a life period may also be mentioned if exact dates are unknown (during childhood, adolescence...)

**Problem**

The second sentence is a note to entry — an allowance about what may be recorded when the date is unknown — sitting inside the definition. FR and NL keep exactly that material in the Description column, so the three languages currently define different things. EN also drops « par le Performer ».

**Proposed**

> date on which a product or vaccine is administered to the patient by the Performer

**Move to the `Description` column:** For vaccines, a life period may also be recorded when the exact date is unknown (during childhood, adolescence, …).

```decision F-007
status: accept        # accept | reject | revise
fr:
nl:
en:
comment:
```

---

### F-008 - `Asserter` (row 3) - FR

**Rules:** 8 (necessary and sufficient) / **Severity:** major

**Current**

> La personne à la source de l’information

**Problem**

« l'information » is unbounded — any information at all. Nothing ties the person to the CareSet, so the definition does not distinguish an Asserter from any informant anywhere.

**Proposed**

> personne qui est à la source de l'information enregistrée dans le CareSet

```decision F-008
status: revise        # accept | reject | revise
fr: personne qui rapporte l'information enregistrée dans le CareSet
nl:
en:
comment: Reviewer's variant: 'rapporte' rather than 'est à la source de'. Settled with F-009 and F-010 so the three languages take the same reading, which also matches the element name Asserter. Knowingly diverges from FHIR's 'source of the information'.
```

### F-009 - `Asserter` (row 3) - NL

**Rules:** 8 (necessary and sufficient), 10 (concept-system consistency) / **Severity:** major

**Current**

> De persoon die de informatie verstrekt

**Problem**

Same unbounded « de informatie », plus a divergence from FR: « verstrekt » (supplies, passes on) is a narrower act than being the source — whoever passes information on is not necessarily where it originates.

**Proposed**

> persoon die aan de bron ligt van de in de CareSet geregistreerde informatie

```decision F-009
status: revise        # accept | reject | revise
fr:
nl: persoon die de in de CareSet geregistreerde informatie rapporteert
en:
comment: Reviewer's variant. NL keeps the reporting sense it already had rather than being pulled to 'source'; FR and EN move to match it.
```

### F-010 - `Asserter` (row 3) - EN

**Rules:** 7 (no requirements/examples), 8 (necessary and sufficient) / **Severity:** major

**Current**

> The person who is the source of the information (e.g., the patient, general practitioner, a relative, the professional recording the information themselves, ...)

**Problem**

The parenthesised list is an example inside the definition. It is also doing the work the differentia should do, so simply deleting it would leave the definition too broad.

**Proposed**

> person who is the source of the information recorded in the CareSet

**Move to the `Description` column:** For example: the patient, the general practitioner, a relative, or the professional recording the information themselves.

```decision F-010
status: revise        # accept | reject | revise
fr:
nl:
en: person who reports the information recorded in the CareSet
comment: Reviewer's variant, same reading as F-008/F-009. The examples still move out of the definition into the Description column as proposed.
```

---

### F-011 - `Author` (row 4) - cross-cutting

**Rules:** 8 (necessary and sufficient), 10 (concept-system consistency) / **Severity:** major

**Current**

> Toutefois, lorsqu'il s'agit d'un parent ou proche, seul le rôle sera encodé (ex : père, mère, voisin, aidant-proche, ami, …) pour répondre aux exigences RGPD. […] on utilisera le ValueSet « VS_PatientRelationshipType » […]

**Problem**

`Description FR` and `Description NL` for Author are a verbatim copy of `Asserter`'s (row 3). Author is defined as a healthcare professional, so guidance about what to do when the person is a parent or an informal carer cannot apply to it — the text was pasted one row too far.

**Proposed**

> Delete the copied block from Author's Description. If a note is needed there, describe how the Author is identified (NISS / BIS / NIHDI number), as `Performer` does.

```decision F-011
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Delete and replace, per the reviewer. The copied Asserter block goes; in its place a note on how the Author is identified (NISS / BIS / NIHDI number), parallel to what Performer's Description already carries.
```

### F-012 - `Author` (row 4) - cross-cutting

**Rules:** 6 (one concept), 10 (concept-system consistency) / **Severity:** major

**Current**

> Author — Synonym: Recorder

**Problem**

Row 4 declares `Recorder` a synonym of `Author`, while `RecordedDate` (row 19) says the record is entered « par l'Author ou le Recorder » — offering them as alternatives. Both cannot hold: either they are one concept, and RecordedDate must name only one, or they are two, and Recorder needs its own entry and must stop being listed as a synonym.

**Proposed**

> Decide which it is. If they are distinct (the person who enters the data vs. the person who owns the content), add a `Recorder` entry and drop the synonym. The Author and RecordedDate proposals below assume that reading.

```decision F-012
status: revise        # accept | reject | revise
fr:
nl:
en:
comment: Reviewer's ruling: one concept, and the main term is Recorder with Author kept as its synonym - the reverse of row 4 today. So the rule-6 objection falls away: entering the data and being responsible for it are two characteristics of one role, not two concepts, and the definition may carry both. Knock-ons: RecordedDate must name the Recorder, not 'l'Author ou le Recorder'; the three GlossaryCode=Author rows in glossary_mappings.csv (vaccination, allergyintolerance, BeModelProblem, all on element 'recorder') must become Recorder; and ClinicalGlossary.csv row 4 swaps Term and Synonym.
```

### F-013 - `Author` (row 4) - FR

**Rules:** 3 (non-circularity), 6 (one concept) / **Severity:** major

**Current**

> le professionnel de la santé qui encode et prend la responsabilité du contenu encodé.

**Problem**

« encode … contenu encodé » defines the term partly by repeating itself. The definition also bundles two characteristics — performing the data entry and carrying responsibility for the content — which the model itself treats as separable (see the `Recorder` synonym and `RecordedDate`).

**Proposed**

> professionnel de la santé qui assume la responsabilité du contenu enregistré dans le CareSet

**Note:** If the Author/Recorder question is settled the other way — one concept covering both acts — say so once, here, and align `RecordedDate` to it.

```decision F-013
status: revise        # accept | reject | revise
fr: professionnel de la santé qui enregistre le contenu du CareSet et en assume la responsabilité
nl:
en:
comment: Reviewer's variant, following the F-012 ruling that Recorder/Author is one concept: both characteristics are kept - recording the content and being responsible for it - and only the circular repetition is removed.
```

### F-014 - `Author` (row 4) - NL

**Rules:** 3 (non-circularity), 6 (one concept) / **Severity:** major

**Current**

> de zorgverlener die de gegevens invoert en de verantwoordelijkheid draagt voor de ingevoerde inhoud.

**Problem**

Mirrors the French: « invoert … ingevoerde inhoud » repeats itself, and the same two characteristics are bundled into one definition.

**Proposed**

> zorgverlener die de verantwoordelijkheid draagt voor de in de CareSet geregistreerde inhoud

```decision F-014
status: revise        # accept | reject | revise
fr:
nl: zorgverlener die de inhoud van de CareSet vastlegt en er de verantwoordelijkheid voor draagt
en:
comment: Reviewer's variant, following the F-012 ruling that Recorder/Author is one concept: both characteristics are kept - recording the content and being responsible for it - and only the circular repetition is removed.
```

### F-015 - `Author` (row 4) - EN

**Rules:** 10 (concept-system consistency) / **Severity:** minor

**Current**

> The healthcare professional who takes responsibility for the recorded content

**Problem**

The cleanest of the three, but it drops the data-entry characteristic that FR and NL both carry, so the languages define slightly different concepts today. Aligning FR and NL onto this reading resolves it; only the leading article then remains.

**Proposed**

> healthcare professional who takes responsibility for the content recorded in the CareSet

```decision F-015
status: revise        # accept | reject | revise
fr:
nl:
en: healthcare professional who records the content of the CareSet and takes responsibility for it
comment: Reviewer's variant, following the F-012 ruling that Recorder/Author is one concept: both characteristics are kept - recording the content and being responsible for it - and only the circular repetition is removed.
```

---

### F-016 - `BodyLaterality` (row 5) - FR

**Rules:** 3 (non-circularity), 4 (genus + differentia) / **Severity:** major

**Current**

> la latéralité du corps .

**Problem**

Circular: the term is restated as its own definition. It gives no genus beyond the term itself, no differentia, and does not say what the laterality qualifies.

**Proposed**

> côté du corps auquel se rapporte l'information enregistrée

```decision F-016
status: accept        # accept | reject | revise
fr:
nl:
en:
comment:
```

### F-017 - `BodyLaterality` (row 5) - NL

**Rules:** 3 (non-circularity), 9 (understandable terms), 10 (concept-system consistency) / **Severity:** major

**Current**

> de zijdelingse oriëntatie van het lichaam

**Problem**

« zijdelingse oriëntatie » means sideways orientation — how the body is turned — not which side of it is concerned. That is a different concept from the FR and EN entries and would mislead an implementer.

**Proposed**

> zijde van het lichaam waarop de geregistreerde informatie betrekking heeft

```decision F-017
status: accept        # accept | reject | revise
fr:
nl:
en:
comment:
```

### F-018 - `BodyLaterality` (row 5) - EN

**Rules:** 1 (substitution), 3 (non-circularity), 7 (no requirements/examples) / **Severity:** major

**Current**

> Specifies the body laterality (right, left, both)

**Problem**

Verb-initial, so it cannot replace the term in a sentence; it restates the term as its own definition; and it carries the permitted values inline, where FR and NL keep them in the Description column.

**Proposed**

> side of the body to which the recorded information refers

**Move to the `Description` column:** Right, left, or both.

```decision F-018
status: accept        # accept | reject | revise
fr:
nl:
en:
comment:
```

---

### F-019 - `BodyLocation` (row 6) - FR

**Rules:** 3 (non-circularity), 4 (genus + differentia), 8 (necessary and sufficient) / **Severity:** major

**Current**

> l'endroit du corps.

**Problem**

The term translated, not a definition: no differentia, and no link to the record it qualifies. As written it also collides with `BodyTopoGraphy`, whose FR definition opens with the same words.

**Proposed**

> partie du corps à laquelle se rapporte l'information enregistrée

```decision F-019
status: accept        # accept | reject | revise
fr:
nl:
en:
comment:
```

### F-020 - `BodyLocation` (row 6) - NL

**Rules:** 3 (non-circularity), 4 (genus + differentia), 8 (necessary and sufficient) / **Severity:** major

**Current**

> het lichaamsdeel

**Problem**

A bare noun repeating the term. No differentia, nothing tying it to the record.

**Proposed**

> lichaamsdeel waarop de geregistreerde informatie betrekking heeft

```decision F-020
status: accept        # accept | reject | revise
fr:
nl:
en:
comment:
```

### F-021 - `BodyLocation` (row 6) - EN

**Rules:** 1 (substitution), 3 (non-circularity), 7 (no requirements/examples) / **Severity:** major

**Current**

> Indicates the body location (head, leg, femur, heart, ...)

**Problem**

Verb-initial, restates the term, and carries examples inline that FR and NL keep in the Description column.

**Proposed**

> part of the body to which the recorded information refers

**Move to the `Description` column:** For example: head, leg, femur, heart, …

```decision F-021
status: accept        # accept | reject | revise
fr:
nl:
en:
comment:
```

---

### F-022 - `BodyTopoGraphy` (row 7) - cross-cutting

**Rules:** 10 (concept-system consistency) / **Severity:** minor

**Current**

> BodyTopoGraphy

**Problem**

Internal capital G in the middle of a word, unlike its siblings `BodyLocation` and `BodyLaterality`.

**Proposed**

> Rename the item to `BodyTopography`.

```decision F-022
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Confirmed by the reviewer. `bodyTopography` is also how the element is spelled in StructureDefinition-BeModelBodySite.json, so the sheet is the outlier.
```

### F-023 - `BodyTopoGraphy` (row 7) - FR

**Rules:** 6 (one concept), 8 (necessary and sufficient), 10 (concept-system consistency) / **Severity:** major

**Current**

> La localisation ou la position relative  sur l'endroit corps

**Problem**

Two concepts joined by « ou » — a location and a relative position — the first of which duplicates `BodyLocation` outright. « l'endroit corps » is also ungrammatical, missing « du ».

**Proposed**

> position relative d'une structure à l'intérieur de la partie du corps concernée

```decision F-023
status: revise        # accept | reject | revise
fr: position relative, à l'intérieur de la partie du corps concernée, du siège de l'information enregistrée
nl:
en:
comment: Reviewer's variant: same split as proposed, but phrased without the word 'structure', so the definition does not imply an anatomical structure is always what is being located.
```

### F-024 - `BodyTopoGraphy` (row 7) - NL

**Rules:** 6 (one concept), 8 (necessary and sufficient), 10 (concept-system consistency) / **Severity:** major

**Current**

> De locatie of de relatieve positie op het lichaam,

**Problem**

Same two-concepts-in-one as FR, same overlap with `BodyLocation`, and the cell ends on a stray comma.

**Proposed**

> relatieve positie van een structuur binnen het betrokken lichaamsdeel

```decision F-024
status: revise        # accept | reject | revise
fr:
nl: relatieve positie, binnen het betrokken lichaamsdeel, van de plaats waarop de geregistreerde informatie betrekking heeft
en:
comment: Reviewer's variant: same split as proposed, but phrased without the word 'structure', so the definition does not imply an anatomical structure is always what is being located.
```

### F-025 - `BodyTopoGraphy` (row 7) - EN

**Rules:** 1 (substitution), 6 (one concept), 7 (no requirements/examples) / **Severity:** major

**Current**

> Describes the location or relative position on the body, such as superior/inferior, medial/lateral or internal/external

**Problem**

Verb-initial, two concepts joined by “or”, and the examples sit inside the definition.

**Proposed**

> relative position of a structure within the body part concerned

**Move to the `Description` column:** For example: superior/inferior, medial/lateral, internal/external.

```decision F-025
status: revise        # accept | reject | revise
fr:
nl:
en: relative position, within the body part concerned, of the site to which the recorded information refers
comment: Reviewer's variant: same split as proposed, but phrased without the word 'structure', so the definition does not imply an anatomical structure is always what is being located.
```

---

### F-026 - `Business Identifier` (row 8) - cross-cutting

**Rules:** 6 (one concept), 8 (necessary and sufficient) / **Severity:** major

**Current**

> Definition: « Identifiant métier unique » · Suggested Max: * · Description: « dans certains cas, plusieurs identifiants seront permit »

**Problem**

The definition asserts uniqueness, the cardinality allows many (`Max = *`), and the Description says several are allowed. The entry contradicts itself in three places, so an implementer cannot tell whether one identifier is valid or several.

**Proposed**

> Keep `Max = *` and let the definition say what each identifier does — designate one instance unambiguously — rather than how many there may be. See the FR/NL findings for this row.

```decision F-026
status: revise        # accept | reject | revise
fr:
nl:
en:
comment: Reviewer's ruling: there can be many identifiers, each unique within its own space. Max = * stays; the definition drops the bare claim of uniqueness and states the scope in which each identifier is unique, which is what resolves the contradiction.
```

### F-027 - `Business Identifier` (row 8) - FR

**Rules:** 3 (non-circularity), 8 (necessary and sufficient) / **Severity:** major

**Current**

> Identifiant métier unique  d'une instance du CareSet.

**Problem**

« Identifiant métier » is the term itself in French, so the definition restates rather than defines. Nothing says who assigns the identifier or in what scope it holds, and « unique » contradicts both `Suggested Max = *` and the Description.

**Proposed**

> identifiant attribué par le système source pour désigner sans ambiguïté une instance de CareSet dans son contexte métier

```decision F-027
status: revise        # accept | reject | revise
fr: identifiant qui désigne une instance de CareSet et qui est unique dans l'espace de nommage du système qui l'attribue
nl:
en:
comment: Reviewer's ruling: there can be many identifiers, each unique within its own space. Max = * stays; the definition drops the bare claim of uniqueness and states the scope in which each identifier is unique, which is what resolves the contradiction.
```

### F-028 - `Business Identifier` (row 8) - NL

**Rules:** 3 (non-circularity), 8 (necessary and sufficient), 9 (understandable terms) / **Severity:** major

**Current**

> Unieke functie-ID van een instantie van de CareSet.

**Problem**

« functie-ID » is not a rendering of « identifiant métier » — it reads as the identifier of a function, a different thing. « Unieke » carries the same contradiction with `Suggested Max = *` as the French.

**Proposed**

> identificatie die door het bronsysteem wordt toegekend om een CareSet-instantie ondubbelzinnig aan te duiden binnen haar functionele context

```decision F-028
status: revise        # accept | reject | revise
fr:
nl: identificatie die een CareSet-instantie aanduidt en uniek is binnen de naamruimte van het systeem dat haar toekent
en:
comment: Reviewer's ruling: there can be many identifiers, each unique within its own space. Max = * stays; the definition drops the bare claim of uniqueness and states the scope in which each identifier is unique, which is what resolves the contradiction.
```

### F-029 - `Business Identifier` (row 8) - EN

**Rules:** - / **Severity:** missing

**Problem**

No EN definition exists: the term is absent from both `ClinicalGlossary.csv` and `OperationalGlossary.csv`, so an active term is published with no English entry.

**Proposed**

> identifier assigned by the source system to designate one CareSet instance unambiguously within its business context

```decision F-029
status: revise        # accept | reject | revise
fr:
nl:
en: identifier that designates a CareSet instance and is unique within the namespace of the system that assigns it
comment: Reviewer's ruling: there can be many identifiers, each unique within its own space. Max = * stays; the definition drops the bare claim of uniqueness and states the scope in which each identifier is unique, which is what resolves the contradiction.
```

---

### F-030 - `Category` (row 9) - FR

**Rules:** 1 (substitution), 7 (no requirements/examples), 8 (necessary and sufficient) / **Severity:** major

**Current**

> Un attribut de classification d’un élément de données dans un CareSet, défini par une ValueSet standardisée, permettant de regrouper les informations selon leur signification clinique ou fonctionnelle dans le modèle logique belge

**Problem**

Opens with an article and runs to a full clause; « défini par une ValueSet standardisée » is an implementation requirement rather than a characteristic of the concept; and « dans le modèle logique belge » narrows a generic concept to one jurisdiction, which would make the definition false anywhere else it is reused.

**Proposed**

> attribut classant un élément de données selon sa signification clinique ou fonctionnelle, permettant d'en regrouper les occurrences

**Move to the `Description` column:** Les valeurs autorisées sont fixées par un ValueSet standardisé. Sert d'instrument de recherche et de regroupement (métadonnée).

**Note:** The sheet writes « une ValueSet » here and « un ValueSet » elsewhere; pick one gender across the glossary.

```decision F-030
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Reviewer's ruling: the classification reading is the real one, so EN moves onto it. Proposals taken as drafted; the ValueSet and 'modèle logique belge' material moves to the Description column.
```

### F-031 - `Category` (row 9) - NL

**Rules:** 1 (substitution), 7 (no requirements/examples), 8 (necessary and sufficient) / **Severity:** major

**Current**

> Een classificatieattribuut van een gegevenselement in een CareSet, gedefinieerd door een gestandaardiseerde ValueSet, waarmee informatie kan worden gegroepeerd op basis van de klinische of functionele betekenis ervan in het Belgische logische model

**Problem**

A faithful translation of a definition that breaches rules 1, 7 and 8 — so it breaches them too. `Description NL` is also empty, so there is nowhere the removed material currently lands.

**Proposed**

> attribuut dat een gegevenselement indeelt naar zijn klinische of functionele betekenis, waardoor de voorkomens ervan gegroepeerd kunnen worden

**Move to the `Description` column:** De toegestane waarden worden vastgelegd door een gestandaardiseerde ValueSet. Dient als zoek- en groeperingsinstrument (metadata).

```decision F-031
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Reviewer's ruling: the classification reading is the real one, so EN moves onto it. Proposals taken as drafted; the ValueSet and 'modèle logique belge' material moves to the Description column.
```

### F-032 - `Category` (row 9) - EN

**Rules:** 8 (necessary and sufficient), 10 (concept-system consistency) / **Severity:** major

**Current**

> Element that specifies the context of use of the information

**Problem**

Says something else entirely: FR and NL define a classification attribute used for grouping, EN defines a context of use. Two concepts under one term, and neither reader can tell which is authoritative.

**Proposed**

> attribute classifying a data element by its clinical or functional meaning, allowing its occurrences to be grouped

```decision F-032
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Reviewer's ruling: the classification reading is the real one, so EN moves onto it. Proposals taken as drafted; the ValueSet and 'modèle logique belge' material moves to the Description column.
```

---

### F-033 - `ClinicalStatus` (row 10) - FR

**Rules:** 1 (substitution), 3 (non-circularity) / **Severity:** major

**Current**

> Indique le statut de la pertinance clinique

**Problem**

Verb-initial, so it fails the substitution test, and it defines *ClinicalStatus* as « le statut … clinique ». « pertinance » is a misspelling of « pertinence ».

**Proposed**

> état rendant compte de l'actualité clinique de l'information enregistrée

**Note:** `Description FR` lists « completed » among the values; that is a lifecycle value belonging to `Statut`, not a clinical-relevance one.

```decision F-033
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

### F-034 - `ClinicalStatus` (row 10) - NL

**Rules:** 1 (substitution), 3 (non-circularity) / **Severity:** major

**Current**

> Geeft de status van de klinische relevantie aan

**Problem**

Verb construction that cannot substitute for the term, and it defines *ClinicalStatus* as « de status … klinische ». `Description NL` is empty, so the permitted values appear in FR only.

**Proposed**

> toestand die de klinische actualiteit van de geregistreerde informatie weergeeft

**Move to the `Description` column:** Bijvoorbeeld: active, inactive, resolved, entered-in-error.

```decision F-034
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

### F-035 - `ClinicalStatus` (row 10) - EN

**Rules:** 1 (substitution), 3 (non-circularity), 7 (no requirements/examples) / **Severity:** major

**Current**

> Indicates the clinical relevance status. E.g., active, inactive, completed, entered-in-error

**Problem**

Verb-initial, restates the term, and carries its value list inside the definition.

**Proposed**

> state expressing the clinical currency of the recorded information

**Move to the `Description` column:** For example: active, inactive, resolved, entered-in-error.

```decision F-035
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

---

### F-036 - `Code` (row 11) - FR

**Rules:** 1 (substitution), 4 (genus + differentia) / **Severity:** major

**Current**

> Décrit le concept clinique de l'information partagée

**Problem**

Verb-initial and therefore not substitutable, and it has no genus: it says what the element does, not what it is.

**Proposed**

> valeur codée désignant le concept clinique auquel se rapporte l'information enregistrée

```decision F-036
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

### F-037 - `Code` (row 11) - NL

**Rules:** 1 (substitution), 4 (genus + differentia) / **Severity:** major

**Current**

> Beschrijft het klinische concept van gedeelde informatie

**Problem**

Same as FR — a verb phrase describing the element's function rather than a noun phrase naming the concept.

**Proposed**

> gecodeerde waarde die het klinische concept aanduidt waarop de geregistreerde informatie betrekking heeft

```decision F-037
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

### F-038 - `Code` (row 11) - EN

**Rules:** 1 (substitution), 4 (genus + differentia) / **Severity:** major

**Current**

> Describes the clinical concept of the shared information

**Problem**

Same as FR and NL — verb-initial, no genus.

**Proposed**

> coded value designating the clinical concept to which the recorded information refers

```decision F-038
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

---

### F-039 - `Implantable Device` (row 12) - FR

**Rules:** 6 (one concept), 7 (no requirements/examples), 8 (necessary and sufficient) / **Severity:** major

**Current**

> Le dispositif médical qui est implanté, retiré ou manipulé d’une autre manière (par ex. calibration, remplacement de batterie, ajustement d’une prothèse, connexion d’un VAC pour plaie, etc.), et qui constitue un élément central de la procédure. Le lien s’effectue via une référence vers une ressource Device.

**Problem**

Three things in one cell: the concept, an inline example list, and an implementation instruction (« Le lien s'effectue via une référence vers une ressource Device »). The definition also describes a *role in a procedure* while the term names a *property of the device*, and « élément central de la procédure » is not a characteristic anyone can test.

**Proposed**

> dispositif médical destiné à demeurer dans le corps du patient, qui est posé, retiré ou modifié au cours de l'acte enregistré

**Move to the `Description` column:** Par exemple : calibration, remplacement de batterie, ajustement d'une prothèse, connexion d'un système VAC pour plaie. Le lien s'effectue via une référence vers une ressource Device.

```decision F-039
status: revise        # accept | reject | revise
fr: dispositif destiné à être introduit en totalité ou en partie dans le corps humain et à y demeurer après l'intervention
nl:
en:
comment: Reviewer's ruling, superseding the earlier subject-vs-instrument wording: Implantable Device is a TYPE of device (MDR 2017/745 sense), while Used device stays a ROLE. Rests on the new Device entry as its genus. Examples and the reference-to-Device sentence still move to the Description.
```

### F-040 - `Implantable Device` (row 12) - NL

**Rules:** 6 (one concept), 7 (no requirements/examples), 8 (necessary and sufficient) / **Severity:** major

**Current**

> "Het medisch hulpmiddel dat wordt geïmplanteerd, verwijderd of op een andere manier wordt gemanipuleerd

**Problem**

The cell is truncated mid-clause, opens with a stray double quote, and the rest of the sentence — including its closing parenthesis — has ended up in `Description NL`. As it stands the NL definition is not a complete phrase.

**Proposed**

> medisch hulpmiddel dat bestemd is om in het lichaam van de patiënt te blijven en dat tijdens de geregistreerde handeling wordt geplaatst, verwijderd of gewijzigd

**Move to the `Description` column:** Bijvoorbeeld: kalibratie, vervanging van de batterij, aanpassing van een prothese, aansluiting van een VAC-systeem voor wondverzorging. De koppeling gebeurt via een verwijzing naar een Device-resource.

```decision F-040
status: revise        # accept | reject | revise
fr:
nl: hulpmiddel dat bestemd is om geheel of gedeeltelijk in het menselijk lichaam te worden gebracht en daar na de ingreep te blijven
en:
comment: Reviewer's ruling, superseding the earlier subject-vs-instrument wording: Implantable Device is a TYPE of device (MDR 2017/745 sense), while Used device stays a ROLE. Rests on the new Device entry as its genus. Examples and the reference-to-Device sentence still move to the Description.
```

### F-041 - `Implantable Device` (row 12) - EN

**Rules:** - / **Severity:** missing

**Problem**

No EN definition exists in either glossary CSV for this active term.

**Proposed**

> medical device intended to remain in the patient's body, which is placed, removed or modified during the recorded act

```decision F-041
status: revise        # accept | reject | revise
fr:
nl:
en: device intended to be introduced wholly or partly into the human body and to remain there after the procedure
comment: Reviewer's ruling, superseding the earlier subject-vs-instrument wording: Implantable Device is a TYPE of device (MDR 2017/745 sense), while Used device stays a ROLE. Rests on the new Device entry as its genus. Examples and the reference-to-Device sentence still move to the Description.
```

---

### F-042 - `Lot Number` (row 13) - FR

**Rules:** 3 (non-circularity), 4 (genus + differentia) / **Severity:** major

**Current**

> N° de lot.

**Problem**

The definition is the term translated. No genus, no differentia, nothing saying who assigns it or what it identifies — and nothing separating it from `Series Number`.

**Proposed**

> identifiant attribué par le fabricant à l'ensemble des unités produites au cours d'un même cycle de fabrication

```decision F-042
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

### F-043 - `Lot Number` (row 13) - NL

**Rules:** 3 (non-circularity), 4 (genus + differentia) / **Severity:** major

**Current**

> Lot Nummer

**Problem**

The cell repeats the term, in English word order. It is not a definition.

**Proposed**

> identificatie die de fabrikant toekent aan alle eenheden die in eenzelfde productiecyclus zijn vervaardigd

```decision F-043
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

### F-044 - `Lot Number` (row 13) - EN

**Rules:** - / **Severity:** missing

**Problem**

No EN definition exists in either glossary CSV for this active term.

**Proposed**

> identifier assigned by the manufacturer to all units produced in the same manufacturing cycle

```decision F-044
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Approved by the reviewer. Fills a language with no entry at all; wording matches the siblings agreed for this term.
```

---

### F-045 - `Note` (row 14) - cross-cutting

**Rules:** 5 (positive formulation), 7 (no requirements/examples) / **Severity:** major

**Current**

> Une note n'est pas structurée. Il n'y a pas de VS associé. Une note ne contient pas de données sensibles. Ex: Niss du patient, Nom, etc…

**Problem**

The Description says a note contains no sensitive data and then offers, as examples, exactly the sensitive data it just excluded (national number, name). Read straight, it states the opposite of what it means — and since it is a rule, it has to be unambiguous.

**Proposed**

> Reword as a prohibition carrying its own examples: « Une note ne doit pas contenir de données identifiantes ou sensibles (par ex. NISS du patient, nom, adresse). »

```decision F-045
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Approved by the reviewer: reworded as a prohibition so the examples illustrate what is forbidden rather than what a note contains.
```

### F-046 - `Note` (row 14) - FR

**Rules:** 1 (substitution), 8 (necessary and sufficient) / **Severity:** minor

**Current**

> Informations complémentaires relative au contenu du CareSet en format texte libre.

**Problem**

« relative » does not agree with « Informations » (should be « relatives »), and « en format texte libre » dangles at the end rather than qualifying the information.

**Proposed**

> informations complémentaires relatives au contenu du CareSet, exprimées en texte libre

```decision F-046
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

### F-047 - `Note` (row 14) - NL

**Rules:** - / **Severity:** missing

**Problem**

`Définition NL` and `Description NL` are both empty for an active term.

**Proposed**

> aanvullende informatie over de inhoud van de CareSet, uitgedrukt in vrije tekst

**Move to the `Description` column:** Een note is niet gestructureerd en heeft geen bijbehorende ValueSet. Een note mag geen identificerende of gevoelige gegevens bevatten (bijv. NISS van de patiënt, naam, adres).

```decision F-047
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Approved by the reviewer. Fills a language with no entry at all; wording matches the siblings agreed for this term.
```

---

### F-048 - `Originating Request` (row 15) - FR

**Rules:** 3 (non-circularity), 8 (necessary and sufficient) / **Severity:** major

**Current**

> La demande qui est à l'origine de CareSet.

**Problem**

Restates the term (« Originating Request » → « la demande … à l'origine ») without adding a differentia, and « de CareSet » is missing its article. Nothing says what kind of request, or what relation it bears to the record.

**Proposed**

> demande de soins ou de prestation dont l'exécution est enregistrée par le CareSet

```decision F-048
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

### F-049 - `Originating Request` (row 15) - NL

**Rules:** 3 (non-circularity), 8 (necessary and sufficient) / **Severity:** major

**Current**

> De aanvraag die aan de basis ligt van CareSet.

**Problem**

Same restatement of the term as FR, and « van CareSet » is likewise missing its article.

**Proposed**

> aanvraag voor zorg of verstrekking waarvan de uitvoering door de CareSet wordt geregistreerd

```decision F-049
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

### F-050 - `Originating Request` (row 15) - EN

**Rules:** - / **Severity:** missing

**Problem**

No EN definition exists in either glossary CSV for this active term.

**Proposed**

> request for care or service whose execution is recorded by the CareSet

```decision F-050
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Approved by the reviewer. Fills a language with no entry at all; wording matches the siblings agreed for this term.
```

---

### F-051 - `PartOf` (row 16) - FR

**Rules:** 3 (non-circularity), 7 (no requirements/examples) / **Severity:** major

**Current**

> Le CareSet dont ce CareSet fait partie, soit le CareSet parent de ce CareSet. Ex: Une biopsie qui fait partie d'une intervention chirugicale

**Problem**

Defines *PartOf* with « fait partie », restates the same thing a second way after « soit », then gives an example inside the definition — an example already present, almost verbatim, in `Description FR`. « chirugicale » is misspelled.

**Proposed**

> CareSet englobant dont l'enregistrement courant constitue un composant

```decision F-051
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

### F-052 - `PartOf` (row 16) - NL

**Rules:** 3 (non-circularity) / **Severity:** major

**Current**

> De CareSet waarvan deze CareSet deel uitmaakt, oftewel de bovenliggende CareSet van deze CareSet.

**Problem**

Circular in the same way as FR, and the clause after « oftewel » only repeats the first in other words. No example leaks in here, so NL is otherwise the cleanest of the three.

**Proposed**

> omvattende CareSet waarvan de huidige registratie een onderdeel vormt

```decision F-052
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

### F-053 - `PartOf` (row 16) - EN

**Rules:** 3 (non-circularity), 7 (no requirements/examples) / **Severity:** major

**Current**

> The CareSet of which this CareSet is part, i.e., the parent CareSet of this CareSet. E.g., a biopsy that is part of a surgical intervention

**Problem**

Circular, restated after “i.e.”, and closes with an example inside the definition.

**Proposed**

> encompassing CareSet of which the current record forms a component

**Move to the `Description` column:** For example: a biopsy that is part of a surgical intervention.

```decision F-053
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

---

### F-054 - `Patient` (row 17) - FR

**Rules:** 9 (understandable terms) / **Severity:** major

**Current**

> La personne qui est l'objet des soins de santé auxquels l'enregistrement (<CareSet>) fait réference.

**Problem**

The angle-bracket placeholder `<CareSet>` is a template marker left in the text, and « réference » is misspelled. The substance is sound.

**Proposed**

> personne qui fait l'objet des soins de santé auxquels se rapporte l'enregistrement

```decision F-054
status: revise        # accept | reject | revise
fr: La personne qui est l'objet des soins de santé auxquels le CareSet fait référence.
nl:
en:
comment: Reviewer's wording. Drops the parenthetical gloss and refers to the CareSet directly.
```

### F-055 - `Patient` (row 17) - NL

**Rules:** 9 (understandable terms) / **Severity:** minor

**Current**

> De persoon op wie de gezondheidszorg betrekking heeft waarnaar de registratie (<CareSet>) verwijst.

**Problem**

Same leftover `<CareSet>` placeholder; otherwise a faithful and well-formed rendering.

**Proposed**

> persoon op wie de zorg betrekking heeft waarnaar de registratie verwijst

```decision F-055
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

---

### F-056 - `Performer` (row 18) - FR

**Rules:** 8 (necessary and sufficient), 9 (understandable terms) / **Severity:** major

**Current**

> Le professionnel de la santé qui a <fait l'action en fonction du <CareSet> .

**Problem**

Two unbalanced `<` template markers make the cell read as broken template text. « en fonction du CareSet » is also the wrong relation: the Performer performs the act that the CareSet records, not an act determined by it.

**Proposed**

> professionnel de la santé qui a réalisé l'acte enregistré par le CareSet

**Note:** Check whether a non-professional can be a Performer — a patient self-administering a vaccine, for instance. If so the genus should widen to « personne » and the professional case become a characteristic.

```decision F-056
status: revise        # accept | reject | revise
fr: personne qui a réalisé l'acte enregistré par le CareSet
nl:
en:
comment: Reviewer's ruling: the Performer is not necessarily a healthcare professional - self-administration and informal carers are in scope - so the genus widens to 'person' and the professional case moves to the Description as a characteristic.
```

### F-057 - `Performer` (row 18) - NL

**Rules:** 9 (understandable terms) / **Severity:** major

**Current**

> De zorgverlener die <de handeling heeft uitgevoerd op basis van de CareSet>

**Problem**

The same leftover template markers, here wrapping the whole predicate, and « op basis van » repeats the wrong relation found in the French.

**Proposed**

> zorgverlener die de door de CareSet geregistreerde handeling heeft uitgevoerd

```decision F-057
status: revise        # accept | reject | revise
fr:
nl: persoon die de door de CareSet geregistreerde handeling heeft uitgevoerd
en:
comment: Reviewer's ruling: the Performer is not necessarily a healthcare professional - self-administration and informal carers are in scope - so the genus widens to 'person' and the professional case moves to the Description as a characteristic. Supersedes the earlier batched accept on this finding.
```

### F-058 - `Performer` (row 18) - EN

**Rules:** 7 (no requirements/examples) / **Severity:** major

**Current**

> The healthcare professional who performed the action according to the CareSet (e.g., administered the vaccine, performed the observation, ...)

**Problem**

The parenthesised examples belong in a note to entry, not in the definition; “according to the CareSet” carries the same wrong relation as FR and NL.

**Proposed**

> healthcare professional who performed the act recorded by the CareSet

**Move to the `Description` column:** For example: administered the vaccine, performed the observation.

```decision F-058
status: revise        # accept | reject | revise
fr:
nl:
en: person who performed the act recorded by the CareSet
comment: Reviewer's ruling: the Performer is not necessarily a healthcare professional - self-administration and informal carers are in scope - so the genus widens to 'person' and the professional case moves to the Description as a characteristic. Supersedes the earlier batched accept on this finding. The examples still move to the Description.
```

---

### F-059 - `RecordedDate` (row 19) - FR

**Rules:** 6 (one concept), 10 (concept-system consistency) / **Severity:** major

**Current**

> Date d'encodage de l'enregistrement par l'Author ou le Recorder.

**Problem**

« l'Author ou le Recorder » offers two roles as alternatives, but row 4 declares `Recorder` a *synonym* of `Author` — the two statements cannot both hold. Initial capital and final period are also out of style.

**Proposed**

> date à laquelle l'enregistrement a été saisi par l'Author

```decision F-059
status: revise        # accept | reject | revise
fr: date à laquelle l'enregistrement a été saisi par le Recorder
nl:
en:
comment: Derived from the F-012 ruling that Recorder is the main term: the definition names the Recorder rather than 'l'Author ou le Recorder'. Otherwise the drafted proposal.
```

### F-060 - `RecordedDate` (row 19) - NL

**Rules:** 6 (one concept), 9 (understandable terms), 10 (concept-system consistency) / **Severity:** major

**Current**

> Datum waarop het record door de Author of de Recorder is ingevoerd

**Problem**

Same Author/Recorder contradiction. « het record » is also an anglicism where the rest of the NL column uses « de registratie », so sibling entries stop reading as siblings.

**Proposed**

> datum waarop de registratie door de Author is ingevoerd

```decision F-060
status: revise        # accept | reject | revise
fr:
nl: datum waarop de registratie door de Recorder is ingevoerd
en:
comment: Derived from the F-012 ruling that Recorder is the main term: the definition names the Recorder rather than 'l'Author ou le Recorder'. Otherwise the drafted proposal.
```

### F-061 - `RecordedDate` (row 19) - EN

**Rules:** 1 (substitution), 7 (no requirements/examples) / **Severity:** major

**Current**

> Recording date by the Author or Recorder (date of last update). Enables CareSet history management via the Business Identifier - RecordedDate pair, which ensures access to the latest version of the content

**Problem**

The second sentence explains what the field enables — historisation through the Business Identifier / RecordedDate pair — which is design rationale, not a characteristic of the concept. FR and NL keep it in the Description column.

**Proposed**

> date on which the record was entered by the Author

**Move to the `Description` column:** Date of last update. Enables CareSet history management through the Business Identifier / RecordedDate pair, which ensures access to the latest version of the content.

```decision F-061
status: revise        # accept | reject | revise
fr:
nl:
en: date on which the record was entered by the Recorder
comment: Derived from the F-012 ruling that Recorder is the main term: the definition names the Recorder rather than 'l'Author ou le Recorder'. Otherwise the drafted proposal.
```

---

### F-062 - `Route` (row 20) - FR

**Rules:** 1 (substitution), 3 (non-circularity) / **Severity:** major

**Current**

> Est la voie d’administration par laquelle un produit est mis en contact avec l’organisme.

**Problem**

Opens with « Est la » — a sentence predicate, which fails the substitution test outright. It also restates the term: `Route` *is* « la voie d'administration ».

**Proposed**

> voie par laquelle un produit est mis en contact avec l'organisme

```decision F-062
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

### F-063 - `Route` (row 20) - NL

**Rules:** 1 (substitution), 3 (non-circularity) / **Severity:** major

**Current**

> Dit is de toedieningsweg waarmee een product in contact komt met het lichaam.

**Problem**

Opens with « Dit is de … », the same substitution failure as FR, and restates the term as « toedieningsweg ».

**Proposed**

> weg waarlangs een product in contact wordt gebracht met het lichaam

```decision F-063
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

### F-064 - `Route` (row 20) - EN

**Rules:** 3 (non-circularity), 7 (no requirements/examples) / **Severity:** major

**Current**

> The route of administration by which a product is brought into contact with the body. See ValueSet VS_Route

**Problem**

Defines *Route* as “the route of administration”, and closes with a pointer to a ValueSet — guidance, which belongs in the Description column where FR and NL keep it.

**Proposed**

> path by which a product is brought into contact with the body

**Move to the `Description` column:** See ValueSet VS_Route.

```decision F-064
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

---

### F-065 - `Series Number` (row 21) - cross-cutting

**Rules:** 9 (understandable terms), 10 (concept-system consistency) / **Severity:** major

**Current**

> Series Number

**Problem**

A *series number* names a series; what both definitions and the note describe is the manufacturer's identifier of one individual device — a *serial* number. The English name states the wrong concept, and it is the name an implementer will map from.

**Proposed**

> Rename the item to `Serial Number`.

```decision F-065
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Approved by the reviewer: rename to Serial Number (code SerialNumber). No GlossaryCode in glossary_mappings.csv points at this item, so nothing downstream breaks.
```

### F-066 - `Series Number` (row 21) - FR

**Rules:** 3 (non-circularity), 4 (genus + differentia) / **Severity:** major

**Current**

> N° de série de l’appareil

**Problem**

The term restated. No genus, nothing about who assigns the number, and — critically — nothing saying it identifies one individual device rather than a production run, which is the only thing separating it from `Lot Number`.

**Proposed**

> identifiant attribué par le fabricant à un exemplaire déterminé d'un dispositif

```decision F-066
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

### F-067 - `Series Number` (row 21) - NL

**Rules:** 3 (non-circularity), 4 (genus + differentia) / **Severity:** major

**Current**

> Serienummer van het apparaat

**Problem**

The term restated, with the same missing differentia against `Lot Number`.

**Proposed**

> identificatie die de fabrikant toekent aan één welbepaald exemplaar van een hulpmiddel

**Note:** `Description NL` (« alleen voor één apparaat » — only for one device) mistranslates `Description FR` (« pour un appareil uniquement » — for a device only); it should say the element applies to devices only.

```decision F-067
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

### F-068 - `Series Number` (row 21) - EN

**Rules:** - / **Severity:** missing

**Problem**

No EN definition exists in either glossary CSV for this active term.

**Proposed**

> identifier assigned by the manufacturer to one individual device

```decision F-068
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Approved by the reviewer. Fills a language with no entry at all; wording matches the siblings agreed for this term.
```

---

### F-069 - `Statut` (row 22) - cross-cutting

**Rules:** 10 (concept-system consistency) / **Severity:** major

**Current**

> Statut

**Problem**

The item name is in French while every other item in the sheet is named in English. A single French name in an English item list breaks the naming consistency of the concept system, and the FR, NL and EN definitions all render the concept as *status* anyway.

**Proposed**

> Rename the item to `Status`.

**Note:** Renaming touches `DataDictionary`, the generated CodeSystems and `glossary_mappings.csv` — check those before applying.

```decision F-069
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Approved by the reviewer: rename to Status. glossary_mappings.csv already uses GlossaryCode 'Status' for this concept, so the rename makes the sheet agree with the mappings.
```

### F-070 - `Statut` (row 22) - FR

**Rules:** 1 (substitution), 3 (non-circularity) / **Severity:** major

**Current**

> Indique le statut de l’enregistrement, le moment dans le cycle de vie

**Problem**

Verb-initial, so not substitutable; defines *Statut* as « le statut »; and the two halves are juxtaposed by a comma with no grammatical link.

**Proposed**

> état de l'enregistrement dans son cycle de vie

```decision F-070
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

### F-071 - `Statut` (row 22) - NL

**Rules:** 1 (substitution), 3 (non-circularity) / **Severity:** major

**Current**

> Geeft de status van de registratie aan, het moment in de levenscyclus

**Problem**

Same verb construction, same restatement of the term, same comma splice as the French.

**Proposed**

> toestand van de registratie in haar levenscyclus

**Note:** `Description NL` also opens with the French abbreviation « Ex : » — use « Bijv. ».

```decision F-071
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

### F-072 - `Statut` (row 22) - EN

**Rules:** - / **Severity:** missing

**Problem**

No EN definition exists in either glossary CSV for this active term.

**Proposed**

> state of the record within its lifecycle

**Move to the `Description` column:** For example: final, corrected, cancelled, entered-in-error.

```decision F-072
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Approved by the reviewer. Fills a language with no entry at all; wording matches the siblings agreed for this term.
```

---

### F-073 - `Used device` (row 23) - FR

**Rules:** 7 (no requirements/examples), 9 (understandable terms) / **Severity:** major

**Current**

> Le dispositif médical qui est utilisé pour <CareSet>.

**Problem**

Leftover `<CareSet>` placeholder, and « utilisé pour » simply restates the term. The Description then carries a scoping rule (« Les petits instruments standard … ne sont pas enregistrés ») — correctly kept out of the definition, but it means the definition alone is too broad to be usable, and it must not be pulled in as a negative characteristic.

**Proposed**

> dispositif médical mis en œuvre pour réaliser l'acte enregistré

**Note:** The boundary with `Implantable Device` should be readable from the two definitions alone: that one is the device that remains in the body. The exclusion of small standard instruments (scalpels, syringes) is a requirement and stays in the Description.

```decision F-073
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Reviewer's ruling: instrument of the act, as against Implantable Device which is its subject. The drafted proposal already states exactly that, so taken as is. The exclusion of small standard instruments stays in the Description as a scoping requirement.
```

### F-074 - `Used device` (row 23) - NL

**Rules:** 9 (understandable terms) / **Severity:** major

**Current**

> Het medisch hulpmiddel dat wordt gebruikt voor <CareSet.

**Problem**

Broken placeholder — an unclosed `<CareSet.` — and the same restatement of the term as FR.

**Proposed**

> medisch hulpmiddel dat wordt ingezet om de geregistreerde handeling uit te voeren

**Note:** `Description NL` also drops the exclusion of small standard instruments and the reference-to-Device sentence that `Description FR` carries.

```decision F-074
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Reviewer's ruling: instrument of the act, as against Implantable Device which is its subject. The drafted proposal already states exactly that, so taken as is. The exclusion of small standard instruments stays in the Description as a scoping requirement.
```

### F-075 - `Used device` (row 23) - EN

**Rules:** - / **Severity:** missing

**Problem**

No EN definition exists in either glossary CSV for this active term.

**Proposed**

> medical device used to carry out the recorded act

```decision F-075
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Reviewer's ruling: instrument of the act, as against Implantable Device which is its subject. The drafted proposal already states exactly that, so taken as is. The exclusion of small standard instruments stays in the Description as a scoping requirement.
```

---

### F-076 - `VerificationStatus` (row 24) - cross-cutting

**Rules:** 10 (concept-system consistency) / **Severity:** major

**Current**

> Observation.Code : Tension artérielle (75367002) / Component.Code : 271649006 : Pression artérielle systolique, 271650006 : Pression artérielle diastolique […] Ce composant est uniquement utilisé pour les mesures de la tension artérielle […]

**Problem**

`Description FR` and `Description NL` for VerificationStatus contain blood-pressure component codes and an explanation of an Observation component. That has nothing to do with a verification status; it belongs to another entry and was pasted into the wrong row.

**Proposed**

> Remove it from VerificationStatus and restore it on the Observation-component entry it was written for.

```decision F-076
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.
```

### F-077 - `VerificationStatus` (row 24) - cross-cutting

**Rules:** 6 (one concept) / **Severity:** major

**Current**

> VerificationStatus — Synonym: Certainty

**Problem**

Verification status (confirmed / refuted / entered-in-error) and certainty (how confident the asserter is) are two concepts. Listing them as synonyms merges them into one entry — and the definitions currently follow the *certainty* reading while the term and its values follow the *verification* one.

**Proposed**

> Drop `Certainty` as a synonym. If a confidence element is genuinely needed, give it its own entry.

```decision F-077
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Approved by the reviewer: this is a verification status, not a certainty. The Certainty synonym is dropped and F-078/F-079/F-080 take the confirmation wording as drafted.
```

### F-078 - `VerificationStatus` (row 24) - FR

**Rules:** 1 (substitution), 3 (non-circularity) / **Severity:** major

**Current**

> Indique le niveau de certitude de l'enregistrement

**Problem**

Verb-initial. It also defines a *verification* status as a *certainty* level — the synonym problem in another form: the values this element carries (confirmed, refuted, entered-in-error) say whether an assertion has been verified, not how confident anyone is.

**Proposed**

> degré de confirmation attribué à l'information enregistrée

```decision F-078
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Follows the F-077 ruling: verification, not certainty. Proposal taken as drafted.
```

### F-079 - `VerificationStatus` (row 24) - NL

**Rules:** 1 (substitution), 3 (non-circularity), 9 (understandable terms) / **Severity:** major

**Current**

> Geeft de mate van zekerheid van de opname aan

**Problem**

Verb construction that cannot substitute for the term, and « opname » in a health context reads first as a hospital admission — the wrong concept. FR and EN both say *record*.

**Proposed**

> graad van bevestiging van de geregistreerde informatie

```decision F-079
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Follows the F-077 ruling: verification, not certainty. Proposal taken as drafted.
```

### F-080 - `VerificationStatus` (row 24) - EN

**Rules:** 1 (substitution), 7 (no requirements/examples) / **Severity:** major

**Current**

> Indicates the certainty level of the record. E.g., confirmed, suspected, entered-in-error, ...

**Problem**

Verb-initial, with the value list inside the definition. The values themselves (“confirmed”, “entered-in-error”) describe verification rather than certainty, which confirms the term/definition mismatch.

**Proposed**

> degree of confirmation assigned to the recorded information

**Move to the `Description` column:** For example: confirmed, unconfirmed, refuted, entered-in-error.

```decision F-080
status: accept        # accept | reject | revise
fr:
nl:
en:
comment: Follows the F-077 ruling: verification, not certainty. Proposal taken as drafted.
```
