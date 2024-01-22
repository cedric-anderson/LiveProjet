# Utiliser une image python légère
FROM python:3.7-slim

# Créer un repertoir et le definir comme reperoire de travail
RUN  mkdir /src
WORKDIR  /src

# Installer jupyter
RUN pip install jupyter

# Definissez la commande pour démarrer le server jupyter
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--no-browser"]

# Ajout de requirements.txt
COPY requirements.txt .

# Installation de bibliotheques dans requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
