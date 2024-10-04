# Réalisation d’une application pour calculer l’impact environnemental de sa consommation alimentaire.

Bonjour à tous!

Bienvenue dans le notebook dédié au projet "FarmPyStep" et issu de la base de donnée Agribalyse 3.0 (https://doc.agribalyse.fr/documentation) 

Une vidéo de présentation est disponible dans le lien ci-contre : https://youtu.be/DNdv0TbxJgc.

**Description du projet**

Le programme Agribalyse® produit des données de référence sur les impacts environnementaux des produits agricoles et alimentaires. 
Les méthodologies et les données ont été élaborées et validées dans le cadre d’un partenariat veillant à leur qualité et leur transparence 
(ADEME, INRAE, les instituts techniques agricoles et agroalimentaires, des experts indépendants et des cabinets d’études).

Agribalyse® est la base de données publique française la plus exhaustive d’indicateurs environnementaux des produits agricoles et alimentaires 
fondés sur l’Analyse du Cycle de Vie. Elle fournit des indicateurs d’impacts environnementaux :

* des principales productions agricoles françaises,
* des principaux produits alimentaires consommés en France.

À chaque étape de la chaîne, des bilans de matières, d’énergie et d’émissions de polluants sont réalisés et agrégés sous forme d’un jeu d’indicateurs environnementaux.
14 indicateurs sont fournis pour chaque produit.
Il s’agit des indicateurs préconisés par la Commission Européenne (projet Product Environmental Footprint).
Ces 14 indicateurs ont vocation à couvrir un ensemble d’enjeux environnementaux (qualité de l’eau, de l’air, climat, sols).
À noter que l’ensemble des indicateurs est ramené à la fabrication de 1 kg de produit alimentaire.


**Contexte & objectifs :**

Le changement climatique est une réalité qui se manifeste sous nos yeux : inondations de
juillet en Allemagne et en Belgique, dôme de chaleur accompagné de violents incendies au
Canada. Le dernier rapport du Groupe d’expert.es intergouvernemental sur l’évolution du
climat (GIEC) confirme l’influence humaine comme un fait établi et indiscutable.

J'ai travaillé sur la base de données Agribalyse créée par Agence de l'Environnement et de la Maîtrise de l'Energie (ADEME), permettant
découvrez l'impact des produits agricoles sur l'environnement en suivant la méthode analyse du cycle de vie.
J'ai  ont développé une application pour calculer l'impact environnemental à partir de données
type de consommation.

*Idée de départ :* identifier des profils alimentaires types.

*Objectifs :*
* Étudiez attentivement toutes les données fournies
* Ajouter une note pour l'agriculture conventionnelle/biologique de Table de pesée EF3
* Créez des buckets moyens qui correspondent aux 7 plans existants
* Analysez l’impact environnemental de la consommation de ces paniers
* Ajouter artificiellement des profils à partir de ces bacs moyens
* Entraîner un modèle d'apprentissage automatique pour prédire le score EF en fonction de type de consommation.

Le but : créer une application accessible pour que tout consommateur puisse évaluer
son impact sur l’environnement et identifier les leviers d’améliorations dans ses choix de
consommation.


