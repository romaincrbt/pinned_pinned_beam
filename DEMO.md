# 🎬 Démonstration Rapide de Vibrateam

## 🚀 Démarrage en 3 Étapes

### Étape 1 : Installer les dépendances
```bash
pip install streamlit numpy matplotlib scipy pandas
```

### Étape 2 : Lancer l'application
```bash
streamlit run vibrateam_app.py
```

### Étape 3 : Ouvrir dans le navigateur
Votre navigateur s'ouvrira automatiquement à l'adresse : **http://localhost:8501**

---

## 📽️ Scénario de Démonstration

### 🎯 Objectif
Analyser une poutre en acier encastrée à une extrémité (console) et calculer sa réponse vibratoire.

### 📝 Configuration

#### 1. Propriétés de la Poutre (Barre latérale)
- **Longueur** : 1.0 m
- **Largeur** : 0.05 m (50 mm)
- **Hauteur** : 0.02 m (20 mm)
- **Module de Young** : 210e9 Pa (acier)
- **Masse volumique** : 7800 kg/m³ (acier)

#### 2. Conditions aux Limites
- Sélectionner : **Encastre-Libre** 🔒🚀
- Description : Poutre encastrée à une extrémité, libre à l'autre (console)

#### 3. Approximation Modale
- **Nombre de modes** : 5
- **Coefficient d'amortissement** : 0.01 (1%)

---

## 📊 Résultats Attendus

### Section 1 : Fréquences Naturelles

**Tableau des fréquences :**
| Mode | Fréquence (Hz) |
|------|----------------|
| Mode 1 | 18.48 Hz |
| Mode 2 | 115.85 Hz |
| Mode 3 | 324.87 Hz |
| Mode 4 | 635.01 Hz |
| Mode 5 | 1047.28 Hz |

**Graphique des déformées modales :**
- Mode 1 : Courbe avec un maximum à l'extrémité libre
- Mode 2 : Courbe avec un nœud intermédiaire
- Mode 3 : Courbe avec deux nœuds
- etc.

### Section 2 : Fonction de Réponse en Fréquence

**Configuration :**
- Position de la force : 0.2 m (20% de la longueur)
- Position de mesure : 0.8 m (80% de la longueur)
- Plage de fréquences : 0-500 Hz

**Graphique FRF :**
- **Pics aux fréquences naturelles** : 18.48 Hz, 115.85 Hz, 324.87 Hz
- **FRF globale** : Courbe noire en trait plein
- **Contributions modales** : Courbes colorées en pointillés
- **Marqueurs verticaux** : Fréquences naturelles

**Analyse des pics :**
| Fréquence (Hz) | Amplitude (dB) | Mode associé | Écart (Hz) |
|----------------|----------------|--------------|-----------|
| 18.48 | 45.2 | Mode 1 | 0.00 |
| 115.85 | 52.1 | Mode 2 | 0.00 |
| 324.87 | 48.7 | Mode 3 | 0.00 |

### Section 3 : Analyse Modale Détaillée

**Sélection du Mode 1 :**
- **Fréquence** : 18.48 Hz
- **Nœuds** : x = 0.0 m (encastré)
- **Ventres** : x = 1.0 m (libre) - amplitude maximale

**Graphique :**
- Déformée modale avec marqueurs pour les nœuds (⚫) et ventres (▲)
- Conditions aux limites indiquées (🔒 à x=0, 🚀 à x=1)

---

## 🔍 Interprétation des Résultats

### Déformées Modales
- **Mode 1** : Vibration fondamentale - la poutre oscille comme un cantilever
- **Mode 2** : Deuxième mode - apparaît un nœud intermédiaire
- **Mode 3** : Troisième mode - deux nœuds intermédiaires
- Plus le mode est élevé, plus la fréquence est haute et plus la déformée est complexe

### FRF (Fonction de Réponse en Fréquence)
- **Pics** : Correspondent aux fréquences naturelles de la poutre
- **Amplitude** : Indique combien la poutre vibre à chaque fréquence
- **Contributions modales** : Montre quelle partie de la réponse vient de chaque mode
- **FRF globale** : Somme de toutes les contributions modales

### Applications Pratiques

#### 1. Conception Mécanique
- **Éviter les résonances** : Ne pas faire fonctionner la machine aux fréquences naturelles
- **Optimisation** : Modifier la géométrie pour déplacer les fréquences naturelles

#### 2. Test de Vibration
- **Identification modale** : Déterminer les fréquences naturelles expérimentales
- **Validation du modèle** : Comparer les résultats théoriques et expérimentaux

#### 3. Contrôle des Vibrations
- **Amortissement** : Ajouter de l'amortissement pour réduire les amplitudes aux résonances
- **Isolation** : Isoler la poutre des sources de vibration

---

## 🎨 Captures d'Écran (Description)

### 1. Interface Principale
```
┌─────────────────────────────────────────────────────────────────┐
│  📊 Vibrateam - Analyse Vibratoire des Poutres                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ⚙️ PARAMÈTRES (Barre latérale)                                │
│  ├─ Propriétés géométriques                                    │
│  │  ├─ Longueur: 1.0 m                                         │
│  │  ├─ Largeur: 0.05 m                                         │
│  │  └─ Hauteur: 0.02 m                                         │
│  ├─ Propriétés matérielles                                     │
│  │  ├─ Module de Young: 210e9 Pa                               │
│  │  └─ Masse volumique: 7800 kg/m³                             │
│  ├─ Conditions aux limites                                     │
│  │  └─ Encastre-Libre 🔒🚀                                       │
│  └─ Approximation modale                                       │
│     ├─ Nombre de modes: 5                                      │
│     └─ Coefficient d'amortissement: 0.01                       │
│                                                                 │
│  🔊 FRÉQUENCES NATURELLES ET DÉFORMÉES MODALES                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Mode  │ Fréquence (Hz)                                  │   │
│  │ Mode 1 │ 18.48                                         │   │
│  │ Mode 2 │ 115.85                                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  [Graphique des déformées modales]                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Graphique des Déformées Modales
```
Amplitude normalisée
  ↑
  │   Mode 5 █
  │   Mode 4 █
  │   Mode 3 █
  │   Mode 2 █
  │   Mode 1 █
  └──────────────────────▶ Position (m)
     0   0.2   0.4   0.6   0.8   1.0
     🔒─────────────────────🚀
