---
layout: default
title: Glossarium
# parent: Home
nav_order: 2

---

# Glossarium

Het glossarium bevat de definities die in de Belgische CareSets worden gebruikt. Het zorgt ervoor dat iedereen die met CareSets werkt dezelfde termen op dezelfde manier gebruikt. Zo worden misverstanden tussen zorgverleners, softwareleveranciers en beleidsmakers vermeden.  


Het glossarium is onderverdeeld in de volgende secties:

[Klinisch glossarium](glossary_clinical.html): Definities van klinische concepten en termen gebruikt in de CareSets
[Operationeel glossarium](glossary_operational.html): Definities van operationele concepten en termen bij het ontwerpen en begrijpen van het Belgische eHealth-ecosysteem


## Waarom een gedeeld glossarium nodig is

Een definitie die één keer wordt geschreven en overal wordt gebruikt, is meer
waard dan alle plaatsen waar zij voorkomt bij elkaar.

**Hergebruik.** Een concept dat één keer is gedefinieerd, kan in alle modellen
worden hergebruikt. Een nieuwe CareSet wordt samengesteld uit onderdelen met
een reeds afgesproken betekenis, zonder telkens opnieuw vast te leggen wat een
patiënt, een Recorder of een toedieningsdatum is. Zo verloopt het ontwerp sneller en is het nalezen
eenvoudiger.

**Consistente regels.** Een regel die op een concept is geformuleerd, geldt
overal waar dat concept voorkomt. Regels voor bewaring, validatie, toestemming
en kwaliteit kunnen één keer worden vastgelegd voor *de Recorder van een
CareSet* en gelden dan voor elk model dat er een heeft. Wanneer elk model
hetzelfde idee anders benoemt, moet elke regel per model worden herhaald, en
lopen de kopieën uiteen.

**Toegangscontrole.** Autorisatiebeleid wordt op concepten geschreven, niet op
veldnamen. Beleid zoals *een patiënt mag zien wie zijn gegevens heeft
geregistreerd* werkt alleen als het element dat in het ene model
*recorder* heet, in het andere *author* en in een derde *recorded by*, als
hetzelfde concept herkenbaar is. Is dat niet zo, dan dekt het beleid sommige
modellen wel en andere niet, zonder dat dit ergens wordt gemeld — en beleid dat
ongemerkt faalt is erger dan beleid dat zichtbaar faalt.

**Controleerbaarheid.** *Wie is de Recorder van een CareSet?* is een vraag over
het geheel van het ecosysteem, niet over één model. Zij kan alleen één keer,
voor alles tegelijk, worden beantwoord doordat elk model zijn
registratie-element aan dezelfde glossariumterm koppelt. Zonder die koppeling zijn het
evenveel afzonderlijke vragen als er modellen zijn, met evenveel afzonderlijke
antwoorden, en is er geen manier om te weten of de lijst volledig is.

**Traceerbaarheid.** Wanneer een definitie verandert, kunnen de betrokken
modellen worden aangewezen in plaats van geraden. Dezelfde koppeling die een
vraag over de gegevens beantwoordt, beantwoordt ook de vraag wat een wijziging
teweegbrengt.

### Hoe de koppeling tot stand komt

Elk element van een logisch model kan aan een glossariumconcept worden
gekoppeld. De koppeling staat in het model zelf en niet alleen in de
documentatie: de elementen die in alle modellen *Recorder* betekenen, kunnen
daardoor worden opgesomd in plaats van gezocht door elk model afzonderlijk te
lezen.

Niet elk element is gekoppeld. Veel elementen zijn eigen aan één model en
hebben geen glossariumconcept; een element zonder koppeling is geen
nalatigheid.
