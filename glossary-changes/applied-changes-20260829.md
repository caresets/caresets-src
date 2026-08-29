# Applied glossary changes

- Source workbook: `C:\work\caresets\glossary\input\Glossaire CareSets V1 28-08-2026.xlsx`
- Written to: `glossary-changes/Glossaire CareSets V1 - revised 20260829.xlsx`
- Cells changed: **46** / Rows added: **1** / EN rows to patch: **22**

The source workbook is not modified. EN has no column in the sheet, so English changes are listed below for `input/ClinicalGlossary.csv` and are not written here.

## Rows added

### `Device` - new row 12

- **FR:** instrument, appareil, équipement, logiciel ou autre article destiné par son fabricant à être utilisé à des fins médicales chez l'être humain
- **NL:** instrument, toestel, apparaat, software of ander artikel dat door de fabrikant bestemd is om bij de mens voor medische doeleinden te worden gebruikt

## Cells changed

### `AdministrationDate` (row 2)

**FR** - F-005

| | |
|--|--|
| Before | Date d’administration du produit / vaccin par le Performer.  |
| After | date à laquelle un produit ou un vaccin est administré au patient par le Performer |

**NL** - F-006

| | |
|--|--|
| Before | Datum waarop het product/vaccin door de Performer is toegediend.  |
| After | datum waarop een product of vaccin door de Performer aan de patiënt is toegediend |

### `Asserter` (row 3)

**FR** - F-008

| | |
|--|--|
| Before | La personne à la source de l’information   |
| After | personne qui rapporte l'information enregistrée dans le CareSet |

**NL** - F-009

| | |
|--|--|
| Before | De persoon die de informatie verstrekt |
| After | persoon die de in de CareSet geregistreerde informatie rapporteert |

### `Author` (row 4)

**FR** - F-013

| | |
|--|--|
| Before | le professionnel de la santé qui encode et prend la responsabilité du contenu encodé.  |
| After | professionnel de la santé qui enregistre le contenu du CareSet et en assume la responsabilité |

**NL** - F-014

| | |
|--|--|
| Before | de zorgverlener die de gegevens invoert en de verantwoordelijkheid draagt voor de ingevoerde inhoud. |
| After | zorgverlener die de inhoud van de CareSet vastlegt en er de verantwoordelijkheid voor draagt |

### `BodyLaterality` (row 5)

**FR** - F-016

| | |
|--|--|
| Before | la latéralité du corps .  |
| After | côté du corps auquel se rapporte l'information enregistrée |

**NL** - F-017

| | |
|--|--|
| Before | de zijdelingse oriëntatie van het lichaam |
| After | zijde van het lichaam waarop de geregistreerde informatie betrekking heeft |

### `BodyLocation` (row 6)

**FR** - F-019

| | |
|--|--|
| Before | l'endroit du corps. |
| After | partie du corps à laquelle se rapporte l'information enregistrée |

**NL** - F-020

| | |
|--|--|
| Before | het lichaamsdeel  |
| After | lichaamsdeel waarop de geregistreerde informatie betrekking heeft |

### `BodyTopoGraphy` (row 7)

**FR** - F-023

| | |
|--|--|
| Before | La localisation ou la position relative  sur l'endroit corps  |
| After | position relative, à l'intérieur de la partie du corps concernée, du siège de l'information enregistrée |

**NL** - F-024

| | |
|--|--|
| Before | De locatie of de relatieve positie op het lichaam, |
| After | relatieve positie, binnen het betrokken lichaamsdeel, van de plaats waarop de geregistreerde informatie betrekking heeft |

### `Business Identifier` (row 8)

**FR** - F-027

| | |
|--|--|
| Before | Identifiant métier unique  d'une instance du CareSet. |
| After | identifiant qui désigne une instance de CareSet et qui est unique dans l'espace de nommage du système qui l'attribue |

**NL** - F-028

| | |
|--|--|
| Before | Unieke functie-ID van een instantie van de CareSet. |
| After | identificatie die een CareSet-instantie aanduidt en uniek is binnen de naamruimte van het systeem dat haar toekent |

### `Category` (row 9)

**FR** - F-030

| | |
|--|--|
| Before | Un attribut de classification d’un élément de données dans un CareSet, défini par une ValueSet standardisée, permettant de regrouper les informations selon leur signification clinique ou fonctionnelle dans le modèle logique belge |
| After | attribut classant un élément de données selon sa signification clinique ou fonctionnelle, permettant d'en regrouper les occurrences |

**NL** - F-031

| | |
|--|--|
| Before | Een classificatieattribuut van een gegevenselement in een CareSet, gedefinieerd door een gestandaardiseerde ValueSet, waarmee informatie kan worden gegroepeerd op basis van de klinische of functionele betekenis ervan in het Belgische logische model |
| After | attribuut dat een gegevenselement indeelt naar zijn klinische of functionele betekenis, waardoor de voorkomens ervan gegroepeerd kunnen worden |

### `ClinicalStatus` (row 10)

