---
layout: default
title: Glossaire
# parent: Home
nav_order: 2

---

# Glossaire

Le glossaire contient les définitions utilisées dans les CareSets belges. Il aide
toute personne travaillant avec les CareSets à employer les mêmes termes de
manière cohérente. Cela évite les malentendus entre prestataires de soins,
éditeurs de logiciels et décideurs politiques.

## Besoin d'un glossaire partagé

Les CareSets sont conçus comme des ensembles de données réutilisables et
harmonisés — les mêmes concepts, avec le même sens, partout où ils apparaissent.
La personne concernée par l'enregistrement, qui l'a enregistré et quand, son
statut, son identifiant : ces éléments sont communs à la plupart des CareSets.

Les CareSets et ce glossaire fournissent ces définitions harmonisées. Les
concepts communs, et les modèles qui les utilisent, sont exprimés dans les
profils FHIR et implémentés dans les systèmes. Définir une fois les concepts
clés évite de les redéfinir dans chaque profil et chaque système, pas toujours
de la même manière. Cela aurait un impact pratique — une requête qui rassemble
le dossier d'un patient pourrait ne pas reprendre ce qu'un modèle appelle
*subject* et un autre *patient* ; une règle d'accès écrite sur le *recorder*
pourrait ne pas atteindre un modèle qui le nomme *author*.

### Les mêmes concepts, sous des noms différents

Quelques-uns des concepts récurrents, dans les modèles rattachés à ce jour :

| Concept | Présent dans | Nommé |
|---|---|---|
| Patient — la personne concernée | 25 modèles | *patient*, *subject* |
| RecordedDate — date d'enregistrement | 19 modèles | *recordedDate*, *recorded*, *creationDate* |
| Recorder — qui a enregistré | 16 modèles | *recorder*, *author* |
| BusinessIdentifier — l'identifiant | 22 modèles | *identifier*, *businessIdentifier* |

Chaque ligne est un seul concept. Le glossaire est ce qui l'affirme, et le lien
entre chaque modèle et lui est ce qui permet au logiciel de le savoir.

### Comment le lien est établi

Chaque élément d'un modèle logique peut être rattaché à un concept du
glossaire. Le rattachement figure dans une correspondance publiée aux côtés des
modèles, et pas seulement dans la documentation : les éléments qui signifient
*Recorder* dans l'ensemble des modèles peuvent donc être énumérés, plutôt que
recherchés en lisant chaque modèle l'un après l'autre.

Tous les éléments ne sont pas rattachés. Beaucoup sont propres à un seul modèle
et n'ont aucun concept de glossaire ; un élément sans rattachement n'est pas un
oubli.

## Les deux glossaires

[Glossaire clinique](glossary_clinical.html) — définitions des concepts et termes cliniques utilisés dans les CareSets.

[Glossaire opérationnel](glossary_operational.html) — définitions des concepts et termes opérationnels utilisés pour concevoir et comprendre l'écosystème eHealth belge.
