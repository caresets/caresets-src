---
layout: default
title: Considérations de conception
nav_order: 4
parent: Modèles de données logiques
lang: fr
---

# Modèles de conception

Cette page décrit certains principes et modèles de conception utilisés dans les CareSets pour garantir la **cohérence**, la **réutilisabilité** et l'**interopérabilité**.


## Blocs d'information réutilisables

### Concept

Les blocs d'information réutilisables sont des structures de données communes qui apparaissent dans plusieurs CareSets. En standardisant ces blocs, nous :

- Réduisons la redondance dans les définitions de modèles
- Assurons la cohérence dans la capture des concepts communs
- Simplifions l'implémentation en réutilisant les mêmes modèles
- Facilitons l'agrégation et l'analyse des données

### Blocs réutilisables courants

#### BodySite

Le modèle BodySite capture les informations de localisation anatomique et est utilisé dans plusieurs contextes :

**Utilisé dans :**
- Observations (où une mesure a été prise)
- Procédures (où une procédure a été effectuée)
- Conditions (emplacement d'un problème/diagnostic)
- Spécimens (site de prélèvement)

**Structure :**
```
BodySite {
  bodyLocation: CodeableConcept     // Site anatomique
  bodyLaterality: CodeableConcept   // Gauche/droite/bilatéral
  bodyTopography: CodeableConcept   // Topographie spécifique
}
```

**Exemple :** Enregistrement de la pression artérielle sur le bras gauche :
- bodyLocation: "Bras supérieur" (SNOMED CT: 40983000)
- bodyLaterality: "Gauche" (SNOMED CT: 7771000)


#### Raison et indication

Capture pourquoi quelque chose a été fait ou demandé :

**Structure :**
```
Reason {
  reasonCode: CodeableConcept         // Raison codée
  reasonReference: Reference(Condition)  // Lien vers condition/problème
}
```

**Utilisé dans :**
- Médicaments (indication pour la prescription)
- Procédures (raison de l'exécution)
- Observations (raison de la mesure)

### Principes de conception pour les blocs réutilisables

1. **Responsabilité unique** : Chaque bloc doit représenter un concept cohérent
2. **Indépendance du contexte** : Les blocs doivent fonctionner dans différents cas d'utilisation
3. **Compatibilité ascendante** : Les modifications ne doivent pas briser les implémentations existantes
4. **Terminologies standard** : Utiliser des systèmes de codes établis dans la mesure du possible
5. **Optionnel le cas échéant** : Tous les contextes n'ont pas besoin de tous les éléments

### Utilisation

Les CareSets réutilisent ces blocs d'information de la manière suivante :

1. **Référencer la définition standard**, au lieu de redéfinir localement
2. **Documenter les contraintes ou extensions spécifiques au contexte** : Des règles spéciales peuvent s'appliquer à chaque cas d'utilisation
3. **Utiliser des noms cohérents** : Garder les noms d'éléments cohérents entre les modèles
4. **Fournir des exemples** : Montrer comment le bloc est utilisé dans votre contexte spécifique
5. **Tester dans tous les cas d'utilisation** : S'assurer que le bloc fonctionne dans tous les scénarios prévus



---


## Identifiants

Les CareSets utilisent des identifiants métier (Business Identifiers), qui identifient de manière unique les entités de santé (patients, observations, procédures, etc.) dans différents systèmes.

* Les entités sont censées avoir un identifiant "principal".
  * Lorsque le CareSet est créé et soumis à son système principal d'enregistrement, l'identifiant "principal" n'est pas encore connu. Dans cette situation, un autre identifiant doit être envoyé, pour faciliter le suivi vers l'enregistrement du soumetteur original. Un exemple est lorsqu'une prescription de médicament est d'abord créée dans un logiciel de médecin généraliste et est envoyée à Recip-e pour créer l'entrée officielle dans ce système.
* Les identifiants métier sont attribués par différentes organisations. Le même objet peut avoir différents identifiants. Par exemple, pour un Patient, les identifiants sont le numéro NISS, le numéro de dossier de réfugié, le numéro de passeport, etc.


Les CareSets utilisent les types de données FHIR Identifier qui se composent de :

- **System (Espace de noms)** : URI indiquant quelle organisation a émis l'identifiant
- **Value** : La chaîne d'identifiant réelle

Le **system** permet d'attribuer différents identifiants métier à une instance de CareSet. Par exemple, le numéro d'identification de sécurité sociale nationale (NISS/INSZ) est l'identifiant patient principal en Belgique :

- **System** : `https://www.ehealth.fgov.be/standards/fhir/core/NamingSystem/ssin`
- **Format** : 11 chiffres (AAMMJJ-XXX-CC) sans ponctuation
- **Exemple de valeur** : `85070512345`

