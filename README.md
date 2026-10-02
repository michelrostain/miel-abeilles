# **Miel et abielles**    

### **Les principes de l'évolution**    

**<u>Les termes principaux :</u>** 
Dans la mise en pratique informatique de la théorie de l'évolution, plusieurs concept sont à reporter dans le monde informatique pour permettre la résolution de problèmes. Ces problèmes sont généralement de très grandes envergures (par exemple avec un nombre de solution possible, dans notre cas de 1,5*10^26).     

<u>Fitness :</u> capacité d'un individu à survuvre et à se reproduire. En informatique, il s'agit de la capacité d'un élément porteur d'une des solutions à traverser les générations et à transmettre toute ou partie de cette soultion à une ou plusieurs génération(s) suivante(s).     

<u>Sélection naturelle :</u> corrélation entre la valeur d'un trait et le fitness.     

<u>Phénotype :</u> ensemble de traits. En informatique, c'est l'ensemble de data qui originalise un élément. Ces traits peuvent être échangés lors d'enjembement (crossover) pour créer un nouvel élément porteur d'un nouveau phénotype.     

<u>Fonction de fitness :</u> relation entre le phénotype et la mesure du fitness. La pente de cette fonction est appelée coefficiant de sélection.     

<u>Agent de sélection :</u> variable de l'envoronnement qui crée une pression de sélection sur les individus.    

<u>Performance :</u> résultat de la combinaison de la valeur de plusieurs traits.     

**Les data d'un éléments peuvent changer de quatre manières différentes :**     
<u>Mutation :</u> une mutation des data constitutives d'un éléments (qui viendra affecter les éléments des générations suivantes si cet élément est sélectionné pour créer la génération suivante). Substitution aléatoire de data entre deux élément. Le taux de mutation doit être choisi faible.    

<u>Dérive génétique :</u> l'échantillonnage ne correspond pas à la réalité des datas qui constitue la majorité des éléments.    

<u>Flux génique :</u> lorsque un élément issu d'une autre propulation vient dans la population étudiée et affecte les data des éléments consécutives au crossover.    

<u>Sélection naturelle :</u> au sein d'une population, la différence de phénotype entre les éléments de cette population permettent la sélection de certains individus plutôt que d'autres pour créer la génération suivante.      

<u>Enjambement ou crossover :</u> échange de data entre deux éléments.     

<u>Sélection :</u> déterminer quels individus sont les plus enclins à obtenir les meilleurs résultats.    

**<u>Les techniques de sélection :</u>**      
<u>Sélection par rang :</u> consiste à conserver K individus qui possèdent les meilleurs scores.    

<u>Sélection proportionnelle à l'adaptation :</u> Roue de la fortune biaisée : les meilleurs éléments ont une part plus importante sur la roue.    

<u>Sélection par tournoi :</u> Sélection proportionnelle sur des paires d'individus qui a le meilleur rôle.      

<u>Sélection uniforme :</u> sélection aléatoire de manière uniforme sans intervention de la valeur d'adaptation. Probabilité de sélection : 1/p (p = nombre d'individus).     


### **L'algorithme génétique**     

Une algorithme génétique est un algorithme qui permet, d'une génération d'éléments constitué de data à une autre, de faire évoluer les peerformances de résolution de problèmes de grandes envergure. Le but est d'obtenir une solution approchée à un problème d'optimisation lorsqu'il n'existe pas de méthode exacte.    


**<u>Application informatique :</u>**      

Il s'agit alors de créer des fonctions ou des méthodes de classes qui représentent les principaux éléments constitutifs de la théorie de l'évolution.     

<u>Population :</u>     
La population est créée de manière aléatoire et est un ensemble de solutions candidates. Ici nous créeons un population de 100 individus.     

<u>Fonction d'aptitude (Fitness) :</u>     
c'est la mesure de l'aptitude  d'un individu à résoudre le problème qui nous intéresse. Une valeur est attribué à chaque individu, un classement est effectué en fonction de celle ci.    
Ici nous attribuons un score à chaque individu, ce score est la somme des distances parcourue, les plus petit scores étant les meilleurs.    

<u>Fonction de sélection :</u>     
Applique une sélection comme celles décrites plus haut, afin de ne garder que les meilleurs individus pour créer la génération suivante.     

<u>Fonction de croisement (crossover):</u>     
Création d'un nouvel élément en fonction de deux autres éléments.     

<u>Fonction de mutation :</u>     
Altération des data d'un élément de manière aléatoire. Dans notre cas, ce sera l'échange des coordonnées de quelques fleurs (au minimum 2).    

<u>Élitisme et renouvellement de la population :</u> 

À chaque génération, les abeilles sont classées selon leur distance totale. Les meilleures sont conservées directement dans la génération suivante grâce à l'élitisme.

Les autres sont remplacées par de nouveaux individus créés par sélection, crossover et mutation. La proportion d'abeilles remplacées dépend du taux de reproduction, tandis que la population reste constante à 100 abeilles.   


## Expérimentation et choix des paramètres

### Méthodologie
Afin de déterminer les paramètres de l'algorithme génétique, nous avons réalisé plusieurs séries d'expériences.

Pour chaque configuration, l'algorithme a été exécuté 10 fois pendant 100 générations. Nous avons utilisé les mêmes graines aléatoires (`random.seed`) pour chaque configuration afin que les différentes valeurs testées commencent avec les mêmes populations initiales.

