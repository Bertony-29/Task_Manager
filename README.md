# 🚀 Smart Task-Manager (Python & AI)
Une application web interactive de gestion de tâches développée avec Streamlit, intégrant une intelligence artificielle pour l'optimisation des priorités.

## 📋 Présentation
Ce projet est une solution moderne de productivité qui permet non seulement de gérer ses tâches quotidiennes, mais aussi de bénéficier de la puissance de l'IA pour organiser son emploi du temps. L'application analyse la liste des tâches et suggère des ajustements de priorité en fonction de l'urgence et de la description des activités.

## ✨ Fonctionnalités clés
- Interface Web Réactive : Développée avec Streamlit pour une expérience utilisateur fluide et intuitive.

- Organisation par IA : Intégration de l'API Google Gemini (gemini-2.5-flash) pour analyser et suggérer des priorités intelligentes.

- Gestion de Base de Données : Utilisation de SQLite pour assurer la persistance locale des tâches (stockage du titre, description, date et statut).

- Architecture Orientée Objet : Code structuré avec une classe Tache pour une meilleure maintenabilité et évolutivité.

- Système CRUD Complet : Création, lecture, modification et suppression des tâches via l'interface graphique.

## 🛠️ Stack Technique
- Langage : Python 3.x

- Framework UI : Streamlit

- IA Générative : Google Generative AI (Gemini SDK)

- Base de données : SQLite3 

## 🔧 Installation et Configuration
### Cloner le dépôt :
- git clone https://github.com/ton-pseudo/smart-task-manager.git
- cd smart-task-manager

### Installer les dépendances :
- pip install streamlit google-generativeai

### Configuration de l'API :
- Créez un dossier .streamlit/ à la racine et un fichier secrets.toml à l'intérieur pour y ajouter votre clé API :
  GEMINI_CLE_API = "VOTRE_CLE_API_GOOGLE"

### Lancer l'application :
- streamlit run app.py

## 📂 Structure du projet
- app.py : Point d'entrée principal de l'application et logique de l'interface.
- tache.py : Définition de la classe Tache (modèle de données).
- tasks.db : Base de données SQLite générée automatiquement au premier lancement.

Projet réalisé en autonomie pour explorer les capacités des LLM dans les outils de productivité quotidienne.
