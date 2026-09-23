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

<u>Sélection uniforme :</u> sélection aléatoire de manière uniforme sans interventionde la valeur d'adaptation. Probabilité de sélection : 1/p (p = nombre d'individus).     

