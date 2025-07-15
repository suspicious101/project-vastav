import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

df = pd.read_csv("./datasets/sensor_training.csv")
X = df[["IR", "RF", "EM", "Vibration"]]
y = df["Label"]

model = RandomForestClassifier()
model.fit(X, y)

with open("./models/classifier.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved as classifier.pkl")

# Testing model on a sample input
sample = [[0.8, 0.6, 0.7, 1]]  # IR, RF, EM, Vibration
prediction = model.predict(sample)
print("Prediction for sample:", prediction[0])
