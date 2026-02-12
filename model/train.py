import pandas as pd
import pickle
import os

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_excel("hackthon.xlsx")

features = ["age","height_cm","weight_kg","bmi","steps","sleep_hours"]

X = df[features]
y = df["suggestion_label"]


le = LabelEncoder()
y_encoded = le.fit_transform(y)


advice_map = dict(zip(df["suggestion_label"], df["advice_explanation"]))


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_scaled, y_encoded)


os.makedirs("model", exist_ok=True)


pickle.dump(model, open("model/model.pkl","wb"))
pickle.dump(scaler, open("model/scaler.pkl","wb"))
pickle.dump(le, open("model/label_encoder.pkl","wb"))
pickle.dump(advice_map, open("model/advice_map.pkl","wb"))

print("✅ Model files saved!")

