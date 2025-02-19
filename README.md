# 🤖 Marvin Discord Bot

Un bot Discord qui surveille et partage automatiquement les résultats des tests Marvin d'Epitech.

## 📋 Description

Ce bot surveille une boîte mail spécifique pour les résultats des tests Marvin, parse les fichiers de résultats, et envoie un résumé formaté sur un canal Discord désigné. Il vérifie automatiquement les nouveaux résultats toutes les 5 minutes.

## 🛠️ Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Dépendances

Installez les dépendances nécessaires avec :

```bash
pip install discord.py python-dotenv tqdm
```

### Configuration

1. Créez un fichier `.env` à la racine du projet avec les informations suivantes :

```env
EMAIL=votre_email@free.fr
PASSWORD=votre_mot_de_passe
DISCORD_TOKEN=votre_token_discord
DISCORD_CHANNEL_ID=id_du_canal
```

2. Assurez-vous d'avoir :
   - Créé un bot Discord et obtenu son token
   - Les permissions nécessaires pour le bot sur votre serveur Discord
   - Les identifiants de votre compte email Free

## 🚀 Utilisation

Pour lancer le bot :

```bash
python3 main.py
```

Le bot va :
- Se connecter à Discord
- Vérifier les nouveaux emails toutes les 5 minutes
- Afficher une barre de progression pour le temps d'attente
- Envoyer les résultats des tests sur le canal Discord configuré

## 📁 Structure du Projet

```
MarvinDiscord/
├── main.py           # Point d'entrée principal
├── marvin_bot.py     # Gestion du bot Discord
├── email_handler.py  # Gestion des emails
├── parser.py         # Parser des résultats de tests
└── .env             # Configuration (non versionné)
```

## 🔍 Fonctionnalités

- 📨 Surveillance automatique des emails
- 📝 Parse les fichiers de résultats de tests
- 💬 Formatage élégant pour Discord
- ⏳ Barre de progression pour le temps d'attente
- 🔄 Évite les doublons de messages
- 📊 Support des traces finales et daily

## ⚙️ Configuration Avancée

Dans `main.py`, vous pouvez ajuster :
- `check_interval` : Intervalle entre les vérifications (défaut : 300 secondes)
- Le format des messages Discord dans `parser.py`
- Les critères de recherche d'emails dans `email_handler.py`

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Push sur votre fork
5. Ouvrir une Pull Request

## 📜 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📧 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub.
