---
layout: default
title: Ontwerpoverwegingen
nav_order: 4
parent: Logische datamodellen
lang: nl
---

# Ontwerppatronen

Deze pagina beschrijft enkele ontwerpprincipes en patronen die in CareSets worden gebruikt om **consistentie**, **herbruikbaarheid** en **interoperabiliteit** te waarborgen.


## Definitie en implementatie van een CareSet

Er moet een duidelijk onderscheid worden gemaakt tussen de **definitie** van een CareSet en de **implementatie** ervan.

### Definitie van de CareSet

- transversaal gedragen door het RIZIV;
- gebaseerd op de businessbehoeften en de gebruiksgevallen;
- normatief en gedeeld binnen het hele ecosysteem.

### Implementatie van de CareSet

- uitgevoerd door businesssoftware, kluizen en andere componenten;
- bestaat erin deze systemen in staat te stellen CareSets te produceren, consumeren, opslaan en uitwisselen conform de gepubliceerde definitie.

De definitie vormt de referentie; implementaties moeten zich daaraan conformeren.

---



## Herbruikbare informatieblokken

### Concept

Herbruikbare informatieblokken zijn gemeenschappelijke datastructuren die in meerdere CareSets voorkomen. Door deze blokken te standaardiseren:

- Verminderen we redundantie in modeldefinities
- Waarborgen we consistentie in hoe gemeenschappelijke concepten worden vastgelegd
- Vereenvoudigen we implementatie door dezelfde patronen te hergebruiken
- Vergemakkelijken we data-aggregatie en -analyse

### Veelvoorkomende herbruikbare blokken

#### BodySite

Het BodySite-model legt anatomische locatie-informatie vast en wordt in meerdere contexten gebruikt:

**Gebruikt in:**
- Observaties (waar een meting werd gedaan)
- Procedures (waar een procedure werd uitgevoerd)
- Condities (locatie van een probleem/diagnose)
- Specimens (afnameplek)

**Structuur:**
```
BodySite {
  bodyLocation: CodeableConcept     // Anatomische locatie
  bodyLaterality: CodeableConcept   // Links/rechts/bilateraal
  bodyTopography: CodeableConcept   // Specifieke topografie
}
```

**Voorbeeld:** Bloeddrukmeting op de linkerarm vastleggen:
- bodyLocation: "Bovenarm" (SNOMED CT: 40983000)
- bodyLaterality: "Links" (SNOMED CT: 7771000)


#### Reden en indicatie

Vastleggen waarom iets is gedaan of aangevraagd:

**Structuur:**
```
Reason {
  reasonCode: CodeableConcept         // Gecodeerde reden
  reasonReference: Reference(Condition)  // Link naar conditie/probleem
}
```

**Gebruikt in:**
- Medicatie (indicatie voor voorschrijven)
- Procedures (reden voor uitvoering)
- Observaties (reden voor meting)

### Ontwerpprincipes voor herbruikbare blokken

1. **Enkele verantwoordelijkheid**: Elk blok moet één samenhangend concept vertegenwoordigen
2. **Contextonafhankelijkheid**: Blokken moeten in verschillende use cases werken
3. **Achterwaartse compatibiliteit**: Wijzigingen mogen bestaande implementaties niet breken
4. **Standaard terminologieën**: Gebruik waar mogelijk gevestigde codesystemen
5. **Optioneel waar gepast**: Niet alle contexten hebben alle elementen nodig

### Gebruik

CareSets hergebruiken deze informatieblokken op de volgende manier:

1. **Refereer naar de standaarddefinitie**, in plaats van lokaal opnieuw te definiëren
2. **Documenteer contextspecifieke beperkingen of uitbreidingen**: Speciale regels kunnen van toepassing zijn op elke use case
3. **Gebruik consistente naamgeving**: Houd elementnamen consistent tussen modellen
4. **Geef voorbeelden**: Toon hoe het blok in uw specifieke context wordt gebruikt
5. **Test in alle use cases**: Zorg ervoor dat het blok in alle beoogde scenario's werkt



---


## Identifiers

CareSets gebruiken Business Identifiers, die zorgenititeiten (patiënten, observaties, procedures, enz.) uniek identificeren in verschillende systemen.

* Entiteiten worden geacht één "hoofd" identifier te hebben.
  * Wanneer de CareSet wordt aangemaakt en ingediend bij het hoofdregistratiesysteem, is de "hoofd" identifier nog niet bekend. In deze situatie moet een andere identifier worden verzonden, voor eenvoudige tracering naar het oorspronkelijke indienerrecord. Een voorbeeld is wanneer een medicatievoorschrift eerst wordt aangemaakt in huisartssoftware en wordt verzonden naar Recip-e om de officiële vermelding in dat systeem aan te maken.
* Business identifiers worden toegewezen door verschillende organisaties. Hetzelfde object kan verschillende identifiers hebben. Bijvoorbeeld, voor een Patiënt zijn de identifiers het INSZ-nummer, vluchtelingendossiernummer, paspoortnummer, enz.


CareSets gebruiken FHIR Identifier datatypes die bestaan uit:

- **System (Namespace)**: URI die aangeeft welke organisatie de identifier heeft uitgegeven
- **Value**: De daadwerkelijke identifier string

Het **system** helpt bij het toewijzen van verschillende business identifiers aan een CareSet-instantie. Bijvoorbeeld, het Identificatienummer van de Sociale Zekerheid (INSZ/NISS) is de primaire patiëntidentifier in België:

- **System**: `https://www.ehealth.fgov.be/standards/fhir/core/NamingSystem/ssin`
- **Formaat**: 11 cijfers (JJMMDD-XXX-CC) zonder interpunctie
- **Voorbeeldwaarde**: `85070512345`

