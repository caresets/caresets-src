---
layout: default
title: Logische datamodellen
nav_order: 2
has_children: true
lang: nl
---

# Logische datamodellen

## Wat zijn logische modellen?

Logische modellen in FHIR zijn abstracte representaties van datastructuren die de informatieinhoud definiëren zonder te specificeren hoe die inhoud technisch wordt geïmplementeerd of uitgewisseld. Ze dienen als brug tussen bedrijfsvereisten en technische implementatie.

In tegenstelling tot FHIR-profielen (die bestaande FHIR-resources beperken), definiëren logische modellen volledig aangepaste structuren die domeinspecifieke concepten vertegenwoordigen. Ze zijn bijzonder nuttig voor:

- **Documenteren van vereisten**: Vastleggen van bedrijfs- en klinische vereisten in een gestructureerd, berekenbaar formaat
- **Multi-paradigma modellering**: Definiëren van structuren die kunnen worden gemapt naar meerdere implementatietechnologieën (FHIR, CDA, databaseschema's, etc.)
- **Communicatie met belanghebbenden**: Bieden van een technologie-neutrale weergave die klinische en zakelijke belanghebbenden kunnen begrijpen

Voor meer details, zie de [FHIR Logische Modellen specificatie](https://hl7.org/fhir/R4/structuredefinition.html#logical).

## Logische modellen als datatypes of voorouders

Een krachtige functie van FHIR logische modellen is hun vermogen om andere logische modellen op twee manieren te refereren:

### Als datatypes

Een logisch model kan een ander logisch model gebruiken als datatype voor zijn elementen. Dit maakt **compositie** mogelijk - het bouwen van complexe modellen uit eenvoudigere, herbruikbare bouwstenen.

Bijvoorbeeld, een `Vaccination` model zou een `BodySite` model kunnen gebruiken als type voor zijn `site` element, in plaats van de lichaamslokalisatievelden inline te definiëren.

### Als voorouders (Specialisatie)

Een logisch model kan een ander logisch model uitbreiden als zijn ouder. Dit creëert een **specialisatie**-relatie waarbij het kindmodel alle elementen van de ouder erft en nieuwe kan toevoegen.

**Belangrijk**: In tegenstelling tot FHIR-profielen vertegenwoordigt overerving van logische modellen **specialisatie, geen beperking**. Het kindmodel breidt de structuur van de ouder uit in plaats van deze te beperken. Dit betekent:

- Kindmodellen kunnen nieuwe verplichte elementen toevoegen
- Kindmodellen kunnen de kardinaliteit van overgeërfde elementen uitbreiden
- Kindmodellen vertegenwoordigen een specifieker concept, geen beperkte weergave

Dit onderscheid is cruciaal: profielen beperken resources voor specifieke use cases, terwijl overerving van logische modellen definities uitbreidt voor gespecialiseerde domeinen.

---
