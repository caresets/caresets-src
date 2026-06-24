# PREVIEW: Glossary changes - BeSafeShare Operational Glossary

> **Preview only** - the JSON has NOT been modified. Re-run without `--preview` to apply.

- Generated: 2026-05-10 13:34:15
- Glossary key: `operational`
- Previous version: `0.1` (date `2025-12-28`)
- New version: `0.1` (date `2026-05-10`)

## Summary

- Concepts before: **5**
- Concepts after: **33**
- Added: **28**
- Removed: **0**
- Modified: **1**

## Added (28)

### + `DataElement`

- **Display:** Data Element
- **Status:** active
- **EN:** A unitary data item that composes a CareSet, corresponding to a precise business concept, with clear and documented semantics, and potentially subject to functional constraints (cardinality, dependencies, conditions). A data element is always defined in the context of a CareSet and is not an isolated technical field
- **FR:** Élément de données unitaire constitutif d'un CareSet, correspondant à un concept métier précis, doté d'une sémantique claire et documentée, et pouvant être soumis à des contraintes fonctionnelles (cardinalité, dépendances, conditions). Un data element est toujours défini dans le contexte d'un CareSet et n'est pas un champ technique isolé
- **NL:** Een elementair data-item dat deel uitmaakt van een CareSet, overeenkomend met een welbepaald business-concept, met een duidelijke en gedocumenteerde semantiek, en eventueel onderworpen aan functionele beperkingen (kardinaliteit, afhankelijkheden, voorwaarden). Een data element wordt altijd gedefinieerd in de context van een CareSet en is geen geïsoleerd technisch veld

### + `CareSetInstance`

- **Display:** CareSet Instance
- **Status:** active
- **EN:** The concrete realisation of a CareSet for a given patient at a given moment, containing real values for the defined data elements. It is created and updated in the context of a care act or event, then stored and exchanged by the systems of the ecosystem. The CareSet defines the model, the instance represents the actual data
- **FR:** Réalisation concrète d'un CareSet pour un patient donné à un moment donné, contenant des valeurs réelles pour les data elements définis. Elle est créée et mise à jour dans le cadre d'un acte ou d'un événement de soins, puis stockée et échangée par les systèmes de l'écosystème. Le CareSet définit le modèle, l'instance représente la donnée effective
- **NL:** De concrete realisatie van een CareSet voor een bepaalde patiënt op een bepaald moment, met reële waarden voor de gedefinieerde data elements. Ze wordt aangemaakt en bijgewerkt in het kader van een zorgactie of -gebeurtenis, en vervolgens opgeslagen en uitgewisseld door de systemen van het ecosysteem. De CareSet definieert het model, de CareSet Instance vertegenwoordigt de werkelijke data

### + `CareSetDefinition`

- **Display:** CareSet Definition
- **Status:** active
- **EN:** The normative, cross-cutting specification of a CareSet, led by the INAMI/RIZIV, grounded in business needs and use cases, and shared across the entire ecosystem. It is the reference with which every implementation must comply
- **FR:** Spécification normative et transverse d'un CareSet, portée par l'INAMI, basée sur les besoins business et les cas d'usage, et commune à l'ensemble de l'écosystème. Elle constitue la référence à laquelle toute implémentation doit se conformer
- **NL:** De normatieve en transversale specificatie van een CareSet, aangestuurd door het RIZIV, gebaseerd op businessbehoeften en gebruiksgevallen, en gedeeld binnen het hele ecosysteem. Zij vormt de referentie waaraan elke implementatie moet voldoen

### + `CareSetImplementation`

- **Display:** CareSet Implementation
- **Status:** active
- **EN:** The technical realisation of a CareSet by business software, vaults and other components of the ecosystem, enabling them to produce, consume, store and exchange CareSets that comply with the published definition
- **FR:** Réalisation technique d'un CareSet par les logiciels métiers, coffres-forts et autres composants de l'écosystème, leur permettant de produire, consommer, stocker et échanger des CareSets conformes à la définition publiée
- **NL:** De technische realisatie van een CareSet door businesssoftware, kluizen en andere componenten van het ecosysteem, zodat deze CareSets kunnen produceren, consumeren, opslaan en uitwisselen conform de gepubliceerde definitie

### + `Vault`

