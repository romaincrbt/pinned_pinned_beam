#!/bin/bash

# Script de lancement de l'application Vibrateam

echo "🚀 Lancement de Vibrateam - Analyse Vibratoire des Poutres"
echo "=========================================================="
echo ""

# Vérifier que Streamlit est installé
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit n'est pas installé."
    echo "Installation en cours..."
    pip install streamlit numpy matplotlib scipy pandas -q
fi

# Vérifier que le fichier principal existe
if [ ! -f "vibrateam_app.py" ]; then
    echo "❌ Le fichier vibrateam_app.py est introuvable."
    echo "Veuillez vous assurer d'être dans le bon répertoire."
    exit 1
fi

# Lancer l'application
echo "✅ Démarrage de l'application..."
echo ""
echo "L'application sera disponible à l'adresse : http://localhost:8501"
echo ""
streamlit run vibrateam_app.py --server.port 8501 --server.address 0.0.0.0
