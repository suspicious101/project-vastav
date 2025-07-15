import streamlit as st
import pickle
import random
from datetime import datetime
import json
import os

# === Load trained model ===
with open("models/classifier.pkl", "rb") as f:
    clf = pickle.load(f)

# === Simulate sensor data ===
def simulate_sensor_data():
    ir = round(random.uniform(0.0, 1.0), 2)
    rf = round(random.uniform(0.0, 1.0), 2)
    em = round(random.uniform(0.0, 1.0), 2)
    vib = random.choice([0, 1])
    return [ir, rf, em, vib]

# === Predict authenticity ===
def classify(sensor_data):
    return clf.predict([sensor_data])[0]

# === Log result ===
def log_result(sensor_data, prediction):
    log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "IR": sensor_data[0],
        "RF": sensor_data[1],
        "EM": sensor_data[2],
        "Vibration": sensor_data[3],
        "Result": prediction
    }
    os.makedirs("logs", exist_ok=True)
    with open("logs/threat_log.json", "a") as f:
        f.write(json.dumps(log) + "\n")

# === Streamlit UI ===
st.set_page_config(page_title="VASTAV-AI", page_icon="💣", layout="centered")
st.title("💣 VASTAV-AI - Bomb Authenticity Classifier")
st.markdown("Place suspicious object and scan to check if it's **REAL**, **FAKE**, or **INACTIVE**.")

if st.button("🔍 Scan Object"):
    sensor_data = simulate_sensor_data()
    result = classify(sensor_data)
    log_result(sensor_data, result)

    st.subheader("🔬 Simulated Sensor Data")
    st.metric("Infrared (IR)", sensor_data[0])
    st.metric("Radio Frequency (RF)", sensor_data[1])
    st.metric("Electromagnetic Field (EM)", sensor_data[2])
    st.metric("Vibration", "Yes" if sensor_data[3] else "No")

    st.success(f"✅ Classified as: **{result.upper()}**")
    st.caption("Result logged with timestamp.")

st.markdown("---")
st.markdown("🧠 Powered by AI | Developed for DRDO Demo | 🇮🇳")