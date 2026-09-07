---
layout: default
title: Glossarium
# parent: Home
nav_order: 2

---

# Glossarium

Het glossarium bevat de definities die in de Belgische CareSets worden gebruikt.
Het helpt iedereen die met CareSets werkt dezelfde termen consistent te
gebruiken. Zo worden misverstanden tussen zorgverleners, softwareleveranciers en
beleidsmakers vermeden.

## Nood aan een gedeeld glossarium

CareSets zijn opgevat als herbruikbare, geharmoniseerde datasets — dezelfde
concepten, met dezelfde betekenis, overal waar zij voorkomen. De persoon op wie
de registratie betrekking heeft, wie ze heeft geregistreerd en wanneer, de
status, de identificatie: die zijn gemeenschappelijk voor de meeste CareSets.

De CareSets en dit glossarium leveren die geharmoniseerde definities. De
gemeenschappelijke concepten, en de modellen die ze gebruiken, worden uitgedrukt
in de FHIR-profielen en geïmplementeerd in systemen. De kernconcepten één keer
vastleggen voorkomt dat zij in elk profiel en elk systeem opnieuw worden
gedefinieerd, niet altijd op dezelfde manier. Dat zou praktische gevolgen hebben
— een bevraging die het dossier van een patiënt samenstelt, zou mogelijk niet
meenemen wat het ene model *subject* en het andere *patient* noemt; een
toegangsregel die over de *recorder* gaat, zou een model dat die *author* noemt
mogelijk niet bereiken.

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