**FR** - F-033

| | |
|--|--|
| Before | Indique le statut de la pertinance clinique  |
| After | état rendant compte de l'actualité clinique de l'information enregistrée |

**NL** - F-034

| | |
|--|--|
| Before | Geeft de status van de klinische relevantie aan |
| After | toestand die de klinische actualiteit van de geregistreerde informatie weergeeft |

### `Code` (row 11)

**FR** - F-036

| | |
|--|--|
| Before | Décrit le concept clinique de l'information partagée  |
| After | valeur codée désignant le concept clinique auquel se rapporte l'information enregistrée |

**NL** - F-037

| | |
|--|--|
| Before | Beschrijft het klinische concept van gedeelde informatie |
| After | gecodeerde waarde die het klinische concept aanduidt waarop de geregistreerde informatie betrekking heeft |

### `Implantable Device` (row 13)

**FR** - F-039

| | |
|--|--|
| Before | Le dispositif médical qui est implanté, retiré ou manipulé d’une autre manière (par ex. calibration, remplacement de batterie, ajustement d’une prothèse, connexion d’un VAC pour plaie, etc.), et qui constitue un élément central de la procédure. Le lien s’effectue via une référence vers une ressource Device.   |
| After | dispositif destiné à être introduit en totalité ou en partie dans le corps humain et à y demeurer après l'intervention |

**NL** - F-040

| | |
|--|--|
| Before | "Het medisch hulpmiddel dat wordt geïmplanteerd, verwijderd of op een andere manier wordt gemanipuleerd  |
| After | hulpmiddel dat bestemd is om geheel of gedeeltelijk in het menselijk lichaam te worden gebracht en daar na de ingreep te blijven |

### `Lot Number` (row 14)

**FR** - F-042

| | |
|--|--|
| Before | N° de lot.  |
| After | identifiant attribué par le fabricant à l'ensemble des unités produites au cours d'un même cycle de fabrication |

**NL** - F-043

| | |
|--|--|
| Before | Lot Nummer |
| After | identificatie die de fabrikant toekent aan alle eenheden die in eenzelfde productiecyclus zijn vervaardigd |

### `Note` (row 15)

**FR** - F-046

| | |
|--|--|
| Before | Informations complémentaires relative au contenu du CareSet en format texte libre.  |
| After | informations complémentaires relatives au contenu du CareSet, exprimées en texte libre |

**NL** - F-047

| | |
|--|--|
| Before | *(empty)* |
| After | aanvullende informatie over de inhoud van de CareSet, uitgedrukt in vrije tekst |

### `Originating Request` (row 16)

**FR** - F-048

| | |
|--|--|
| Before | La demande qui est à l'origine de CareSet. |
| After | demande de soins ou de prestation dont l'exécution est enregistrée par le CareSet |

**NL** - F-049

| | |
|--|--|
| Before | De aanvraag die aan de basis ligt van CareSet.  |
| After | aanvraag voor zorg of verstrekking waarvan de uitvoering door de CareSet wordt geregistreerd |

### `PartOf` (row 17)

**FR** - F-051

| | |
|--|--|
| Before | Le CareSet dont ce CareSet fait partie, soit le CareSet parent de ce CareSet. Ex: Une biopsie qui fait partie d'une intervention chirugicale |
| After | CareSet englobant dont l'enregistrement courant constitue un composant |

**NL** - F-052

| | |
|--|--|
| Before | De CareSet waarvan deze CareSet deel uitmaakt, oftewel de bovenliggende CareSet van deze CareSet.  |
| After | omvattende CareSet waarvan de huidige registratie een onderdeel vormt |

### `Patient` (row 18)

**FR** - F-054

| | |
|--|--|
| Before | La personne qui est l'objet des soins de santé auxquels l'enregistrement (<CareSet>) fait réference.   |
| After | La personne qui est l'objet des soins de santé auxquels le CareSet fait référence. |

**NL** - F-055

| | |
|--|--|
| Before | De persoon op wie de gezondheidszorg betrekking heeft waarnaar de registratie (<CareSet>) verwijst. |
| After | persoon op wie de zorg betrekking heeft waarnaar de registratie verwijst |

### `Performer` (row 19)

**FR** - F-056

| | |
|--|--|
| Before | Le professionnel de la santé qui a <fait l'action en fonction du <CareSet> . |
| After | personne qui a réalisé l'acte enregistré par le CareSet |

**NL** - F-057

| | |
|--|--|
| Before | De zorgverlener die <de handeling heeft uitgevoerd op basis van de CareSet> |
| After | persoon die de door de CareSet geregistreerde handeling heeft uitgevoerd |

### `RecordedDate` (row 20)

**FR** - F-059

| | |
|--|--|
| Before | Date d'encodage de l'enregistrement par l'Author ou le Recorder. |
| After | date à laquelle l'enregistrement a été saisi par le Recorder |

**NL** - F-060

| | |
|--|--|
| Before | Datum waarop het record door de Author of de Recorder is ingevoerd  |
| After | datum waarop de registratie door de Recorder is ingevoerd |

