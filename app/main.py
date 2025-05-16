from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import xgboost as xgb

model = xgb.Booster()
model.load_model('model/model_xgboost_journalier_optimise.json')


# Création de l'API FastAPI
app = FastAPI()

# Définir le schéma d'entrée des données
class ConsumptionInput(BaseModel):
    oil_mw: float
    coal_mw: float
    gas_mw: float
    nuclear_mw: float
    wind_mw: float
    solar_mw: float
    bioenergy_mw: float
    wind_offshore_mw: float
    wind_onshore_mw: float
    exchange_uk_mw: float
    exchange_spain_mw: float
    exchange_italy_mw: float
    exchange_switzerland_mw: float
    exchange_germany_belgium_mw: float
    year: int
    month: int
    day: int
    weekday: int
    season: int

@app.post("/predict")
def predict_consumption(data: ConsumptionInput):
    # Conversion en DataFrame
    input_df = pd.DataFrame([data.dict()])

    # Prédiction
    prediction = model.predict(xgb.DMatrix(input_df))[0]


    return {"prediction_MWh": round(float(prediction), 2)}
