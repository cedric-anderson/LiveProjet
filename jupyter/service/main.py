from fastapi import FastAPI, HTTPException
from typing import List, Optional
from joblib import load
import numpy as np
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import StreamingResponse 
import time
import io


# Chargement du modèle exporté
model = load("model.joblib")

# Création de l'application FastAPI
app = FastAPI()


# Création d'une métrique de compteur pour les prédictions
predictions_counter = Counter("predictions_total", "Total number of predictions")

# Création d'une métrique d'histogramme pour la latence des prédictions
predictions_latency_histogram = Histogram("predictions_latency_seconds", "Latency of predictions")



# Premier point de terminaison pour gérer les prédictions
@app.post("/prediction")
def predict(features: List[float], score: Optional[bool] = False):
    try:
        # Enregistrement de la prédiction dans la métrique de compteur
        predictions_counter.inc()

        # Enregistrement du début du calcul pour calculer la latence
        start_time = time.time() 


        # Vérification de la longueur des caractéristiques
        if len(features) != 2:
            raise HTTPException(status_code=400, detail="Le vecteur de caractéristiques doit avoir une longueur de 2.")

        # Prédiction du modèle
        prediction = model.predict([features])[0]

        # Si le paramètre score est True, retourne également le score d'anomalie
        if score:
            anomaly_score = float(model.decision_function([features])[0])
            return {"prediction": prediction, "anomaly_score": anomaly_score}
        else:
            return {"prediction": prediction} 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally: 
        # Calcul de la latence et enregistrement dans la métrique d'histogramme
        latency = time.time() - start_time
        predictions_latency_histogram.observe(latency)



# Deuxième point de terminaison pour fournir les hyperparamètres du modèle
@app.get("/model_information")
def get_model_information():
    try:
        model_params = model.get_params()
        return model_params
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Point de terminaison pour exposer les métriques Prometheus
@app.get("/metrics")
def get_metrics():
    return StreamingResponse(io.BytesIO(generate_latest()), media_type=CONTENT_TYPE_LATEST)
