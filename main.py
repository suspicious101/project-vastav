import streamlit as st
import pickle
import random
import json
import os
from datetime import datetime

# === Load AI Classifier ===
with open("models/classifier.pkl", "rb") as f:
    clf = pickle.load(f)

# === Simulate Sensor Data ===
def simulate_sensor_data():
    ir = round(random.uniform(0.0, 1.0), 2)
    rf = round(random.uniform(0.0, 1.0), 2)
    em = round(random.uniform(0.0, 1.0), 2)
    vib = random.choice([0, 1])
    return [ir, rf, em, vib]

# === RF Signature Fingerprint ===
def analyze_rf_signature(rf):
    if rf > 0.75:
        return "🔴 High-risk RF signal - possible remote detonator"
    elif rf > 0.4:
        return "🟠 Medium RF activity - monitor closely"
    else:
        return "🟢 Low RF - likely safe"

# === Spoofing & Deception Detection ===
def detect_sensor_anomalies(ir, rf, em, vib):
    flags = []

    if (rf > 0.6 or em > 0.6) and ir < 0.2:
        flags.append("⚠️ Signal present without heat – possible decoy")
    if ir == 0.0 and rf == 0.0 and em == 0.0 and vib == 0:
        flags.append("⚠️ All sensors silent – possible spoofing")
    if ir > 0.9 and rf > 0.9 and em > 0.9:
        flags.append("⚠️ Sensor overload – unnatural values (possible fake signals)")

    return flags

# === Classify Object ===
def classify(sensor_data):
    return clf.predict([sensor_data])[0]

# === Log Result ===
def log_result(sensor_data, prediction, warnings):
    log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "IR": sensor_data[0],
        "RF": sensor_data[1],
        "EM": sensor_data[2],
        "Vibration": sensor_data[3],
        "Prediction": prediction,
        "Warnings": warnings
    }
    os.makedirs("logs", exist_ok=True)
    with open("logs/threat_log.json", "a") as f:
        f.write(json.dumps(log) + "\n")

# === Streamlit UI ===
st.set_page_config(page_title="VASTAV-AI", layout="centered", page_icon="💣")
st.title("PROJECT VASTAV: Bomb Authenticity & Cyber Threat Classifier")
st.markdown("Detects if suspicious object is **Real / Fake / Inactive** using simulated sensor data + cyber deception logic.")

# === Scan Button ===
if st.button("🔍 Scan Object"):
    sensor_data = simulate_sensor_data()
    ir, rf, em, vib = sensor_data
    prediction = classify(sensor_data)
    rf_result = analyze_rf_signature(rf)
    warnings = detect_sensor_anomalies(ir, rf, em, vib)

    # === Show Results ===
    st.subheader("🔬 Sensor Readings")
    col1, col2 = st.columns(2)
    col1.metric("IR (Infrared)", ir)
    col2.metric("RF (Radio Freq)", rf)
    col1.metric("EM Field", em)
    col2.metric("Vibration", "Yes" if vib else "No")

    st.subheader("🧠 Prediction")
    st.success(f"Object classified as: **{prediction.upper()}**")

    st.subheader("📡 RF Signal Analysis")
    st.info(rf_result)

    if warnings:
        st.subheader("⚠️ Cyber Deception Alerts")
        for warn in warnings:
            st.warning(warn)
    else:
        st.subheader("✅ Sensor Consistency")
        st.success("No anomalies detected.")

    log_result(sensor_data, prediction, warnings)

st.markdown("---")