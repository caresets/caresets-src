# Glossary definition changes - for approval

- Source review: `definition-quality-20260828_235034.md`
- Changes proposed: **83** / Rejected: **0** / Still open: **0**

Each change below has been reviewed and is put forward for approval. The full justification for every item - the rule it breaches and why - is in the source review report.

## Changes proposed

### `(template placeholders)`

**F-001 - META** (major, rules 9)

| | |
|--|--|
| Current | Patient (row 17): « l'enregistrement (<CareSet>) » · Performer (row 18): « qui a <fait l'action en fonction du <CareSet> » · Used device (row 23): « utilisé pour <CareSet>. » |
| **Proposed** | **Sweep the whole sheet — not only the Active rows — for `<` and `>` in the Definition and Description columns and resolve each one into real text.** |

> Sweep approved. The Patient row 17 wording drafted here has moved to F-054, which is the finding that writes to the cell; rows 18 and 23 are decided on their own findings.

### `(body-site items)`

**F-002 - META** (major, rules 8, 10)

| | |
|--|--|
| Current | *(none)* |
| **Proposed** | **Separate them explicitly — `BodyLocation` names the body part, `BodyTopoGraphy` names the position *within* that part. The per-language proposals below are written to that split.** |

> Split approved. It matches StructureDefinition-BeModelBodySite.json, where bodyLocation, bodyLaterality and bodyTopography are already three sibling 0..1 elements. Wording lands via F-019/F-020/F-021 and F-023/F-024/F-025.

### `(item naming)`

### `(status-like items)`

**F-004 - META** (minor, rules 10)

| | |
|--|--|
| Current | *(none)* |
| **Proposed** | **Give all three the same genus (« état … » / « toestand … » / “state …”) and let the differentia carry the distinction — lifecycle, clinical currency, verification. The per-language proposals below are written to do that.** |

> Approved by the reviewer. All three status items take a parallel genus; the differentia carries lifecycle vs clinical currency vs verification.

### `Device`

**F-081 - FR** (missing, rules 4, 9)

| | |
|--|--|
| Current | *(none)* |
| **Proposed** | **instrument, appareil, équipement, logiciel ou autre article destiné par son fabricant à être utilisé à des fins médicales chez l'être humain** |

> Approved by the reviewer: Device is added as an Active term so both Implantable Device and Used device have a defined genus. New row in the sheet plus a row in ClinicalGlossary.csv - no script writes it, since the term has no row yet.

**F-082 - NL** (missing, rules 4, 9)

| | |
|--|--|
| Current | *(none)* |
| **Proposed** | **instrument, toestel, apparaat, software of ander artikel dat door de fabrikant bestemd is om bij de mens voor medische doeleinden te worden gebruikt** |

> Approved by the reviewer: Device is added as an Active term so both Implantable Device and Used device have a defined genus. New row in the sheet plus a row in ClinicalGlossary.csv - no script writes it, since the term has no row yet.

**F-083 - EN** (missing, rules 4, 9)

| | |
|--|--|
| Current | *(none)* |
| **Proposed** | **instrument, apparatus, appliance, software or other article intended by its manufacturer to be used for medical purposes in human beings** |

> Approved by the reviewer: Device is added as an Active term so both Implantable Device and Used device have a defined genus. New row in the sheet plus a row in ClinicalGlossary.csv - no script writes it, since the term has no row yet.

### `AdministrationDate` (row 2)

**F-005 - FR** (minor, rules 1)

| | |
|--|--|
| Current | Date d’administration du produit / vaccin par le Performer. |
| **Proposed** | **date à laquelle un produit ou un vaccin est administré au patient par le Performer** |

**F-006 - NL** (minor, rules 1)

| | |
|--|--|
| Current | Datum waarop het product/vaccin door de Performer is toegediend. |
| **Proposed** | **datum waarop een product of vaccin door de Performer aan de patiënt is toegediend** |

**F-007 - EN** (major, rules 1, 7)

| | |
|--|--|
| Current | Date of administration of the vaccine or product. For vaccines, a life period may also be mentioned if exact dates are unknown (during childhood, adolescence...) |
| **Proposed** | **date on which a product or vaccine is administered to the patient by the Performer** |

### `Asserter` (row 3)

**F-008 - FR** (major, rules 8)

| | |
|--|--|
| Current | La personne à la source de l’information |
| **Proposed** | **personne qui rapporte l'information enregistrée dans le CareSet** |

