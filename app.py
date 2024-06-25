from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import librosa
import pickle
import numpy as np
import os
import pandas as pd

feature_names = [
    'Amplitude', 'ZCR', 'RMSE', 'SC', 'SB', 'MFCC1', 'MFCC2', 'MFCC3', 'MFCC4', 
    'MFCC5', 'MFCC6', 'MFCC7', 'MFCC8', 'MFCC9', 'MFCC10', 'MFCC11', 'MFCC12', 'MFCC13'
]

# Obtiene la dirección del script
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'modelo_entrenado_rf.pkl')

# Cargar el modelo pre-entrenado
try:
    with open(model_path, 'rb') as f:
        modelo = pickle.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"Model file not found at path: {model_path}")
except Exception as e:
    raise Exception(f"Error loading model: {e}")

app = FastAPI()

# Habilitar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def process_audio(audio_file):
    try:
        audio, sample_rate = librosa.load(audio_file, sr=None)
        # Calcular las características
        amplitude = np.max(np.abs(audio))
        zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(audio))
        rmse = np.mean(librosa.feature.rms(y=audio))
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio, sr=sample_rate))
        mel_frequency_cepstral_coefficients = np.mean(librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=13), axis=1)
        spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=audio, sr=sample_rate))
        return [
            amplitude,
            zero_crossing_rate,
            rmse,
            spectral_centroid,
            spectral_bandwidth,
            *mel_frequency_cepstral_coefficients
        ]
    except Exception as e:
        print(f"Error processing audio: {e}")
        raise HTTPException(status_code=500, detail=f"Error procesando el audio: {e}")

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        # Ensure the temp directory exists
        os.makedirs("temp", exist_ok=True)
        
        file_location = os.path.join("temp", file.filename)
        with open(file_location, "wb+") as file_object:
            file_object.write(await file.read())

        embeddings = process_audio(file_location)
        df = pd.DataFrame([embeddings], columns=feature_names)
        prediction = modelo.predict(df)
        os.remove(file_location)
        return { prediction.tolist()[0]}
    except Exception as e:
        # Debug: print the error
        print(f"Error making prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Error making prediction: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

#uvicorn app:app --reload
