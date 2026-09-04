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

Une définition rédigée une seule fois et utilisée partout vaut davantage que la
somme des endroits où elle apparaît.

**Réutilisation.** Un concept défini une fois peut être réutilisé dans
l'ensemble des modèles. Un nouveau CareSet s'assemble à partir d'éléments dont
la signification est déjà convenue, sans redéfinir chaque fois ce qu'est un
patient, un Recorder ou une date d'administration. La conception est plus
rapide et la relecture plus simple.

**Cohérence des règles.** Une règle formulée sur un concept s'applique partout
où ce concept apparaît. Les règles de conservation, de validation, de
consentement et de qualité peuvent être énoncées une seule fois pour *le
Recorder d'un CareSet* et valoir pour tous les modèles qui en comportent un.
Lorsque chaque modèle nomme différemment la même idée, chaque règle doit être
réécrite modèle par modèle, et les copies divergent.

**Contrôle d'accès.** Les politiques d'autorisation portent sur des concepts,
non sur des noms de champs. Une politique telle que *un patient peut savoir qui
a enregistré ses données* ne fonctionne que si l'élément appelé *recorder* dans
un modèle, *author* dans un autre et *recorded by* dans un troisième sont
reconnus comme un même concept. À défaut, une politique
couvre certains modèles et en manque d'autres, sans que rien ne le signale — et une
politique qui échoue sans le dire est pire qu'une politique qui échoue de
manière visible.

**Vérifiabilité.** *Qui est le Recorder d'un CareSet ?* est une question qui
porte sur l'ensemble de l'écosystème, et non sur un seul modèle. Elle ne peut
recevoir une réponse unique, valable partout, que parce que chaque modèle
rattache son élément d'enregistrement au même terme du glossaire. Sans ce lien, ce sont autant de
questions distinctes que de modèles, autant de réponses distinctes, et aucun
moyen de savoir si la liste est complète.

**Traçabilité.** Lorsqu'une définition change, les modèles concernés peuvent
être identifiés plutôt que supposés. Le lien qui répond à une question sur les
données répond aussi à la question des conséquences d'une modification.

### Comment le lien est établi

Chaque élément d'un modèle logique peut être rattaché à un concept du
glossaire. Le rattachement est inscrit dans le modèle lui-même, et pas
seulement dans la documentation : les éléments qui signifient *Recorder* dans
l'ensemble des modèles peuvent donc être énumérés, plutôt que recherchés en
lisant chaque modèle l'un après l'autre.

Tous les éléments ne sont pas rattachés. Beaucoup sont propres à un seul modèle
et n'ont aucun concept de glossaire ; un élément sans rattachement n'est pas un
oubli.