> Reviewer's variant: 'rapporte' rather than 'est à la source de'. Settled with F-009 and F-010 so the three languages take the same reading, which also matches the element name Asserter. Knowingly diverges from FHIR's 'source of the information'.

**F-009 - NL** (major, rules 8, 10)

| | |
|--|--|
| Current | De persoon die de informatie verstrekt |
| **Proposed** | **persoon die de in de CareSet geregistreerde informatie rapporteert** |

> Reviewer's variant. NL keeps the reporting sense it already had rather than being pulled to 'source'; FR and EN move to match it.

**F-010 - EN** (major, rules 7, 8)

| | |
|--|--|
| Current | The person who is the source of the information (e.g., the patient, general practitioner, a relative, the professional recording the information themselves, ...) |
| **Proposed** | **person who reports the information recorded in the CareSet** |

> Reviewer's variant, same reading as F-008/F-009. The examples still move out of the definition into the Description column as proposed.

### `Author` (row 4)

**F-011 - META** (major, rules 8, 10)

| | |
|--|--|
| Current | Toutefois, lorsqu'il s'agit d'un parent ou proche, seul le rôle sera encodé (ex : père, mère, voisin, aidant-proche, ami, …) pour répondre aux exigences RGPD. […] on utilisera le ValueSet « VS_PatientRelationshipType » […] |
| **Proposed** | **Delete the copied block from Author's Description. If a note is needed there, describe how the Author is identified (NISS / BIS / NIHDI number), as `Performer` does.** |

> Delete and replace, per the reviewer. The copied Asserter block goes; in its place a note on how the Author is identified (NISS / BIS / NIHDI number), parallel to what Performer's Description already carries.

**F-013 - FR** (major, rules 3, 6)

| | |
|--|--|
| Current | le professionnel de la santé qui encode et prend la responsabilité du contenu encodé. |
| **Proposed** | **professionnel de la santé qui enregistre le contenu du CareSet et en assume la responsabilité** |

> Reviewer's variant, following the F-012 ruling that Recorder/Author is one concept: both characteristics are kept - recording the content and being responsible for it - and only the circular repetition is removed.

**F-014 - NL** (major, rules 3, 6)

| | |
|--|--|
| Current | de zorgverlener die de gegevens invoert en de verantwoordelijkheid draagt voor de ingevoerde inhoud. |
| **Proposed** | **zorgverlener die de inhoud van de CareSet vastlegt en er de verantwoordelijkheid voor draagt** |

> Reviewer's variant, following the F-012 ruling that Recorder/Author is one concept: both characteristics are kept - recording the content and being responsible for it - and only the circular repetition is removed.

**F-015 - EN** (minor, rules 10)

| | |
|--|--|
| Current | The healthcare professional who takes responsibility for the recorded content |
| **Proposed** | **healthcare professional who records the content of the CareSet and takes responsibility for it** |

> Reviewer's variant, following the F-012 ruling that Recorder/Author is one concept: both characteristics are kept - recording the content and being responsible for it - and only the circular repetition is removed.

### `BodyLaterality` (row 5)

**F-016 - FR** (major, rules 3, 4)

| | |
|--|--|
| Current | la latéralité du corps . |
| **Proposed** | **côté du corps auquel se rapporte l'information enregistrée** |

**F-017 - NL** (major, rules 3, 9, 10)

| | |
|--|--|
| Current | de zijdelingse oriëntatie van het lichaam |
| **Proposed** | **zijde van het lichaam waarop de geregistreerde informatie betrekking heeft** |

**F-018 - EN** (major, rules 1, 3, 7)

| | |
|--|--|
| Current | Specifies the body laterality (right, left, both) |
| **Proposed** | **side of the body to which the recorded information refers** |

### `BodyLocation` (row 6)

**F-019 - FR** (major, rules 3, 4, 8)

| | |
|--|--|
| Current | l'endroit du corps. |
| **Proposed** | **partie du corps à laquelle se rapporte l'information enregistrée** |

**F-020 - NL** (major, rules 3, 4, 8)

| | |
|--|--|
| Current | het lichaamsdeel |
| **Proposed** | **lichaamsdeel waarop de geregistreerde informatie betrekking heeft** |

**F-021 - EN** (major, rules 1, 3, 7)

| | |
|--|--|
| Current | Indicates the body location (head, leg, femur, heart, ...) |
| **Proposed** | **part of the body to which the recorded information refers** |