L'algorithme reste stochastique : chaque exécution utilise une population initiale différente ainsi que des opérations aléatoires de sélection, crossover et mutation. L'utilisation des mêmes graines permet simplement de rendre les configurations plus comparables et les expériences reproductibles.

Pour comparer les configurations, nous avons calculé la distance finale moyenne de la meilleure abeille sur les 10 exécutions. Une distance plus faible correspond donc à une meilleure performance.

Les paramètres ont été testés progressivement : après chaque expérience, le paramètre donnant la plus faible distance moyenne parmi les valeurs testées a été conservé pour l'expérience suivante.

### Taux de mutation

Nous avons d'abord comparé plusieurs taux de mutation afin d'étudier leur influence sur l'évolution de la population.

| Taux de mutation | Distance finale moyenne |
|------------------|------------------------:|
| 0                | 12 555,86 |
| 0,05             | 12 567,20 |
| 0,10             | 12 438,09 |
| 0,20             | 11 814,38 |
| 0,40             | 12 344,53 |

Parmi les valeurs testées, un taux de mutation de **0,20** a obtenu la distance finale moyenne la plus faible. Nous avons donc conservé cette valeur pour les expériences suivantes.

### Taille du tournoi

Après avoir fixé le taux de mutation à 0,20, nous avons comparé différentes tailles de tournoi pour la sélection des parents.

| Taille du tournoi | Distance finale moyenne |
|-------------------|------------------------:|
| 2                 | 12 668,68 |
| 3                 | 11 814,38 |
| 5                 | 11 926,05 |
| 10                | 11 545,15 |

La taille du tournoi influence la pression de sélection : plus le tournoi est grand, plus les abeilles ayant de bonnes performances ont de chances d'être sélectionnées comme parents.

Parmi les valeurs testées, une taille de tournoi de **10** a obtenu la distance finale moyenne la plus faible. Nous avons donc conservé cette valeur pour la suite des expériences.

### Taux de reproduction

Après avoir fixé le taux de mutation à 0,20 et la taille du tournoi à 10, nous avons testé différents taux de reproduction.

Le taux de reproduction détermine la proportion de la population qui est remplacée par de nouveaux individus à chaque génération. Les meilleures abeilles restantes sont conservées grâce à l'élitisme.

| Taux de reproduction | Distance finale moyenne |
|----------------------|------------------------:|
| 0,10                 | 13 912,77 |
| 0,30                 | 11 545,15 |
| 0,50                 | 10 236,10 |
| 0,70                 | 10 377,17 |

Parmi les valeurs testées, un taux de reproduction de **0,50** a obtenu la distance finale moyenne la plus faible.

Nous avons donc choisi de conserver **50 % des meilleures abeilles** et de remplacer les **50 % restantes par de nouveaux individus** à chaque génération.

### Mutation fixe et mutation évolutive

Nous avons ensuite comparé deux stratégies de mutation :

- un taux de mutation **fixe de 0,20** ;
- un taux de mutation **évolutif**, diminuant linéairement de 0,40 à 0,01 au cours des 100 générations.

L'objectif du taux évolutif était de favoriser davantage l'exploration au début de l'évolution, puis de réduire progressivement les mutations afin de stabiliser les solutions obtenues.

| Stratégie de mutation | Distance finale moyenne |
|-----------------------|------------------------:|
| Fixe (0,20)           | 10 236,10 |
| Évolutive (0,40 → 0,01) | 10 772,36 |

Dans nos expériences, le taux fixe de **0,20** a obtenu une distance finale moyenne plus faible que le taux évolutif testé.

Nous avons donc conservé un taux de mutation fixe de **0,20** pour le paramétrage final. Ce résultat concerne cependant la stratégie évolutive testée (de 0,40 à 0,01) et ne signifie pas qu'un taux fixe est toujours plus performant qu'un taux évolutif.

### Paramétrage final

À partir des résultats obtenus lors des différentes expériences, nous avons retenu le paramétrage suivant :

| Paramètre | Valeur |
|-----------|-------:|
| Nombre d'abeilles | 100 |
| Nombre de générations | 100 |
| Taux de mutation | 0,20 |
| Taille du tournoi | 10 |
| Taux de reproduction | 0,50 |
| Type de mutation | Fixe |

Ces paramètres correspondent aux meilleurs résultats obtenus au cours de notre démarche expérimentale parmi les configurations testées.

Le paramétrage a été déterminé de manière progressive : à chaque étape, le paramètre donnant la plus faible distance finale moyenne a été conservé pour tester le paramètre suivant. Cette méthode permet de limiter le nombre d'expériences, mais ne teste pas toutes les combinaisons possibles entre les différents paramètres.

## Visualisations

Afin d'observer les résultats de l'algorithme génétique, nos avons créé trois visualisations.

### Évolution de la population

Nous représentons la distance de la reine et la distance moyenne de la population au cours des générations. Cela permet d'observer l'amélioration progressive des solutions et la convergence de la population.

### Chemin de la meilleure abeille

Le chemin de la meilleure abeille de la dernière génération est représenté sur le champ de fleurs. Les points correspondent aux fleurs et les lignes montrent l'ordre dans lequel elles sont visitées, depuis la ruche jusqu'au retour à celle-ci.

### Graphe généalogique

Chaque nouvelle abeille conserve une référence vers ses deux parents. À partir de la reine finale, nous parcourons récursivement ses ancêtres afin de construire un graphe généalogique orienté.

Les générations sont représentes sur différents niveaux, ce qui permet de visualiser la transmission des chemins au cours de l'évolution.