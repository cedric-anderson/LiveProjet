# Utiliser l'image Python de la version souhaitée comme base
FROM python:3.7-slim

# Repertoire de travail
WORKDIR /app

# Copier le script Python, le fichier requirements.txt et le modèle exporté dans l'image Docker
# COPY main.py
COPY essai_app.py /app
COPY requirements.txt /app
COPY model.joblib /app

# Installer les dépendances définies dans requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exécuter la commande qui démarre le service
CMD ["uvicorn", "essai_app:app", "--host", "0.0.0.0", "--port", "8000"]
