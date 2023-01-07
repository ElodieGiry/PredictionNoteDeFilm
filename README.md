# PredictionNoteDeFilm
Projet prédiction notes de film Allo Ciné

Ce projet a été réalisé par Elodie Giry et Lydia Soltani

## Analyse descriptive
Analyse descriptive et statistiques sur les données des commentaires

## SVM
Création du dictionnaire contenant les mots des commentaires

Création des fichiers SVM d'entraînement (train.svm) et de test (test.svm)

## Réseau de neurones
Création d'un réseau de neurones profond pour prédire les notes

Utilisation du modèle Camembert pour prédire les notes

## Lexique sentimentale
Calcul de la polarité de chaque commentaire à partir de la bibliothéque Python TextBlob

Calcul de la polarité (positif, neutre et négatif) de chaque mot de chaque commentaire à partir d'un lexique sentimentale

 ## Méta données
 
Moyenne et écart-type des notes de chaque utilisateurs présent dans le corpus de Train. Ensuite nous avons ajouté dans le SVM les moyennes et écart-type des utilisateurs qui étaient présents dans le corpus de train et de test. 

## Fichier de formatage pour évaluation sur Pedago
Pour convertir le fichier contenant les notes prédites au format adéquat pour l'évaluation sur la plateforme Pedago (review_id note avec virgule /5)