### `BodyTopoGraphy` (row 7)

**F-022 - META** (minor, rules 10)

| | |
|--|--|
| Current | BodyTopoGraphy |
| **Proposed** | **Rename the item to `BodyTopography`.** |

> Confirmed by the reviewer. `bodyTopography` is also how the element is spelled in StructureDefinition-BeModelBodySite.json, so the sheet is the outlier.

**F-023 - FR** (major, rules 6, 8, 10)

| | |
|--|--|
| Current | La localisation ou la position relative sur l'endroit corps |
| **Proposed** | **position relative, à l'intérieur de la partie du corps concernée, du siège de l'information enregistrée** |

> Reviewer's variant: same split as proposed, but phrased without the word 'structure', so the definition does not imply an anatomical structure is always what is being located.

**F-024 - NL** (major, rules 6, 8, 10)

| | |
|--|--|
| Current | De locatie of de relatieve positie op het lichaam, |
| **Proposed** | **relatieve positie, binnen het betrokken lichaamsdeel, van de plaats waarop de geregistreerde informatie betrekking heeft** |

> Reviewer's variant: same split as proposed, but phrased without the word 'structure', so the definition does not imply an anatomical structure is always what is being located.

**F-025 - EN** (major, rules 1, 6, 7)

| | |
|--|--|
| Current | Describes the location or relative position on the body, such as superior/inferior, medial/lateral or internal/external |
| **Proposed** | **relative position, within the body part concerned, of the site to which the recorded information refers** |

> Reviewer's variant: same split as proposed, but phrased without the word 'structure', so the definition does not imply an anatomical structure is always what is being located.

### `Business Identifier` (row 8)

**F-027 - FR** (major, rules 3, 8)

| | |
|--|--|
| Current | Identifiant métier unique d'une instance du CareSet. |
| **Proposed** | **identifiant qui désigne une instance de CareSet et qui est unique dans l'espace de nommage du système qui l'attribue** |

> Reviewer's ruling: there can be many identifiers, each unique within its own space. Max = * stays; the definition drops the bare claim of uniqueness and states the scope in which each identifier is unique, which is what resolves the contradiction.

**F-028 - NL** (major, rules 3, 8, 9)

| | |
|--|--|
| Current | Unieke functie-ID van een instantie van de CareSet. |
| **Proposed** | **identificatie die een CareSet-instantie aanduidt en uniek is binnen de naamruimte van het systeem dat haar toekent** |

> Reviewer's ruling: there can be many identifiers, each unique within its own space. Max = * stays; the definition drops the bare claim of uniqueness and states the scope in which each identifier is unique, which is what resolves the contradiction.

**F-029 - EN** (missing, rules -)

| | |
|--|--|
| Current | *(none)* |
| **Proposed** | **identifier that designates a CareSet instance and is unique within the namespace of the system that assigns it** |

> Reviewer's ruling: there can be many identifiers, each unique within its own space. Max = * stays; the definition drops the bare claim of uniqueness and states the scope in which each identifier is unique, which is what resolves the contradiction.

### `Category` (row 9)

**F-030 - FR** (major, rules 1, 7, 8)

| | |
|--|--|
| Current | Un attribut de classification d’un élément de données dans un CareSet, défini par une ValueSet standardisée, permettant de regrouper les informations selon leur signification clinique ou fonctionnelle dans le modèle logique belge |
| **Proposed** | **attribut classant un élément de données selon sa signification clinique ou fonctionnelle, permettant d'en regrouper les occurrences** |

> Reviewer's ruling: the classification reading is the real one, so EN moves onto it. Proposals taken as drafted; the ValueSet and 'modèle logique belge' material moves to the Description column.

**F-031 - NL** (major, rules 1, 7, 8)

| | |
|--|--|
| Current | Een classificatieattribuut van een gegevenselement in een CareSet, gedefinieerd door een gestandaardiseerde ValueSet, waarmee informatie kan worden gegroepeerd op basis van de klinische of functionele betekenis ervan in het Belgische logische model |
| **Proposed** | **attribuut dat een gegevenselement indeelt naar zijn klinische of functionele betekenis, waardoor de voorkomens ervan gegroepeerd kunnen worden** |

> Reviewer's ruling: the classification reading is the real one, so EN moves onto it. Proposals taken as drafted; the ValueSet and 'modèle logique belge' material moves to the Description column.

