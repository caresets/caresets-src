---
layout: default
title: Glossaire
# parent: Home
nav_order: 2

---

# Glossaire

Le glossaire contient les définitions utilisées dans les CareSets belges. Il garantit que toute personne travaillant avec les CareSets utilise les mêmes termes de la même manière. Cela évite les malentendus entre prestataires de soins, éditeurs de logiciels et décideurs politiques.  


Le glossaire est organisé en sections suivantes :

[Glossaire clinique](glossary_clinical.html) : Définitions des concepts et termes cliniques utilisés dans les CareSets
[Glossaire opérationnel](glossary_operational.html) : Définitions des concepts et termes opérationnels lors de la conception et de la compréhension de l'écosystème eHealth belge

## Pourquoi un glossaire partagé est nécessaire

Lorsqu'un nouveau CareSet est défini, l'essentiel de son contenu n'est pas
nouveau. Les mêmes quelques concepts reviennent dans presque tous : la personne
concernée par l'enregistrement, qui l'a enregistré et quand, son statut, son
identifiant. Les convenir une fois et les réutiliser est ce qui rend un
ensemble de CareSets cohérent, plutôt qu'une collection de structures
semblables en apparence mais différentes dans le détail.

La cohérence n'est pas ici qu'une question de lisibilité : elle touche tout ce
qui se construit sur les CareSets. Deux exemples.

**Implémentabilité.** Qui définit un nouveau CareSet part de concepts dont la
signification est déjà convenue, au lieu de redéfinir ce qu'est un patient ou
une date d'administration. Un logiciel qui parcourt plusieurs CareSets y
retrouve le même concept, sans traitement particulier par modèle.

**Contrôle d'accès et audit.** Les règles d'autorisation et de journalisation
portent sur des concepts, non sur des noms de champs. Une règle telle que *un
patient peut savoir qui a enregistré ses données* doit retrouver le Recorder
dans chaque CareSet qui en comporte un. Si chaque modèle le nomme autrement, la
règle couvre certains modèles et en manque d'autres, sans que rien ne le
signale — et une règle qui échoue sans le dire est pire qu'une règle qui échoue
de manière visible.

*Qui est le Recorder d'un CareSet ?* est une question qui porte sur l'ensemble
de l'écosystème. Elle ne peut recevoir une réponse unique, valable partout, que
parce que chaque modèle rattache son élément d'enregistrement au même concept
du glossaire.

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
