# ❤️ Monod-Crush

MonodCrush est un réseau social pour le lycée. Il permet aussi aux éleves de se faire des amis ou de trouver l'amour.
Le site est en ligne et disponible [ici](https://monodcrush.fr)

Les fonctionnalités suivantes sont dispoibles : 
- Création et édition de profil,
- Création et modification de posts,
- Modération automatique des posts par IA (https://sightengine.com)
- Signalement des posts des autres utilisateurs,
- Like des posts des autres utilisateurs,
- Statistiques dans le panneau administrateur,
- Gestion des signalements dans le panneau administrateur
- Site 100% responsive (desktop, tablette et smartphone)
- Workflow de test pour le CI / CD

Pour tester le site vous pouvez vous connecter avec les comptes suivants pour tester les différentes fonctionnalités : 
- Username : admin / Mot de passe : admin -> Compte administrateur
- Username : user / Mot de passe : user -> Compte lambda

Pour lancer le site en local, lancez le fichier wsgi.py !

## ⚙️ Partie technique

### Version de Python
Versions de Python compatibles avec le projet : **3.7+**

### Bibliothèques
```
Flask==2.0.3
pytest==7.0.1
coverage==6.3.2
Faker==13.2.0
requests==2.27.1

Bulma==0.9.3 (CSS)
```
La liste des bibliothèques est aussi disponible dans le fichier "requirements.txt"

### Sitographie
- **StackOverflow** (https://stackoverflow.com/),
- **MDN Web Doc** (https://developer.mozilla.org/fr/),
- Documentation de **Flask** (https://flask.palletsprojects.com/en/2.0.x/),
- Documentation de **SQL** (https://sql.sh/)

## 🚩 Projet

### Avancement
Le site n'est pas terminé à 100%, les fonctionnalités suivantes sont prévues dans de prochaines mises à jour : 
- Abonnements à d'autres utilisateurs (comme sur Facebook, Instagram)
- Map Instagram : carte des profils Instagram des utilisateurs du site avec leurs relations communes
- Commentaires sous les posts
- voir https://github.com/BenoitObelia/Monod-Crush/issues

### Répartition
- **Jules** : Création de la base de données (init-db, populate-db), création, édition, suppression des posts (blog), création du schéma de la base de données (schema.sql), système de signalement des posts (Python, HTML), système de likes (Python, HTML)
- **Benoît** : Système de connection et d'inscription (HTML), système de profil et d'édition du profil (HTML, Python et SQL), statistiques du panel admin (HTML, Python et SQL) + intégralité du fichier user.py, fichier user_helper, fonctions de vérification des données (Python)
- **Killian** : Gestion des erreurs (HTML et Python), création du logo (CSS), barre de recherche (Python, HTML), système de likes (Python, HTML)