### `Route` (row 21)

**FR** - F-062

| | |
|--|--|
| Before | Est la voie d’administration par laquelle un produit est mis en contact avec l’organisme.  |
| After | voie par laquelle un produit est mis en contact avec l'organisme |

**NL** - F-063

| | |
|--|--|
| Before | Dit is de toedieningsweg waarmee een product in contact komt met het lichaam.  |
| After | weg waarlangs een product in contact wordt gebracht met het lichaam |

### `Series Number` (row 22)

**FR** - F-066

| | |
|--|--|
| Before | N° de série de l’appareil  |
| After | identifiant attribué par le fabricant à un exemplaire déterminé d'un dispositif |

**NL** - F-067

| | |
|--|--|
| Before | Serienummer van het apparaat |
| After | identificatie die de fabrikant toekent aan één welbepaald exemplaar van een hulpmiddel |

### `Statut` (row 23)

**FR** - F-070

| | |
|--|--|
| Before | Indique le statut de l’enregistrement, le moment dans le cycle de vie  |
| After | état de l'enregistrement dans son cycle de vie |

**NL** - F-071

| | |
|--|--|
| Before | Geeft de status van de registratie aan, het moment in de levenscyclus |
| After | toestand van de registratie in haar levenscyclus |

### `Used device` (row 24)

**FR** - F-073

| | |
|--|--|
| Before | Le dispositif médical qui est utilisé pour <CareSet>.   |
| After | dispositif médical mis en œuvre pour réaliser l'acte enregistré |

**NL** - F-074

| | |
|--|--|
| Before | Het medisch hulpmiddel dat wordt gebruikt voor <CareSet. |
| After | medisch hulpmiddel dat wordt ingezet om de geregistreerde handeling uit te voeren |

### `VerificationStatus` (row 25)

**FR** - F-078

| | |
|--|--|
| Before | Indique le niveau de certitude de l'enregistrement   |
| After | degré de confirmation attribué à l'information enregistrée |

**NL** - F-079

| | |
|--|--|
| Before | Geeft de mate van zekerheid van de opname aan |
| After | graad van bevestiging van de geregistreerde informatie |

## EN changes for `input/ClinicalGlossary.csv`

| Term | Finding | New EN definition |
|------|---------|-------------------|
| Device | F-083 | instrument, apparatus, appliance, software or other article intended by its manufacturer to be used for medical purposes in human beings |
| AdministrationDate | F-007 | date on which a product or vaccine is administered to the patient by the Performer |
| Asserter | F-010 | person who reports the information recorded in the CareSet |
| Author | F-015 | healthcare professional who records the content of the CareSet and takes responsibility for it |
| BodyLaterality | F-018 | side of the body to which the recorded information refers |
| BodyLocation | F-021 | part of the body to which the recorded information refers |
| BodyTopoGraphy | F-025 | relative position, within the body part concerned, of the site to which the recorded information refers |
| Business Identifier | F-029 | identifier that designates a CareSet instance and is unique within the namespace of the system that assigns it |
| Category | F-032 | attribute classifying a data element by its clinical or functional meaning, allowing its occurrences to be grouped |
| ClinicalStatus | F-035 | state expressing the clinical currency of the recorded information |
| Code | F-038 | coded value designating the clinical concept to which the recorded information refers |
| Implantable Device | F-041 | device intended to be introduced wholly or partly into the human body and to remain there after the procedure |
| Lot Number | F-044 | identifier assigned by the manufacturer to all units produced in the same manufacturing cycle |
| Originating Request | F-050 | request for care or service whose execution is recorded by the CareSet |
| PartOf | F-053 | encompassing CareSet of which the current record forms a component |
| Performer | F-058 | person who performed the act recorded by the CareSet |
| RecordedDate | F-061 | date on which the record was entered by the Recorder |
| Route | F-064 | path by which a product is brought into contact with the body |
| Series Number | F-068 | identifier assigned by the manufacturer to one individual device |
| Statut | F-072 | state of the record within its lifecycle |
| Used device | F-075 | medical device used to carry out the recorded act |
| VerificationStatus | F-080 | degree of confirmation assigned to the recorded information |

## Not applied by this run (13)

| Finding | Reason |
|---------|--------|
| F-001 | cross-cutting finding - apply by hand |
| F-002 | cross-cutting finding - apply by hand |
| F-003 | cross-cutting finding - apply by hand |
| F-004 | cross-cutting finding - apply by hand |
| F-011 | cross-cutting finding - apply by hand |
| F-012 | cross-cutting finding - apply by hand |
| F-022 | cross-cutting finding - apply by hand |
| F-026 | cross-cutting finding - apply by hand |
| F-045 | cross-cutting finding - apply by hand |
| F-065 | cross-cutting finding - apply by hand |
| F-069 | cross-cutting finding - apply by hand |
| F-076 | cross-cutting finding - apply by hand |
| F-077 | cross-cutting finding - apply by hand |
