
# Utiliser une image Python officielle
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de requirements d'abord (pour mieux utiliser le cache Docker)
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application
COPY . .

# Exposer le port
EXPOSE 5000

# Commande pour lancer l'application
# CMD ["python", "src/app.py"]
# Utiliser Gunicorn qui est plus robuste
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app:app"]