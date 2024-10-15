# Réalisation d’une application pour calculer l’impact environnemental de sa consommation alimentaire.

### Contexte 

Le programme Agribalyse® produit des données de référence sur les impacts environnementaux des produits agricoles et alimentaires. 
Les méthodologies et les données ont été élaborées et validées dans le cadre d’un partenariat veillant à leur qualité et leur transparence 
(ADEME, INRAE, les instituts techniques agricoles et agroalimentaires, des experts indépendants et des cabinets d’études).

Agribalyse® est la base de données publique française la plus exhaustive d’indicateurs environnementaux des produits agricoles et alimentaires 
fondés sur l’Analyse du Cycle de Vie. Elle fournit des indicateurs d’impacts environnementaux :
* des principales productions agricoles françaises,
* des principaux produits alimentaires consommés en France.

À chaque étape de la chaîne, des bilans de matières, d’énergie et d’émissions de polluants sont réalisés et agrégés sous forme d’un jeu d’indicateurs environnementaux.
14 indicateurs sont fournis pour chaque produit. Il s’agit des indicateurs préconisés par la Commission Européenne (projet Product Environmental Footprint).
Ces 14 indicateurs ont vocation à couvrir un ensemble d’enjeux environnementaux (qualité de l’eau, de l’air, climat, sols).

L’ensemble des indicateurs est ramené à la fabrication de 1 kg de produit alimentaire.

Pour autant il n'existe pas d'outil dédiée permettant, à partir de ces données, d'évaluer l'impact sur l'environnement de sa consommation alimentaire de manière précise. 

J'ai donc développé une application pour calculer l'impact environnemental à partir de données type de consommation.

### Objectifs

Créer une application accessible pour que chaque consommateur puisse évaluer l'impact de son alimentation sur l’environnement et identifier des leviers d’améliorations dans ses choix de consommation. Cela en identifiant des profils alimentaires types.

La démarche a été la suivante : 

* Étudiez attentivement toutes les données fournies ;
* Ajouter une note pour l'agriculture conventionnelle/biologique de Table de pesée EF3 ;
* Créez des buckets moyens qui correspondent aux 7 plans existants ;
* Analysez l’impact environnemental de la consommation de ces paniers ;
* Ajouter artificiellement des profils à partir de ces bacs moyens ;
* Entraîner un modèle d'apprentissage automatique pour prédire le score EF en fonction de type de consommation.

### Données

 Le projet "FarmPyStep" est issu de la base de donnée Agribalyse 3.0 : https://doc.agribalyse.fr/documentation

 Une vidéo de présentation de la démarche Agribalyse est disponiblesur ce lien : https://youtu.be/DNdv0TbxJgc.