**F-032 - EN** (major, rules 8, 10)

| | |
|--|--|
| Current | Element that specifies the context of use of the information |
| **Proposed** | **attribute classifying a data element by its clinical or functional meaning, allowing its occurrences to be grouped** |

> Reviewer's ruling: the classification reading is the real one, so EN moves onto it. Proposals taken as drafted; the ValueSet and 'modèle logique belge' material moves to the Description column.

### `ClinicalStatus` (row 10)

**F-033 - FR** (major, rules 1, 3)

| | |
|--|--|
| Current | Indique le statut de la pertinance clinique |
| **Proposed** | **état rendant compte de l'actualité clinique de l'information enregistrée** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

**F-034 - NL** (major, rules 1, 3)

| | |
|--|--|
| Current | Geeft de status van de klinische relevantie aan |
| **Proposed** | **toestand die de klinische actualiteit van de geregistreerde informatie weergeeft** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

**F-035 - EN** (major, rules 1, 3, 7)

| | |
|--|--|
| Current | Indicates the clinical relevance status. E.g., active, inactive, completed, entered-in-error |
| **Proposed** | **state expressing the clinical currency of the recorded information** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

### `Code` (row 11)

**F-036 - FR** (major, rules 1, 4)

| | |
|--|--|
| Current | Décrit le concept clinique de l'information partagée |
| **Proposed** | **valeur codée désignant le concept clinique auquel se rapporte l'information enregistrée** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

**F-037 - NL** (major, rules 1, 4)

| | |
|--|--|
| Current | Beschrijft het klinische concept van gedeelde informatie |
| **Proposed** | **gecodeerde waarde die het klinische concept aanduidt waarop de geregistreerde informatie betrekking heeft** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

**F-038 - EN** (major, rules 1, 4)

| | |
|--|--|
| Current | Describes the clinical concept of the shared information |
| **Proposed** | **coded value designating the clinical concept to which the recorded information refers** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

### `Implantable Device` (row 12)

**F-039 - FR** (major, rules 6, 7, 8)

| | |
|--|--|
| Current | Le dispositif médical qui est implanté, retiré ou manipulé d’une autre manière (par ex. calibration, remplacement de batterie, ajustement d’une prothèse, connexion d’un VAC pour plaie, etc.), et qui constitue un élément central de la procédure. Le lien s’effectue via une référence vers une ressource Device. |
| **Proposed** | **dispositif destiné à être introduit en totalité ou en partie dans le corps humain et à y demeurer après l'intervention** |

> Reviewer's ruling, superseding the earlier subject-vs-instrument wording: Implantable Device is a TYPE of device (MDR 2017/745 sense), while Used device stays a ROLE. Rests on the new Device entry as its genus. Examples and the reference-to-Device sentence still move to the Description.

**F-040 - NL** (major, rules 6, 7, 8)

| | |
|--|--|
| Current | "Het medisch hulpmiddel dat wordt geïmplanteerd, verwijderd of op een andere manier wordt gemanipuleerd |
| **Proposed** | **hulpmiddel dat bestemd is om geheel of gedeeltelijk in het menselijk lichaam te worden gebracht en daar na de ingreep te blijven** |

> Reviewer's ruling, superseding the earlier subject-vs-instrument wording: Implantable Device is a TYPE of device (MDR 2017/745 sense), while Used device stays a ROLE. Rests on the new Device entry as its genus. Examples and the reference-to-Device sentence still move to the Description.

**F-041 - EN** (missing, rules -)

| | |
|--|--|
| Current | *(none)* |
| **Proposed** | **device intended to be introduced wholly or partly into the human body and to remain there after the procedure** |

> Reviewer's ruling, superseding the earlier subject-vs-instrument wording: Implantable Device is a TYPE of device (MDR 2017/745 sense), while Used device stays a ROLE. Rests on the new Device entry as its genus. Examples and the reference-to-Device sentence still move to the Description.

### `Lot Number` (row 13)

**F-042 - FR** (major, rules 3, 4)

| | |
|--|--|
| Current | N° de lot. |
| **Proposed** | **identifiant attribué par le fabricant à l'ensemble des unités produites au cours d'un même cycle de fabrication** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

**F-043 - NL** (major, rules 3, 4)

| | |
|--|--|
| Current | Lot Nummer |
| **Proposed** | **identificatie die de fabrikant toekent aan alle eenheden die in eenzelfde productiecyclus zijn vervaardigd** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

