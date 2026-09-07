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

Samenhang is hier niet alleen een kwestie van leesbaarheid. De CareSets en dit
glossarium vormen de gemeenschappelijke specificatie: wat hier wordt
afgesproken, is wat de FHIR-profielen uitdrukken en wat systemen vervolgens
implementeren, zodat een concept dat hier één keer is vastgelegd, in elk profiel
en elke implementatie terugkomt. Gebeurt dat niet, dan verdwijnt de afstemming
niet: zij zakt door naar elk profiel en elk systeem, waar iedereen ze opnieuw
maakt, en anders. De risico's die daaruit volgen zijn concreet: een bevraging
die het dossier van een patiënt samenstelt, kan missen wat het ene model
*subject* en het andere *patient* noemt, en een toegangsregel die over de
Recorder gaat, bereikt mogelijk een model niet dat die *author* noemt.

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
