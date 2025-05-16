# Base légère avec apt pour compiler numpy/pandas sans GPU overhead
FROM python:3.9-slim

# Installer build-essential pour compiler les libs (obligatoire pour XGBoost CPU-only)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Dossier de travail
WORKDIR /app

# Copier d’abord les requirements pour optimiser le cache Docker
COPY ./app/requirements.txt /app/requirements.txt

# Installer les dépendances en amont
RUN pip install --no-cache-dir -r requirements.txt

# Copier ensuite le code de l’app et le modèle
COPY ./app /app
COPY ./model /app/model

# Exposer le port 8000
EXPOSE 8000

# Lancer l’API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
