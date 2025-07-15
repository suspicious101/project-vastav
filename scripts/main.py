import pickle
import random
import json
from datetime import datetime
import os

# === Load your trained classifier ===
with open("./models/classifier.pkl", "rb") as f:
    clf = pickle.load(f)

# === Simulate sensor data ===
def simulate_sensor_data():
    # Later, real sensors can fill these values
    ir = round(random.uniform(0.0, 1.0), 2)
    rf = round(random.uniform(0.0, 1.0), 2)
    em = round(random.uniform(0.0, 1.0), 2)
    vib = random.choice([0, 1])
    return [ir, rf, em, vib]

# === Predict threat authenticity ===
def classify_bomb(sensor_data):
    prediction = clf.predict([sensor_data])[0]
    return prediction

# === Log result ===
def log_result(sensor_data, prediction):
    log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "IR": sensor_data[0],
        "RF": sensor_data[1],
        "EM": sensor_data[2],
        "Vibration": sensor_data[3],
        "classification": prediction
    }

    os.makedirs("./logs", exist_ok=True)
    with open("./logs/threat_log.json", "a") as f:
        f.write(json.dumps(log) + "\n")

# === Main interface ===
print("VASTAV-AI: Real-Fake Bomb Classifier")
while True:
    input("Place object and press Enter to simulate sensors.")
    data = simulate_sensor_data()
    result = classify_bomb(data)
    print(f"> Sensor Data: IR={data[0]} RF={data[1]} EM={data[2]} VIB={data[3]}")
    print(f"> Classified as: {result.upper()}")
    log_result(data, result)

    if input("Classify another object? (y/n): ").lower() != "y":
        break