- **Display:** Coffre-fort,Kluis
- **Status:** active
- **EN:** An ecosystem component that stores CareSet instances and implements the relevant CareSets to ensure interoperability. Vaults enable secure access, exchange and persistence of health data, and play a central role in the management of CareSets within the Belgian ecosystem
- **FR:** Composant de l'écosystème qui stocke des instances de CareSets et implémente les CareSets pertinents pour assurer l'interopérabilité. Les coffres-forts permettent l'accès, l'échange et la persistance sécurisée des données de santé, et jouent un rôle central dans la gestion des CareSets au sein de l'écosystème belge
- **NL:** Een component van het ecosysteem dat CareSet-instances opslaat en de relevante CareSets implementeert om interoperabiliteit te garanderen. Kluizen maken veilige toegang, uitwisseling en persistentie van gezondheidsgegevens mogelijk en spelen een centrale rol in het beheer van CareSets binnen het Belgische ecosysteem

### + `BusinessAnalysisDocument`

- **Display:** Business Analysis Document
- **Status:** active
- **EN:** Normative deliverable accompanying the publication of a CareSet, describing the context and objectives, actors and roles, usage scenarios, and the functional scope of the CareSet
- **FR:** Délivrable normatif accompagnant la publication d'un CareSet, décrivant le contexte et les objectifs, les acteurs et rôles, les scénarios d'usage, ainsi que le périmètre fonctionnel du CareSet
- **NL:** Normatief deliverable dat de publicatie van een CareSet begeleidt en de context en doelstellingen, actoren en rollen, gebruiksscenario's en het functionele bereik van de CareSet beschrijft

### + `BusinessRules`

- **Display:** Business Rules
- **Status:** active
- **EN:** Functional and business rules associated with a CareSet, covering constraints that cannot – or cannot fully – be expressed in the FHIR specification, as well as rules of consistency, dependency or temporality
- **FR:** Règles fonctionnelles et métier associées à un CareSet, incluant les contraintes qui ne peuvent pas – ou pas entièrement – être exprimées dans la spécification FHIR, ainsi que les règles de cohérence, de dépendance ou de temporalité
- **NL:** Functionele en business-regels verbonden aan een CareSet, inclusief beperkingen die niet – of niet volledig – in de FHIR-specificatie kunnen worden uitgedrukt, en regels inzake consistentie, afhankelijkheid of tijdsvolgorde

### + `FHIRSpecification`

- **Display:** FHIR Specification
- **Status:** active
- **EN:** The normative technical part of a CareSet publication, comprising the FHIR profiles required for its representation, cardinalities, bindings, invariants and technical constraints, and its alignment with international standards
- **FR:** Partie normative et technique de la publication d'un CareSet, comprenant les profils FHIR nécessaires à sa représentation, les cardinalités, bindings, invariants et contraintes techniques, ainsi que l'alignement avec les standards internationaux
- **NL:** Het normatieve technische deel van de publicatie van een CareSet, met de FHIR-profielen die nodig zijn voor de representatie ervan, kardinaliteiten, bindings, invarianten en technische beperkingen, en de afstemming op internationale standaarden

### + `CoreHealthDomains`

- **Display:** (Core) Health Domains
- **Status:** proposed
- **EN:** Domains of clinical, care, administrative or social concepts considered necessary or eligible for a patient file by business stakeholders. By Core Health Domains we mean the common Health Care Data generally shared among all HealthCareProfessionals.
- **FR:** Domaines de concepts cliniques, de soins, administratifs ou sociaux considérés comme nécessaires ou pertinents pour le dossier du patient par les parties prenantes métier. Par domaines de santé de base, on entend les données de santé communes généralement partagées par l'ensemble des professionnels de santé.
- **NL:** Domeinen van klinische, zorg-, administratieve of sociale concepten die door business-stakeholders als noodzakelijk of relevant voor het patiëntendossier worden beschouwd. Met Kerngezondheidsdomeinen bedoelen we de gemeenschappelijke gezondheidsgegevens die doorgaans door alle zorgverleners worden gedeeld.

### + `BIHRSections`

