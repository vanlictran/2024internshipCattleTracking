# Utiliser une image de base officielle Python
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /usr/src/app

# Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt ./

# Installer les dépendances nécessaires
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le contenu du répertoire actuel dans le répertoire de travail du conteneur
COPY . .

# Exposer le port 5000 pour le serveur Flask
EXPOSE 5000

# Spécifier la commande à exécuter pour démarrer le script Python
CMD ["python3", "./retrieve_data_from_chirpstack.py"]
