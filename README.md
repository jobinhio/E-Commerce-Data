
# Analyse des Données E-commerce

![E-Commerce-Data](./img/image.jpg)

Ce projet vise à analyser les comportements des clients, les performances des produits et les tendances d’achat à partir d’un jeu de données transactionnelles issu d’un site e-commerce britannique. L'approche adoptée permet non seulement de comprendre en profondeur les habitudes d'achat selon plusieurs dimensions (heure, jour, mois), mais aussi de segmenter la clientèle afin de proposer des actions marketing adaptées.

## Objectifs du Projet

- **Analyse des comportements d'achat**  
  Comprendre les habitudes selon l'heure, le jour et le mois pour optimiser la planification des campagnes marketing.

- **Évaluation de la performance produit**  
  Identifier les produits populaires et ceux posant problème (cas de retours fréquents), afin de mettre en place des actions correctives.

- **Segmentation client**  
  Utiliser la méthode RFM (Récence, Fréquence, Montant) et le clustering (K-means) pour définir des segments clients et personnaliser les actions.

- **Propositions d’améliorations et recommandations**  
  Développer des recommandations marketing basées sur des insights issus de l'analyse des comportements et de la segmentation.

## Contenu de l’Analyse

### 1. Exploration des Données

- **Chargement, nettoyage et enrichissement du dataset**  
  Traitement des données brutes pour assurer la qualité de l'analyse (gestion des valeurs manquantes, normalisation, etc.).
  
- **Création de variables dérivées**  
  Calcul de variables pertinentes telles que le montant d’achat, le taux de retour et la diversité des produits achetés pour enrichir les analyses.

### 2. Analyse Comportementale

- **Répartition des ventes**  
  Étude des pics d'activité et détermination des heures et jours les plus performants.
  
- **Analyse des paniers**  
  Calcul de la valeur moyenne des paniers et distinction entre clients actifs et inactifs.

### 3. Performance Produit

- **Top ventes et retours**  
  Identification des meilleurs vendeurs ainsi que des produits présentant un taux de retour supérieur à 20 %, indicateurs potentiels d’un problème de qualité ou de satisfaction client.

### 4. Segmentation Client

- **Méthode RFM**  
  Analyse de la récence, de la fréquence et du montant d’achat pour classer les clients.
  
- **Clustering via K-means**  
  Regroupement des clients en segments distincts. Une visualisation interactive en 3D permet d’illustrer ces clusters de manière géographique.

### 5. Recommandations et Actions

- **Actions marketing ciblées**  
  Élaboration de campagnes spécifiques en fonction des profils clients.
  
- **Optimisation de l’offre produit**  
  Proposition d’exclusions pour certains produits à risque lors d’opérations promotionnelles et amélioration des fiches produits et de la logistique.

## Technologies et Environnement

- **Langages et bibliothèques**  
  - Python (Pandas, NumPy, Scikit-learn)  
  - Visualisation avec Plotly & Seaborn  

- **Outils d'exploration**  
  - Jupyter Notebook pour l’analyse interactive et le prototypage

## Organisation du Code

- **`main.ipynb`**  
  Notebook principal regroupant les étapes d’analyse, de visualisation et de segmentation.
  
- **`functions/`**  
  Ensemble de fonctions personnalisées pour modulariser le traitement et l’analyse des données.

- **`data/`**  
  Dossier contenant les jeux de données brutes et les données traitées.

- **`img/`**  
  Dossier contenant les images et visualisations utilisées.
  
- **`README.md`**  
  Présentation et documentation complète du projet.
  
- **`requirements.txt`**  
  Liste des dépendances nécessaires pour reproduire l’environnement de développement.

## Résultats Clés

- **Comportement d'achat**  
  Les ventes se concentrent principalement entre **10h et 14h**, surtout en semaine, indiquant les créneaux où il est pertinent d’intensifier les actions marketing.
  
- **Retour produit**  
  Plusieurs produits présentent un taux de retour supérieur à 20 %, suggérant des points de vigilance sur la qualité ou l’adéquation aux attentes clients.
  
- **Segmentation réussie**  
  Grâce au clustering K-means et à la méthode RFM, les clients sont regroupés en segments distincts, permettant une personnalisation des offres.

## Contact

Pour toute question ou commentaire, n’hésitez pas à me contacter sur [LinkedIn](linkedin.com/in/job-congo-303908197) ou via mon [GitHub](https://github.com/jobinhio/congo). Ce projet est une vitrine de mon expertise en data science, et j'ai hâte de discuter de nouvelles idées ou de collaborations potentielles !
