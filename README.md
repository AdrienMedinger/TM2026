# BloomWay

BloomWay est un site e-commerce de vente d'habits réalisé avec Django, dans le cadre de mon travail de maturité

## Fonctionalités

- Inscription, connexion et déconnexion des utilisateurs

- Catalogue de produits classés par catégorie avec possibilité de les filtrer par catégorie, taille, couleur, prix

- Page détail produit: plusieurs images, choix de la taille, affichage du stock

- Panier:ajouter, modifier la quantité, supprimer, affichage des produits dans le panier avec calcul du total pour chaque produit et sa quantité et un total pour tout le panier

- Passage de la commande:information de livraison, facturation, paiement simulé (à cause d'un problème avec strip)

- Mail de confirmation à la fin de la commande

- Historique des commandes passées avec un détail ma commande pour chacune d'entre elle

- tableau de bord pour l'administrateur commandes envoyées/pas envoyées


## Prérequis

- **Python** (version 3.9.6 ou une plus récente)
- **Django** (version 4.2.30)
- **Environnement virtuel** (Venv)
- **Pip** (normalement inclus dans python)
- **Pillow** (pour ajouter des photos au site)
- **Git** 


## Installation
Suivez ces étapes une par une afin d'installer mon site 


### 1. Installation de Python et de pip
Avant de commencer le code, il faut vérifier que python est bien installé et pip inclus


```bash
  python --version
  pip --version
```
si cette première ligne ne fonctionne pas, alors tapez la ligne suivante:

```bash
  python3 --version
```

### 2. Cloner le dépôt 

```bash
   git clone https://github.com/AdrienMedinger/TM2026.git
   cd Bloomway
```
### 3. Créer et activer un environnement virtuel

```bash
   python -m venv venv
```
    Windows
```bash
   venv\Scripts\activate
```
    macOS / Linux
```bash
   source venv/bin/activate
```
### 3. Installer les dépendances

```bash
   pip install -r requirements.txt
```

### 4. Création d'une migration puis de la base de donnée

```bash
python manage.py makemigrations

python manage.py migrate
```

### 5. Créer un compte admin 
```bash
   python manage.py createsuperuser
```
### 6. Lancer le serveur
```bash
python manage.py runserver
```
### 7. Ouvrir le site 
 - http://127.0.0.1:8000/ pour le site clients
 - http://127.0.0.1:8000/admin/ pour l'administration

## Outils utilisés 
- Python (logique du site et côté serveur: views, models, etc..)
- Django (framework qui structure le site 
- HTML (structure de chaque page)
- CSS (mise en forme personnalisée)
- W3.CSS (bibliothèque CSS toute faite)
- Javascript (animation sur les pages ex:menu latéral)
- SQLite (base de données)
- Github (sauvegarder le code)


## Auteur 

Adrien Medinger






























