# Dockerfile pour l'application Vibrateam
# Analyse vibratoire des poutres

# Utilisation d'une image Python officielle
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir streamlit numpy matplotlib scipy pandas

# Créer un utilisateur non-root pour la sécurité
RUN useradd -m vibrateam
USER vibrateam

# Exposer le port de Streamlit
EXPOSE 8501

# Commande par défaut pour lancer l'application
CMD ["streamlit", "run", "vibrateam_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
