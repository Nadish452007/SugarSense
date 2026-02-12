import pickle
import numpy as np
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

model_path = BASE_DIR / "model" / "model.pkl"
scaler_path = BASE_DIR / "model" / "scaler.pkl"
le_path = BASE_DIR / "model" / "label_encoder.pkl"
advice_path = BASE_DIR / "model" / "advice_map.pkl"


model = pickle.load(open(model_path, "rb"))
scaler = pickle.load(open(scaler_path, "rb"))
le = pickle.load(open(le_path, "rb"))
advice_map = pickle.load(open(advice_path, "rb"))

def predict_health(age, height, weight, bmi, steps, sleep):

    user_data = np.array([[age, height, weight, bmi, steps, sleep]])

    user_scaled = scaler.transform(user_data)

    pred = model.predict(user_scaled)

    label = le.inverse_transform(pred)[0]

    explanation = advice_map[label]

    return label, explanation