**F-044 - EN** (missing, rules -)

| | |
|--|--|
| Current | *(none)* |
| **Proposed** | **identifier assigned by the manufacturer to all units produced in the same manufacturing cycle** |

> Approved by the reviewer. Fills a language with no entry at all; wording matches the siblings agreed for this term.

### `Note` (row 14)

**F-045 - META** (major, rules 5, 7)

| | |
|--|--|
| Current | Une note n'est pas structurée. Il n'y a pas de VS associé. Une note ne contient pas de données sensibles. Ex: Niss du patient, Nom, etc… |
| **Proposed** | **Reword as a prohibition carrying its own examples: « Une note ne doit pas contenir de données identifiantes ou sensibles (par ex. NISS du patient, nom, adresse). »** |

> Approved by the reviewer: reworded as a prohibition so the examples illustrate what is forbidden rather than what a note contains.

**F-046 - FR** (minor, rules 1, 8)

| | |
|--|--|
| Current | Informations complémentaires relative au contenu du CareSet en format texte libre. |
| **Proposed** | **informations complémentaires relatives au contenu du CareSet, exprimées en texte libre** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

**F-047 - NL** (missing, rules -)

| | |
|--|--|
| Current | *(none)* |
| **Proposed** | **aanvullende informatie over de inhoud van de CareSet, uitgedrukt in vrije tekst** |

> Approved by the reviewer. Fills a language with no entry at all; wording matches the siblings agreed for this term.

### `Originating Request` (row 15)

**F-048 - FR** (major, rules 3, 8)

| | |
|--|--|
| Current | La demande qui est à l'origine de CareSet. |
| **Proposed** | **demande de soins ou de prestation dont l'exécution est enregistrée par le CareSet** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

**F-049 - NL** (major, rules 3, 8)

| | |
|--|--|
| Current | De aanvraag die aan de basis ligt van CareSet. |
| **Proposed** | **aanvraag voor zorg of verstrekking waarvan de uitvoering door de CareSet wordt geregistreerd** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

**F-050 - EN** (missing, rules -)

| | |
|--|--|
| Current | *(none)* |
| **Proposed** | **request for care or service whose execution is recorded by the CareSet** |

> Approved by the reviewer. Fills a language with no entry at all; wording matches the siblings agreed for this term.

### `PartOf` (row 16)

**F-051 - FR** (major, rules 3, 7)

| | |
|--|--|
| Current | Le CareSet dont ce CareSet fait partie, soit le CareSet parent de ce CareSet. Ex: Une biopsie qui fait partie d'une intervention chirugicale |
| **Proposed** | **CareSet englobant dont l'enregistrement courant constitue un composant** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

**F-052 - NL** (major, rules 3)

| | |
|--|--|
| Current | De CareSet waarvan deze CareSet deel uitmaakt, oftewel de bovenliggende CareSet van deze CareSet. |
| **Proposed** | **omvattende CareSet waarvan de huidige registratie een onderdeel vormt** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

**F-053 - EN** (major, rules 3, 7)

| | |
|--|--|
| Current | The CareSet of which this CareSet is part, i.e., the parent CareSet of this CareSet. E.g., a biopsy that is part of a surgical intervention |
| **Proposed** | **encompassing CareSet of which the current record forms a component** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

### `Patient` (row 17)

**F-054 - FR** (major, rules 9)

| | |
|--|--|
| Current | La personne qui est l'objet des soins de santé auxquels l'enregistrement (<CareSet>) fait réference. |
| **Proposed** | **La personne qui est l'objet des soins de santé auxquels le CareSet fait référence.** |

> Reviewer's wording. Drops the parenthetical gloss and refers to the CareSet directly.

**F-055 - NL** (minor, rules 9)

| | |
|--|--|
| Current | De persoon op wie de gezondheidszorg betrekking heeft waarnaar de registratie (<CareSet>) verwijst. |
| **Proposed** | **persoon op wie de zorg betrekking heeft waarnaar de registratie verwijst** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

### `Performer` (row 18)

**F-056 - FR** (major, rules 8, 9)

| | |
|--|--|
| Current | Le professionnel de la santé qui a <fait l'action en fonction du <CareSet> . |
| **Proposed** | **personne qui a réalisé l'acte enregistré par le CareSet** |