- **Display:** BIHR sections
- **Status:** proposed
- **EN:** Dynamic list of (currently) 15 healthcare-information sections that should be included within the Belgian Integrated Health Record of each Belgian citizen. These correspond partly with the Core Health Domains.
- **FR:** Liste dynamique de (actuellement) 15 sections d'information de santé qui doivent être incluses dans le Belgian Integrated Health Record de chaque citoyen belge. Elles correspondent en partie aux domaines de santé de base.
- **NL:** Dynamische lijst van (momenteel) 15 secties met zorginformatie die opgenomen moeten worden in het Belgian Integrated Health Record van elke Belgische burger. Deze komen gedeeltelijk overeen met de Kerngezondheidsdomeinen.

### + `CoreDataForInteroperability`

- **Display:** Core Data for Interoperability
- **Status:** proposed
- **EN:** The nationally agreed set of essential information, organized through Health Domains, that must be captured and exchanged consistently so all systems and professionals can understand and reuse it.
- **FR:** Ensemble nationalement convenu d'informations essentielles, organisé par domaines de santé, qui doit être capturé et échangé de manière cohérente afin que tous les systèmes et professionnels puissent les comprendre et les réutiliser.
- **NL:** De nationaal overeengekomen set essentiële informatie, gestructureerd volgens Gezondheidsdomeinen, die op een consistente manier moet worden vastgelegd en uitgewisseld zodat alle systemen en zorgprofessionals deze correct kunnen begrijpen en hergebruiken.

### + `Entry`

- **Display:** Entry
- **Status:** proposed
- **EN:** An Entry represents a unit of health information as it is created, recorded, and maintained within a local system, such as an electronic health record. It reflects how information is captured in the context of a specific application, organization, or workflow.
- **FR:** Une Entry représente une unité d'information de santé telle qu'elle est créée, enregistrée et maintenue dans un système local, tel qu'un dossier patient électronique. Elle reflète la manière dont l'information est capturée dans le contexte d'une application, d'une organisation ou d'un workflow spécifique.
- **NL:** Een Entry vertegenwoordigt een eenheid van gezondheidsinformatie zoals die wordt aangemaakt, geregistreerd en beheerd binnen een lokaal systeem, zoals een elektronisch patiëntendossier. Ze weerspiegelt hoe informatie wordt vastgelegd binnen de context van een specifieke applicatie, organisatie of workflow.

### + `Data`

