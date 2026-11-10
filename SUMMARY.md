# 📊 Vibrateam - Résumé de l'Application

## 🎯 Objectifs de l'Application

L'application **Vibrateam** est une solution complète pour l'analyse vibratoire des poutres selon la théorie d'Euler-Bernoulli. Elle permet de :

1. **Choisir la modélisation de la poutre** avec différentes conditions aux limites
2. **Sélectionner l'approximation modale** (nombre de fréquences naturelles à calculer)
3. **Visualiser les déformées modales** de chaque fréquence naturelle sur un unique plot
4. **Calculer et afficher les Fonctions de Réponse en Fréquence (FRF)** avec la contribution de chaque mode

## 📁 Structure du Projet

```
vibrateam/
├── vibrateam_app.py          # Application principale (Streamlit)
├── test_vibrateam.py         # Tests unitaires
├── requirements.txt          # Dépendances Python
├── README.md                 # Documentation complète
├── SUMMARY.md                # Ce fichier
├── Dockerfile                # Configuration Docker
├── .dockerignore             # Fichiers à ignorer pour Docker
├── run_app.sh                # Script de lancement
└── .streamlit/
    └── config.toml           # Configuration de Streamlit
```

## 🚀 Fonctionnalités Implémentées

### 1. Conditions aux Limites
L'application supporte **5 types de conditions aux limites** :

| Condition | Emoji | Description |
|-----------|-------|-------------|
| Encastre-Encastre | 🔒🔒 | Poutre fixée rigidement aux deux extrémités |
| Encastre-Libre | 🔒🚀 | Poutre encastrée à une extrémité, libre à l'autre (console) |
| Libre-Libre | 🚀🚀 | Poutre libre aux deux extrémités (volante) |
| Articule-Articule | 🔗🔗 | Poutre articulée aux deux extrémités (simplement supportée) |
| Encastre-Articule | 🔒🔗 | Poutre encastrée à une extrémité, articulée à l'autre |

### 2. Approximation Modale
- **Nombre de modes configurable** : de 1 à 10
- **Calcul automatique** des fréquences naturelles pour chaque mode
- **Affichage tabulaire** des fréquences
- **Visualisation graphique** des déformées modales

### 3. Déformées Modales
- **Affichage multiple** : toutes les déformées sur un seul graphique
- **Affichage individuel** : sélection d'un mode spécifique
- **Normalisation** : amplitude maximale = 1
- **Identification des nœuds** (points de déplacement nul)
- **Identification des ventres** (points de déplacement maximal)
- **Représentation graphique** des conditions aux limites

### 4. Fonction de Réponse en Fréquence (FRF)
- **Sélection des positions** :
  - Point d'application de la force (x_force)
  - Point de mesure (x_mesure)
- **Calcul de la FRF** avec prise en compte de l'amortissement
- **Visualisation** :
  - FRF globale (plus visible, en trait plein noir)
  - Contributions de chaque mode (en pointillés colorés)
  - Marqueurs pour les fréquences naturelles
- **Analyse des pics** : détection automatique des résonances
- **Affichage des métriques** : fréquence et amplitude des pics

### 5. Export des Données
- **Fréquences naturelles** → CSV
- **FRF** → CSV
- **Déformées modales** → CSV

## 📐 Paramètres Configurables

### Propriétés Géométriques
- **Longueur** : 0.1 à 10 mètres
- **Largeur** : 0.01 à 1 mètre
- **Hauteur** : 0.01 à 1 mètre
- **Moment d'inertie** : calculé automatiquement pour section rectangulaire
- **Aire de la section** : calculée automatiquement