> Reviewer's ruling: the Performer is not necessarily a healthcare professional - self-administration and informal carers are in scope - so the genus widens to 'person' and the professional case moves to the Description as a characteristic.

**F-057 - NL** (major, rules 9)

| | |
|--|--|
| Current | De zorgverlener die <de handeling heeft uitgevoerd op basis van de CareSet> |
| **Proposed** | **persoon die de door de CareSet geregistreerde handeling heeft uitgevoerd** |

> Reviewer's ruling: the Performer is not necessarily a healthcare professional - self-administration and informal carers are in scope - so the genus widens to 'person' and the professional case moves to the Description as a characteristic. Supersedes the earlier batched accept on this finding.

**F-058 - EN** (major, rules 7)

| | |
|--|--|
| Current | The healthcare professional who performed the action according to the CareSet (e.g., administered the vaccine, performed the observation, ...) |
| **Proposed** | **person who performed the act recorded by the CareSet** |

> Reviewer's ruling: the Performer is not necessarily a healthcare professional - self-administration and informal carers are in scope - so the genus widens to 'person' and the professional case moves to the Description as a characteristic. Supersedes the earlier batched accept on this finding. The examples still move to the Description.

### `RecordedDate` (row 19)

**F-059 - FR** (major, rules 6, 10)

| | |
|--|--|
| Current | Date d'encodage de l'enregistrement par l'Author ou le Recorder. |
| **Proposed** | **date à laquelle l'enregistrement a été saisi par le Recorder** |

> Derived from the F-012 ruling that Recorder is the main term: the definition names the Recorder rather than 'l'Author ou le Recorder'. Otherwise the drafted proposal.

**F-060 - NL** (major, rules 6, 9, 10)

| | |
|--|--|
| Current | Datum waarop het record door de Author of de Recorder is ingevoerd |
| **Proposed** | **datum waarop de registratie door de Recorder is ingevoerd** |

> Derived from the F-012 ruling that Recorder is the main term: the definition names the Recorder rather than 'l'Author ou le Recorder'. Otherwise the drafted proposal.

**F-061 - EN** (major, rules 1, 7)

| | |
|--|--|
| Current | Recording date by the Author or Recorder (date of last update). Enables CareSet history management via the Business Identifier - RecordedDate pair, which ensures access to the latest version of the content |
| **Proposed** | **date on which the record was entered by the Recorder** |

> Derived from the F-012 ruling that Recorder is the main term: the definition names the Recorder rather than 'l'Author ou le Recorder'. Otherwise the drafted proposal.

### `Route` (row 20)

**F-062 - FR** (major, rules 1, 3)

| | |
|--|--|
| Current | Est la voie d’administration par laquelle un produit est mis en contact avec l’organisme. |
| **Proposed** | **voie par laquelle un produit est mis en contact avec l'organisme** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

**F-063 - NL** (major, rules 1, 3)

| | |
|--|--|
| Current | Dit is de toedieningsweg waarmee een product in contact komt met het lichaam. |
| **Proposed** | **weg waarlangs een product in contact wordt gebracht met het lichaam** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

**F-064 - EN** (major, rules 3, 7)

| | |
|--|--|
| Current | The route of administration by which a product is brought into contact with the body. See ValueSet VS_Route |
| **Proposed** | **path by which a product is brought into contact with the body** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

### `Series Number` (row 21)

**F-065 - META** (major, rules 9, 10)

| | |
|--|--|
| Current | Series Number |
| **Proposed** | **Rename the item to `Serial Number`.** |

> Approved by the reviewer: rename to Serial Number (code SerialNumber). No GlossaryCode in glossary_mappings.csv points at this item, so nothing downstream breaks.

**F-066 - FR** (major, rules 3, 4)

| | |
|--|--|
| Current | N° de série de l’appareil |
| **Proposed** | **identifiant attribué par le fabricant à un exemplaire déterminé d'un dispositif** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

**F-067 - NL** (major, rules 3, 4)

| | |
|--|--|
| Current | Serienummer van het apparaat |
| **Proposed** | **identificatie die de fabrikant toekent aan één welbepaald exemplaar van een hulpmiddel** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

**F-068 - EN** (missing, rules -)

| | |
|--|--|
| Current | *(none)* |
| **Proposed** | **identifier assigned by the manufacturer to one individual device** |

> Approved by the reviewer. Fills a language with no entry at all; wording matches the siblings agreed for this term.

### `Statut` (row 22)

**F-069 - META** (major, rules 10)