- **Display:** Data
- **Status:** proposed
- **EN:** In this specific context we refer to Data as an in- or output (such as a registration, either manually by a HCP or automatically via Devices,...) of Data belonging to the Core Data for Interoperability. This data is being captured/entered at data production and is being visualised upon data consumption. For architectural reasons, we distinguish Dynamic Data from Static Data.
- **FR:** Dans ce contexte spécifique, les Données désignent les entrées ou sorties (telles qu'un enregistrement, réalisé manuellement par un professionnel de santé ou automatiquement via des dispositifs) appartenant aux données de base pour l'interopérabilité. Ces données sont capturées lors de la production des données et visualisées lors de leur consommation. Pour des raisons architecturales, une distinction est faite entre données dynamiques et données statiques.
- **NL:** In deze context verwijst Data naar input of output (zoals een registratie, manueel door een zorgverlener of automatisch via toestellen) van gegevens die behoren tot de Kerngegevens voor interoperabiliteit. Deze gegevens worden vastgelegd bij dataproductie en gevisualiseerd bij dataconsumptie. Om architecturale redenen maken we een onderscheid tussen Dynamische Data en Statische Data.

### + `ResourceInstance`

- **Display:** Resource instance
- **Status:** proposed
- **EN:** The same Data, but then mapped to FHIR Resources using Belgian profiles in order to be transported from one interface/data actor to another.
- **FR:** Les mêmes Données, mais mappées sur des ressources FHIR à l'aide de profils belges, afin de permettre leur transport entre interfaces ou acteurs de données.
- **NL:** Dezelfde Data, maar gemapt op FHIR Resources volgens Belgische profielen, met als doel het transport van gegevens tussen interfaces of data-actoren.

### + `DynamicData`

- **Display:** Dynamic Data
- **Status:** proposed
- **EN:** Data representing a persistent clinical state or status that evolves over time. Updates are allowed, and each change creates a new version with full audit history. Corresponds to persistent resources in HL7 FHIR. These data are typically, but not exclusively, stored in Public Authentic Sources.
- **FR:** Données représentant un état ou un statut clinique persistant qui évolue dans le temps. Les mises à jour sont autorisées et chaque modification génère une nouvelle version avec un historique d'audit complet. Elles correspondent aux persisten resources en HL7 FHIR et sont généralement, mais pas exclusivement, stockées dans des sources authentiques publiques.
- **NL:** Gegevens die een persistente klinische toestand of status vertegenwoordigen en in de tijd evolueren. Updates zijn toegestaan en elke wijziging resulteert in een nieuwe versie met volledige audithistoriek. Komt overeen met persistent resources in HL7 FHIR. Deze gegevens worden gangbaar, maar niet uitsluitend, opgeslagen in Publieke Authentieke Bronnen.

### + `StaticData`

- **Display:** Static Data
- **Status:** proposed
- **EN:** Data representing a clinical event or observation at a specific point in time. It is conceptually immutable; changes occur only through corrections or new entries. Corresponds to event-based resources in HL7 FHIR. These data are typically, but not exclusively, stored in Distributed Authentic Sources.
- **FR:** Données représentant un événement ou une observation clinique à un moment donné. Elles sont conceptuellement immuables ; les modifications se font uniquement par des corrections ou de nouvelles entrées. Elles correspondent aux event resources en HL7 FHIR et sont généralement, mais pas exclusivement, stockées dans des sources authentiques distribuées.
- **NL:** Gegevens die een klinische gebeurtenis of observatie op een specifiek moment in de tijd vertegenwoordigen. Ze zijn conceptueel onveranderlijk; wijzigingen gebeuren enkel via correcties of nieuwe registraties. Komt overeen met event resources in HL7 FHIR. Deze gegevens worden gangbaar, maar niet uitsluitend, opgeslagen in Gedistribueerde Authentieke Bronnen.

### + `ResourceFHIR`

- **Display:** Resource (FHIR)
- **Status:** proposed
- **EN:** A standardized FHIR building block that structures health data and, when instantiated, carries it. It provides the base model for representing and exchanging CareSet Instances. FHIR Profiles constrain these Resources.
- **FR:** Un composant de base FHIR standardisé qui structure les données de santé et, lorsqu'il est instancié, les porte. Il constitue le modèle de base pour la représentation et l'échange des instances de CareSet. Les profils FHIR contraignent ces ressources.
- **NL:** Een gestandaardiseerd FHIR-bouwblok dat gezondheidsgegevens structureert en, wanneer geïnstantieerd, deze draagt. Het vormt het basismodel voor het representeren en uitwisselen van CareSet-instantiaties. FHIR-profielen beperken deze Resources.

### + `BelgianProfileFHIR`

- **Display:** Belgian Profile (FHIR)
- **Status:** proposed
- **EN:** Formalizes the "authorized and expected" way to structure a data exchange in the Belgian context using a set of constraints on a resource represented as a structure definition with derivation = constraint.
- **FR:** Formalise la manière « autorisée et attendue » de structurer les échanges de données dans le contexte belge au moyen d'un ensemble de contraintes appliquées à une ressource, définies dans une StructureDefinition avec derivation = constraint.
- **NL:** Formaliseert de "toegelaten en verwachte" manier om gegevensuitwisseling te structureren in de Belgische context via een set beperkingen op een resource, vastgelegd in een StructureDefinition met derivation = constraint.

### + `BaseProfiles`

- **Display:** Base Profiles
- **Status:** proposed
- **EN:** Define common concepts in a flexible way.
- **FR:** Définissent des concepts communs de manière flexible.
- **NL:** Definiëren gemeenschappelijke concepten op een flexibele manier.

### + `CoreProfiles`

- **Display:** Core Profiles
- **Status:** proposed
- **EN:** Add essential constraints that can be reused across many UseCases.
- **FR:** Ajoutent des contraintes essentielles pouvant être réutilisées dans de nombreux UseCases.
- **NL:** Voegen essentiële beperkingen toe die herbruikbaar zijn over meerdere UseCases heen.

### + `Terminology`

- **Display:** Terminology
- **Status:** proposed
- **EN:** Provides the standardized vocabulary used to express clinical meaning. International terminologies, such as SNOMED, are specialized within the Belgian context to ensure alignment with local requirements. Terminology systems define the available concepts and their relationships.
- **FR:** Fournit les vocabulaires standardisés utilisés pour exprimer la signification clinique. Les terminologies internationales, telles que SNOMED CT, sont spécialisées dans le contexte belge afin de répondre aux exigences locales. Les systèmes de terminologie définissent les concepts disponibles et leurs relations.
- **NL:** Biedt de gestandaardiseerde vocabularia om klinische betekenis uit te drukken. Internationale terminologieën, zoals SNOMED CT, worden in de Belgische context gespecialiseerd om aan lokale vereisten te voldoen. Terminologiesystemen definiëren de beschikbare concepten en hun onderlinge relaties.

### + `AuthenticSource`

- **Display:** Authentic Source
- **Status:** proposed
- **EN:** The authoritative repository where health data is stored with full traceability, versioning, and persistence. Central Authentic Sources generally, but not exclusively, support Dynamic Data; Distributed Authentic Sources generally, but not exclusively, store Static Data. They provide access to these data 24/7.
- **FR:** Le dépôt faisant autorité dans lequel les données de santé sont stockées avec une traçabilité complète, un versionnage et une persistance. Les sources authentiques centrales prennent généralement en charge les données dynamiques, tandis que les sources authentiques distribuées stockent principalement les données statiques. Elles offrent un accès 24h/24 et 7j/7 à ces données.
- **NL:** De gezaghebbende opslagplaats waar gezondheidsgegevens worden bewaard met volledige traceerbaarheid, versiebeheer en persistentie. Centrale Authentieke Bronnen ondersteunen doorgaans, maar niet uitsluitend, Dynamische Data; Gedistribueerde Authentieke Bronnen slaan doorgaans, maar niet uitsluitend, Statische Data op. Ze bieden 24/7 toegang tot deze gegevens.

### + `SoftwarePackage`

- **Display:** Software package
- **Status:** proposed
- **EN:** Also referred to as EHR or Work Environment. The clinical EHR software used by healthcare professionals to manage Patient Files. It implements CareSets and ensures that documentation and exchange follow national conventions, including FHIR-based interoperability rules.
- **FR:** Également appelé DPI ou environnement de travail. Logiciel clinique utilisé par les professionnels de santé pour gérer les dossiers patients. Il implémente les CareSets et garantit que la documentation et les échanges respectent les conventions nationales, y compris les règles d'interopérabilité basées sur FHIR.
- **NL:** Ook aangeduid als EPD of werkomgeving. De klinische EPD-software die door zorgverleners wordt gebruikt om patiëntendossiers te beheren. Het implementeert CareSets en zorgt ervoor dat documentatie en uitwisseling voldoen aan nationale conventies, inclusief FHIR-gebaseerde interoperabiliteitsregels.

### + `PatientFile`

- **Display:** Patient File
- **Status:** proposed
- **EN:** The structured collection of all health information for a patient as maintained within a Software Package.
- **FR:** Ensemble structuré de toutes les informations de santé d'un patient, tel qu'il est géré au sein d'un logiciel métier.
- **NL:** De gestructureerde verzameling van alle gezondheidsinformatie van een patiënt zoals beheerd binnen een Softwarepakket.

### + `UseCase`

- **Display:** UseCase
- **Status:** proposed
- **EN:** In this specific context, a UseCase refers to a clearly defined healthcare-related need, either a care-related act or situation or a required information product, for which information must be standardized and exchanged interoperably.
- **FR:** Dans ce contexte, un UseCase désigne un besoin de santé clairement défini, qu'il s'agisse d'un acte ou d'une situation de soins, ou d'un produit d'information requis, pour lequel les informations doivent être standardisées et échangées de manière interopérable.
- **NL:** In deze context verwijst een UseCase naar een duidelijk afgebakende zorggerelateerde behoefte, hetzij een zorghandeling of -situatie, hetzij een vereist informatieproduct, waarvoor informatie gestandaardiseerd en interoperabel moet worden uitgewisseld.

### + `BIHR`

- **Display:** BIHR
- **Status:** proposed
- **EN:** Not a patient record, but an ecosystem. As such, BIHR stands for a shared, governed environment that brings together shared health data and the means to make it discoverable, accessible, exchangeable and interoperable across partners. It includes the actors, standards, rules and technologies that collectively support the secure creation, governance, exchange and reuse of health information across organizational boundaries.
- **FR:** Il ne s'agit pas d'un dossier patient, mais d'un écosystème. Le BIHR désigne un environnement partagé et gouverné qui regroupe les données de santé partagées ainsi que les moyens de les rendre découvrables, accessibles, échangeables et interopérables entre partenaires. Il inclut les acteurs, les standards, les règles et les technologies qui soutiennent collectivement la création, la gouvernance, l'échange et la réutilisation sécurisés des informations de santé au-delà des frontières organisationnelles.
- **NL:** Geen patiëntendossier, maar een ecosysteem. BIHR staat voor een gedeelde en beheerde omgeving die gedeelde gezondheidsgegevens samenbrengt en de middelen biedt om deze vindbaar, toegankelijk, uitwisselbaar en interoperabel te maken tussen partners. Het omvat de actoren, standaarden, regels en technologieën die samen het veilige creëren, beheren, uitwisselen en hergebruiken van gezondheidsinformatie ondersteunen over organisatorische grenzen heen.

### + `Conformance`

- **Display:** Conformance
- **Status:** proposed
- **EN:** The property by which information aligns with agreed definitions, rules, and constraints so that it remains interpretable and reusable across systems and organizations. Clinical conformance: the Record aligns with the CareSets (meaning, expected content, business rules). Syntactical conformance: the Resource instance aligns with applicable Profiles (structure, codes, cardinalities, computable rules).
- **FR:** Propriété selon laquelle l'information est alignée sur des définitions, règles et contraintes convenues afin de rester interprétable et réutilisable entre systèmes et organisations. Conformité clinique : le dossier est aligné avec les CareSets (signification, contenu attendu, règles métier). Conformité syntaxique : l'instance de ressource est conforme aux profils applicables (structure, codes, cardinalités, règles calculables).
- **NL:** De eigenschap waarbij informatie in overeenstemming is met afgesproken definities, regels en beperkingen zodat ze interpreteerbaar en herbruikbaar blijft over systemen en organisaties heen. Klinische conformiteit: het dossier stemt overeen met de CareSets (betekenis, verwachte inhoud, business rules). Syntactische conformiteit: de resource-instantie stemt overeen met de toepasselijke profielen (structuur, codes, cardinaliteiten, computabele regels).

### + `Interface`

- **Display:** Interface
- **Status:** proposed
- **EN:** Not merely a User Interface, but more broadly a defined boundary through which a system exposes or accesses functionality, data, or services, enabling interaction with other systems, components, or actors.
- **FR:** Non seulement une interface utilisateur, mais plus largement une frontière définie par laquelle un système expose ou consomme des fonctionnalités, des données ou des services, permettant l'interaction avec d'autres systèmes, composants ou acteurs.
- **NL:** Niet louter een gebruikersinterface, maar breder opgevat als een afgebakend grensvlak waarlangs een systeem functionaliteit, data of diensten aanbiedt of afneemt, en zo interactie mogelijk maakt met andere systemen, componenten of actoren.

## Modified (1)

### ~ `CareSet`

**EN:**

```diff
- A structured set of clinical data related to a specific domain (vaccination, allergy, medication, etc.), defined by a logical model and intended to be shared between healthcare systems
+ A CareSet is a structured, coherent and standardised set of health data, defined by a logical model to cover a specific clinical or medico-administrative use case (for example: vaccination, prescription, referral, patient summary), and intended to be shared between the systems of the care ecosystem
```

**FR:**

```diff
- Un ensemble structuré de données cliniques relatives à un domaine spécifique (vaccination, allergie, médication, etc.), défini par un modèle logique et destiné à être partagé entre systèmes de soins de santé
+ Un CareSet est un ensemble structuré, cohérent et standardisé de données de santé, défini par un modèle logique pour couvrir un cas d'usage clinique ou médico-administratif précis (par exemple : vaccination, prescription, referral, patient summary), et destiné à être partagé entre les systèmes de l'écosystème de soins
```

**NL:**

```diff
- Een gestructureerde set klinische gegevens met betrekking tot een specifiek domein (vaccinatie, allergie, medicatie, enz.), gedefinieerd door een logisch model en bedoeld om te worden gedeeld tussen zorgsystemen
+ Een CareSet is een gestructureerde, coherente en gestandaardiseerde set gezondheidsgegevens, gedefinieerd door een logisch model om een specifiek klinisch of medisch-administratief gebruiksgeval te dekken (bijvoorbeeld: vaccinatie, voorschrift, verwijzing, patient summary), en bedoeld om te worden gedeeld tussen de systemen van het zorgecosysteem
```