```

### 3. Schéma de la Poutre
```
┌─────────────────────────────────────────────────────────────────┐
│  Configuration : Encastre-Libre                                │
│                                                                 │
│  🔒────────────●────────────────────────★────────────🚀       │
│  0.0          0.2                    0.8           1.0      │
│              Force @ 0.20m        Mesure @ 0.80m              │
└─────────────────────────────────────────────────────────────────┘
```

### 4. Graphique de la FRF
```
Amplitude (dB)
  ↑
  │          █
  │          █ Mode 1
  │          █ Mode 2
  │       █  █ Mode 3
  │    █  █  █
  │ █  █  █  █ FRF Globale
  └──────────────────────────────────────────────────────────────▶
     0   50  100  150  200  250  300  350  400  450  500
     Fréquence (Hz)
     │   │   │   │   │
     f1  f2  f3  f4  f5
```

---

## 💡 Astuces et Bonnes Pratiques

### 1. Choix du Nombre de Modes
- **1-3 modes** : Pour une analyse rapide ou des poutres simples
- **4-5 modes** : Pour une analyse complète de la plupart des applications
- **6-10 modes** : Pour des analyses très précises ou des poutres complexes

### 2. Sélection des Positions
- **Force** : Choisir un point accessible pour l'excitation
- **Mesure** : Choisir un point où la vibration est maximale (ventre)
- **Éviter les nœuds** : Les mesures aux nœuds donneront une amplitude nulle

### 3. Coefficient d'Amortissement
- **0.001-0.01** : Structures métalliques avec peu d'amortissement
- **0.01-0.05** : Structures avec amortissement modéré
- **0.05-0.1** : Structures avec amortissement important (caoutchouc, etc.)

### 4. Plage de Fréquences
- **0-10×f1** : Pour capturer les premiers modes
- **Autour de f1** : Pour une analyse détaillée du premier mode
- **Large plage** : Pour identifier tous les modes dans la plage

### 5. Conditions aux Limites
- **Encastre-Encastre** : Poutre très rigide, fréquences élevées
- **Encastre-Libre** : Poutre en console, fréquences plus basses
- **Libre-Libre** : Poutre flottante, inclut des modes rigides
- **Articule-Articule** : Poutre simplement supportée
- **Encastre-Articule** : Condition intermédiaire

---

## 🎯 Exercices Pratiques

### Exercice 1 : Comparaison des Conditions aux Limites
**Objectif** : Comparer les fréquences naturelles pour différentes conditions

1. Sélectionner **Encastre-Encastre**
2. Noter les fréquences des 3 premiers modes
3. Changer pour **Encastre-Libre**
4. Noter les nouvelles fréquences
5. **Observation** : Les fréquences sont plus basses pour Encastre-Libre

### Exercice 2 : Effet de la Longueur
**Objectif** : Voir comment la longueur affecte les fréquences

1. Régler la longueur à **1.0 m**
2. Noter la fréquence du premier mode
3. Doubler la longueur à **2.0 m**
4. Noter la nouvelle fréquence
5. **Observation** : La fréquence est divisée par 4 (∝ 1/L²)

### Exercice 3 : Localisation des Nœuds
**Objectif** : Trouver les positions des nœuds pour différents modes

1. Sélectionner **Articule-Articule**
2. Choisir **5 modes**
3. Pour chaque mode, noter les positions des nœuds
4. **Observation** : Les nœuds sont régulièrement espacés

### Exercice 4 : Optimisation de la Mesure
**Objectif** : Trouver la meilleure position pour mesurer la vibration

1. Sélectionner **Encastre-Libre**
2. Régler la position de mesure à **0.5 m**
3. Observer l'amplitude de la FRF
4. Déplacer la mesure vers **1.0 m** (extrémité libre)
5. **Observation** : L'amplitude est maximale à l'extrémité libre

---

## 📚 Ressources Complémentaires

### Théorie
- **Théorie d'Euler-Bernoulli** : Modèle classique pour les poutres minces
- **Vibrations mécaniques** : Rao, Inman, Thomson
- **Analyse modale** : Techniques d'identification des paramètres modaux

### Outils Complémentaires
- **MATLAB** : Fonctions `eig` pour l'analyse modale
- **ANSYS** : Simulation par éléments finis
- **Python** : Bibliothèques `scipy.signal` pour l'analyse des signaux

### Applications
- **Aérospatial** : Analyse des ailes d'avion
- **Automobile** : Conception des suspensions
- **Bâtiment** : Analyse sismique des structures
- **Mécanique** : Conception des machines tournantes

---

## 🎉 Conclusion

L'application **Vibrateam** vous permet d'explorer et de comprendre le comportement vibratoire des poutres de manière interactive et visuelle. Que vous soyez étudiant, ingénieur ou chercheur, cet outil vous aidera à :

✅ Comprendre les concepts fondamentaux des vibrations des poutres
✅ Analyser rapidement différentes configurations
✅ Visualiser les déformées modales et les FRF
✅ Exporter les données pour une analyse plus approfondie

**Bonne exploration vibratoire !** 🎊