| | |
|--|--|
| Current | Statut |
| **Proposed** | **Rename the item to `Status`.** |

> Approved by the reviewer: rename to Status. glossary_mappings.csv already uses GlossaryCode 'Status' for this concept, so the rename makes the sheet agree with the mappings.

**F-070 - FR** (major, rules 1, 3)

| | |
|--|--|
| Current | Indique le statut de l’enregistrement, le moment dans le cycle de vie |
| **Proposed** | **état de l'enregistrement dans son cycle de vie** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

**F-071 - NL** (major, rules 1, 3)

| | |
|--|--|
| Current | Geeft de status van de registratie aan, het moment in de levenscyclus |
| **Proposed** | **toestand van de registratie in haar levenscyclus** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

**F-072 - EN** (missing, rules -)

| | |
|--|--|
| Current | *(none)* |
| **Proposed** | **state of the record within its lifecycle** |

> Approved by the reviewer. Fills a language with no entry at all; wording matches the siblings agreed for this term.

### `Used device` (row 23)

**F-073 - FR** (major, rules 7, 9)

| | |
|--|--|
| Current | Le dispositif médical qui est utilisé pour <CareSet>. |
| **Proposed** | **dispositif médical mis en œuvre pour réaliser l'acte enregistré** |

> Reviewer's ruling: instrument of the act, as against Implantable Device which is its subject. The drafted proposal already states exactly that, so taken as is. The exclusion of small standard instruments stays in the Description as a scoping requirement.

**F-074 - NL** (major, rules 9)

| | |
|--|--|
| Current | Het medisch hulpmiddel dat wordt gebruikt voor <CareSet. |
| **Proposed** | **medisch hulpmiddel dat wordt ingezet om de geregistreerde handeling uit te voeren** |

> Reviewer's ruling: instrument of the act, as against Implantable Device which is its subject. The drafted proposal already states exactly that, so taken as is. The exclusion of small standard instruments stays in the Description as a scoping requirement.

**F-075 - EN** (missing, rules -)

| | |
|--|--|
| Current | *(none)* |
| **Proposed** | **medical device used to carry out the recorded act** |

> Reviewer's ruling: instrument of the act, as against Implantable Device which is its subject. The drafted proposal already states exactly that, so taken as is. The exclusion of small standard instruments stays in the Description as a scoping requirement.

### `VerificationStatus` (row 24)

**F-076 - META** (major, rules 10)

| | |
|--|--|
| Current | Observation.Code : Tension artérielle (75367002) / Component.Code : 271649006 : Pression artérielle systolique, 271650006 : Pression artérielle diastolique […] Ce composant est uniquement utilisé pour les mesures de la tension artérielle […] |
| **Proposed** | **Remove it from VerificationStatus and restore it on the Observation-component entry it was written for.** |

> Batched by the reviewer as a mechanical fix: the proposal is taken as drafted. Reversible - set this back to pending or reject and re-run the export.

**F-077 - META** (major, rules 6)

| | |
|--|--|
| Current | VerificationStatus — Synonym: Certainty |
| **Proposed** | **Drop `Certainty` as a synonym. If a confidence element is genuinely needed, give it its own entry.** |

> Approved by the reviewer: this is a verification status, not a certainty. The Certainty synonym is dropped and F-078/F-079/F-080 take the confirmation wording as drafted.

**F-078 - FR** (major, rules 1, 3)

| | |
|--|--|
| Current | Indique le niveau de certitude de l'enregistrement |
| **Proposed** | **degré de confirmation attribué à l'information enregistrée** |

> Follows the F-077 ruling: verification, not certainty. Proposal taken as drafted.

**F-079 - NL** (major, rules 1, 3, 9)

| | |
|--|--|
| Current | Geeft de mate van zekerheid van de opname aan |
| **Proposed** | **graad van bevestiging van de geregistreerde informatie** |

> Follows the F-077 ruling: verification, not certainty. Proposal taken as drafted.

**F-080 - EN** (major, rules 1, 7)

| | |
|--|--|
| Current | Indicates the certainty level of the record. E.g., confirmed, suspected, entered-in-error, ... |
| **Proposed** | **degree of confirmation assigned to the recorded information** |

> Follows the F-077 ruling: verification, not certainty. Proposal taken as drafted.

## Approval

| | Name | Date | Outcome |
|--|------|------|---------|
| Reviewer | | | |
| Approver | | | |