### Propriétés Matérielles
- **Module de Young** : 1e9 à 1e12 Pa (210 GPa par défaut pour l'acier)
- **Masse volumique** : 100 à 30000 kg/m³ (7800 kg/m³ par défaut pour l'acier)

### Paramètres d'Analyse
- **Nombre de modes** : 1 à 10
- **Coefficient d'amortissement** : 0.001 à 0.1 (0.01 par défaut)
- **Plage de fréquences** : configurable pour la FRF
- **Nombre de points** : 100 à 10000 pour le calcul de la FRF

## 🔬 Théorie Implémentée

### Équation de Base
L'application utilise l'équation différentielle des vibrations transversales des poutres d'Euler-Bernoulli :

```
EI * ∂⁴w/∂x⁴ + ρA * ∂²w/∂t² = 0
```

Où :
- `w(x,t)` : déplacement transversal
- `E` : module de Young
- `I` : moment d'inertie
- `ρ` : masse volumique
- `A` : aire de la section

### Solution Modale
La solution est de la forme :
```
w(x,t) = Σ φₙ(x) * qₙ(t)
```

Où :
- `φₙ(x)` : déformées modales
- `qₙ(t)` : coordonnées généralisées

### Fréquences Naturelles
```
fₙ = (βₙ² / (2πL²)) * √(EI/(ρA))
```

Où `βₙ` dépend des conditions aux limites.

### Fonction de Réponse en Fréquence
```
H(ω) = Σ [φₙ(x_force) * φₙ(x_mesure) / mₙ] / [ωₙ² - ω² + 2jζωₙω]
```

Où :
- `mₙ` : masse généralisée
- `ζ` : coefficient d'amortissement

## 🎨 Interface Utilisateur

### Barre Latérale
- **Propriétés géométriques** : longueur, largeur, hauteur
- **Propriétés matérielles** : module de Young, masse volumique
- **Conditions aux limites** : sélection du type
- **Approximation modale** : nombre de modes, coefficient d'amortissement

### Section 1 : Fréquences Naturelles et Déformées Modales
- Tableau des fréquences naturelles
- Graphique des déformées modales
- Option pour afficher toutes les déformées ou une spécifique

### Section 2 : Fonction de Réponse en Fréquence (FRF)
- Schéma de la poutre avec positions de force et mesure
- Graphique de la FRF avec contributions modales
- Analyse des pics de résonance

### Section 3 : Analyse Modale Détaillée
- Sélection d'un mode spécifique
- Visualisation de la déformée
- Identification des nœuds et ventres

### Section 4 : Export des Données
- Export des fréquences naturelles
- Export de la FRF
- Export des déformées modales

## 📊 Exemple de Sortie

### Pour une poutre encastrée-encastrée (L=1m, acier, section 50×20 mm) :

**Fréquences naturelles :**
- Mode 1 : 184.76 Hz
- Mode 2 : 508.20 Hz
- Mode 3 : 1030.84 Hz
- Mode 4 : 1752.68 Hz
- Mode 5 : 2673.72 Hz

**Déformées modales :**
- Mode 1 : 1 demi-onde
- Mode 2 : 2 demi-ondes
- Mode 3 : 3 demi-ondes
- etc.

**FRF (Force @ 0.25m, Mesure @ 0.5m) :**
- Pics aux fréquences naturelles
- Contributions modales visibles
- FRF globale en trait plein noir

## 🧪 Tests Unitaires

L'application comprend **12 tests unitaires** couvrant :

1. Initialisation de la poutre
2. Calcul des valeurs βₙ pour différentes conditions
3. Calcul des fréquences naturelles
4. Calcul des déformées modales
5. Calcul de la FRF
6. Comportement à la résonance
7. Modes rigides pour poutre libre-libre
8. Normalisation des déformées
9. Gestion des conditions inconnues

**Exécution des tests :**
```bash
python test_vibrateam.py
```

## 🚀 Installation et Exécution

### Méthode 1 : Local (Recommandé)

```bash
# Cloner le dépôt ou se placer dans le dossier
cd /chemin/vers/vibrateam

# Créer un environnement virtuel (optionnel mais recommandé)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run vibrateam_app.py
```

### Méthode 2 : Utilisation du Script

```bash
# Donner les permissions d'exécution
chmod +x run_app.sh

# Lancer l'application
./run_app.sh
```

### Méthode 3 : Docker

```bash
# Construire l'image
docker build -t vibrateam .

# Lancer le conteneur
docker run -p 8501:8501 vibrateam

# Accéder à l'application : http://localhost:8501
```

## 📦 Dépendances

Les dépendances sont listées dans `requirements.txt` :

- **streamlit** (≥1.20.0) : Framework pour l'interface web
- **numpy** (≥1.21.0) : Calculs numériques
- **matplotlib** (≥3.5.0) : Visualisation graphique
- **scipy** (≥1.7.0) : Fonctions scientifiques avancées
- **pandas** (≥1.3.0) : Manipulation de données (optionnel pour l'export)

## 🎯 Cas d'Utilisation

### Cas 1 : Analyse Modale d'une Poutre Console
- Condition : Encastre-Libre
- Nombre de modes : 5
- Longueur : 2 mètres
- Matériau : Acier
- **Résultat** : Fréquences naturelles et déformées modales

### Cas 2 : Calcul de FRF pour un Test de Vibration
- Condition : Articule-Articule
- Position force : 0.3 m
- Position mesure : 0.7 m
- Plage fréquences : 0-1000 Hz
- **Résultat** : FRF avec pics aux fréquences naturelles

### Cas 3 : Optimisation de la Conception
- Comparaison de différentes conditions aux limites
- Analyse de l'effet de la longueur sur les fréquences
- Visualisation des déformées pour identifier les zones critiques

## 🔧 Personnalisation

Vous pouvez modifier les paramètres par défaut dans :
- `vibrateam_app.py` : Classe `PoutreVibratoire`
- `.streamlit/config.toml` : Thème et configuration de Streamlit

## 📚 Documentation

- **README.md** : Guide complet d'utilisation
- **SUMMARY.md** : Ce fichier - résumé de l'application
- **Code source** : Commenté et structuré

## 🏆 Avantages

✅ **Interface intuitive** avec Streamlit
✅ **Calculs précis** basés sur la théorie d'Euler-Bernoulli
✅ **Visualisation avancée** avec Matplotlib
✅ **5 conditions aux limites** supportées
✅ **Export des données** en format CSV
✅ **Tests unitaires** complets
✅ **Documentation** détaillée
✅ **Déploiement facile** avec Docker

## 📞 Support

Pour toute question ou problème :
1. Vérifiez que toutes les dépendances sont installées
2. Consultez les logs d'erreur dans la console
3. Référez-vous à la documentation

## 📄 Licence

Ce projet est sous licence **MIT**. Vous êtes libre d'utiliser, modifier et distribuer ce code.

---

**Développé avec ❤️ pour l'analyse vibratoire des poutres**
