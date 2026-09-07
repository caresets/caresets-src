---
layout: default
title: Glossarium
# parent: Home
nav_order: 2

---

# Glossarium

Het glossarium bevat de definities die in de Belgische CareSets worden gebruikt. Het zorgt ervoor dat iedereen die met CareSets werkt dezelfde termen op dezelfde manier gebruikt. Zo worden misverstanden tussen zorgverleners, softwareleveranciers en beleidsmakers vermeden.  


## Waarom een gedeeld glossarium nodig is

Wanneer een nieuwe CareSet wordt gedefinieerd, is het meeste van de inhoud niet
nieuw. Dezelfde handvol concepten keert in bijna elke CareSet terug: de persoon
op wie de registratie betrekking heeft, wie ze heeft geregistreerd en wanneer,
de status, de identificatie. Die één keer afspreken en hergebruiken is wat een
geheel van CareSets samenhangend maakt, in plaats van een verzameling
structuren die op elkaar lijken maar in de details verschillen.

Samenhang is hier niet alleen een kwestie van leesbaarheid: zij raakt alles wat
op de CareSets wordt gebouwd. Zonder samenhang legt elke CareSet opnieuw vast
wat een patiënt is, moet software voor elk model een uitzondering maken, en
geldt een regel als *een patiënt mag zien wie zijn gegevens heeft geregistreerd*
in de ene CareSet wel en faalt zij ongemerkt in de andere. Het gevolg is geen
slordige documentatie, maar een geheel van CareSets dat niet als één geheel te
implementeren of te besturen valt.

### Dezelfde concepten, onder verschillende namen

Enkele van de terugkerende concepten, in de gekoppelde modellen van vandaag:

| Concept | Komt voor in | Genoemd |
|---|---|---|
| Patient — de betrokken persoon | 25 modellen | *patient*, *subject* |
| RecordedDate — datum van registratie | 19 modellen | *recordedDate*, *recorded*, *creationDate* |
| Recorder — wie registreerde | 16 modellen | *recorder*, *author* |
| BusinessIdentifier — de identificatie | 22 modellen | *identifier*, *businessIdentifier* |

Elke rij is één concept. Het glossarium is wat dat vaststelt, en de koppeling
tussen elk model en het glossarium is wat software dat laat weten.

### Hoe de koppeling tot stand komt

Elk element van een logisch model kan aan een glossariumconcept worden
gekoppeld. De koppeling staat in een gepubliceerde mapping naast de modellen en
niet alleen in de documentatie: de elementen die in alle modellen *Recorder*
betekenen, kunnen daardoor worden opgesomd in plaats van gezocht door elk model
afzonderlijk te lezen.

Niet elk element is gekoppeld. Veel elementen zijn eigen aan één model en
hebben geen glossariumconcept; een element zonder koppeling is geen
nalatigheid.

## De twee glossaria

[Klinisch glossarium](glossary_clinical.html) — definities van de klinische concepten en termen die in de CareSets worden gebruikt.

[Operationeel glossarium](glossary_operational.html) — definities van de operationele concepten en termen die worden gebruikt bij het ontwerpen en begrijpen van het Belgische eHealth-ecosysteem.
