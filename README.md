# Pinned-Pinned Beam — Analyse vibratoire d'une poutre (web app)

Web app Streamlit pour modéliser une poutre (géométrie, matériau, conditions aux
limites) et reproduire l'analyse du notebook de référence : fréquences propres,
déformées modales et Fonctions de Réponse en Fréquence (FRF), selon la théorie
d'Euler-Bernoulli.

## Installation

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sous Windows
pip install -r requirements.txt
```

## Exécution

```bash
streamlit run app.py
```

L'application s'ouvre dans le navigateur à l'adresse `http://localhost:8501`.

## Fonctionnalités

- **Matériau** : presets (aluminium, acier, titane, cuivre, laiton) ou valeurs
  personnalisées (E, rho)
- **Géométrie** : longueur L, largeur b, hauteur h de la section rectangulaire
- **Conditions aux limites** : articulée / encastrée / libre à chaque extrémité
  (articulée-articulée par défaut)
- **Analyse modale** : fréquences propres (racines de det(H(w)) = 0 par balayage
  et `brentq`) et déformées modales (vecteur propre nul de H)
- **FRF** : superposition modale avec amortissement modal, force et capteurs au
  choix, tracés amplitude (log) / phase
- **Export CSV** des fréquences propres et de la FRF

## Tests

```bash
pip install pytest
pytest test_beam.py
```

Les tests comparent les résultats aux solutions analytiques connues
(articulée-articulée : f_n = (nπ/L)² √(EJ/m_l) / 2π ; console : cos(βL)cosh(βL) = -1).
