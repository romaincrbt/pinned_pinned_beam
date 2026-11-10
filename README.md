# 📊 Vibrateam - Analyse Vibratoire des Poutres

Une application complète pour l'analyse modale et des Fonctions de Réponse en Fréquence (FRF) des poutres selon la théorie d'Euler-Bernoulli.

## 🚀 Installation

### Prérequis
- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
# Cloner le dépôt ou se placer dans le dossier
cd /chemin/vers/vibrateam

# Créer un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate  # Sur Linux/Mac
# ou
venv\Scripts\activate  # Sur Windows

# Installer les dépendances
pip install -r requirements.txt
```

## 🏃‍♂️ Exécution

```bash
# Lancer l'application Streamlit
streamlit run vibrateam_app.py
```

L'application s'ouvrira dans votre navigateur par défaut à l'adresse `http://localhost:8501`.

## 📋 Fonctionnalités

### 1. Sélection des conditions aux limites
L'application propose 5 types de conditions aux limites pour la poutre :
- **Encastre-Encastre** 🔒🔒 : Poutre fixée rigidement aux deux extrémités
- **Encastre-Libre** 🔒🚀 : Poutre encastrée à une extrémité, libre à l'autre (console)
- **Libre-Libre** 🚀🚀 : Poutre libre aux deux extrémités (volante)
- **Articule-Articule** 🔗🔗 : Poutre articulée aux deux extrémités (simplement supportée)
- **Encastre-Articule** 🔒🔗 : Poutre encastrée à une extrémité, articulée à l'autre

### 2. Approximation modale
- Sélection du nombre de modes à calculer (1 à 10)
- Calcul automatique des fréquences naturelles pour chaque mode
- Affichage des fréquences dans un tableau

### 3. Visualisation des déformées modales
- Affichage de toutes les déformées modales sur un seul graphique
- Option pour afficher une déformée modale spécifique
- Visualisation des nœuds (points de déplacement nul) et des ventres (points de déplacement maximal)
- Représentation graphique des conditions aux limites

### 4. Fonction de Réponse en Fréquence (FRF)
- Sélection des positions de la force d'excitation et de mesure
- Calcul de la FRF avec prise en compte de l'amortissement
- Visualisation de la FRF globale et des contributions de chaque mode
- Détection automatique des pics de la FRF
- Analyse des fréquences de résonance

### 5. Export des données
- Export des fréquences naturelles au format CSV
- Export de la FRF au format CSV
- Export des déformées modales au format CSV

## 📐 Paramètres personnalisables

### Propriétés géométriques
- Longueur de la poutre (m)
- Largeur de la section (m)
- Hauteur de la section (m)

### Propriétés matérielles
- Module de Young (Pa) - par défaut : 210 GPa (acier)
- Masse volumique (kg/m³) - par défaut : 7800 kg/m³ (acier)

### Paramètres d'analyse
- Nombre de modes (1-10)
- Coefficient d'amortissement (0.001-0.1)
- Plage de fréquences pour la FRF
- Nombre de points pour le calcul de la FRF

## 📚 Théorie

L'application utilise l'équation différentielle des vibrations transversales des poutres d'Euler-Bernoulli :

```
EI * ∂⁴w/∂x⁴ + ρA * ∂²w/∂t² = 0
```

Où :
- `w(x,t)` : déplacement transversal
- `E` : module de Young
- `I` : moment d'inertie de la section
- `ρ` : masse volumique
- `A` : aire de la section

La solution modale est de la forme :
```
w(x,t) = Σ φₙ(x) * qₙ(t)
```

Où `φₙ(x)` sont les déformées modales et `qₙ(t)` sont les coordonnées généralisées.

## 🎯 Exemple d'utilisation

1. **Configuration de la poutre**
   - Longueur : 1.0 m
   - Section : 50 mm × 20 mm
   - Matériau : Acier (E = 210 GPa, ρ = 7800 kg/m³)
   - Condition aux limites : Encastre-Libre

2. **Analyse modale**
   - Nombre de modes : 5
   - Visualisation des déformées modales

3. **Calcul de la FRF**
   - Position de la force : 0.25 m
   - Position de mesure : 0.5 m
   - Plage de fréquences : 0-500 Hz
   - Coefficient d'amortissement : 0.01

4. **Résultats**
   - Tableau des fréquences naturelles
   - Graphique des déformées modales
   - Graphique de la FRF avec contributions modales
   - Analyse des pics de résonance

## 🔧 Personnalisation

Vous pouvez modifier les paramètres par défaut dans le code source :
- `vibrateam_app.py` : Contient toute la logique de l'application
- Les propriétés matérielles par défaut peuvent être modifiées dans la classe `PoutreVibratoire`

## 📊 Sorties

L'application génère plusieurs visualisations :
1. Tableau des fréquences naturelles
2. Graphique des déformées modales
3. Schéma de la poutre avec positions de force et mesure
4. Graphique de la FRF avec contributions modales
5. Analyse détaillée d'un mode spécifique

## 🎨 Interface Utilisateur

L'interface est organisée en plusieurs sections :
- **Barre latérale** : Paramètres de la poutre et conditions aux limites
- **Section 1** : Fréquences naturelles et déformées modales
- **Section 2** : Fonction de Réponse en Fréquence (FRF)
- **Section 3** : Analyse modale détaillée
- **Section 4** : Export des données

## 📝 Notes

- L'application utilise des approximations pour les valeurs de βₙ (paramètre modal)
- Les calculs sont basés sur la théorie des poutres d'Euler-Bernoulli
- L'amortissement est modélisé par un coefficient d'amortissement visqueux
- Les déformées modales sont normalisées pour avoir une amplitude maximale de 1

## 🔒 Limitations

- Théorie valable pour les poutres minces (rapport L/h > 10)
- Pas de prise en compte des effets de cisaillement (théorie de Timoshenko non implémentée)
- Amortissement constant pour tous les modes
- Section rectangulaire uniquement pour le calcul automatique du moment d'inertie

## 📞 Support

Pour toute question ou problème, veuillez vérifier :
1. Que toutes les dépendances sont installées (`pip install -r requirements.txt`)
2. Que vous utilisez une version compatible de Python (3.7+)
3. Les logs d'erreur dans la console lors du lancement de Streamlit

## 🏆 Contributions

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Améliorer la documentation
- Optimiser le code

## 📄 Licence

Ce projet est sous licence MIT. Vous êtes libre d'utiliser, modifier et distribuer ce code.
