import streamlit as st
import pickle
import random
import json
import os
from datetime import datetime

# === Load Classifier ===
with open("models/classifier.pkl", "rb") as f:
    clf = pickle.load(f)

# === Sensor Simulators ===
def simulate_threat_sensors():
    ir = round(random.uniform(0.0, 1.0), 2)
    rf = round(random.uniform(0.0, 1.0), 2)
    em = round(random.uniform(0.0, 1.0), 2)
    vib = random.choice([0, 1])
    return [ir, rf, em, vib]

def simulate_environment_sensors():
    heat = round(random.uniform(0.0, 1.0), 2)
    smoke = round(random.uniform(0.0, 1.0), 2)
    em_rad = round(random.uniform(0.0, 1.0), 2)
    radiation = round(random.uniform(0.0, 1.0), 2)
    sound = round(random.uniform(0.0, 1.0), 2)
    return heat, smoke, em_rad, radiation, sound

# === Cyber Anomaly Detection ===
def detect_sensor_anomalies(ir, rf, em, vib):
    flags = []
    if (rf > 0.6 or em > 0.6) and ir < 0.2:
        flags.append("⚠️ Signals without heat - possible fake")
    if ir == 0 and rf == 0 and em == 0 and vib == 0:
        flags.append("⚠️ All sensors silent - likely spoofed object")
    if ir > 0.9 and rf > 0.9 and em > 0.9:
        flags.append("⚠️ Unnaturally high readings - spoofing suspected")
    return flags

# === RF Signature Detection ===
def analyze_rf_signature(rf):
    if rf > 0.75:
        return "🔴 High-risk RF signal - likely remote trigger"
    elif rf > 0.4:
        return "🟠 Medium RF activity - suspicious"
    return "🟢 Low RF - safe"

# === PARINAAM Score Logic ===
def calculate_parinaam_score(heat, smoke, em_rad, radiation, sound):
    weighted = (heat * 0.25 + smoke * 0.25 + em_rad * 0.2 + radiation * 0.15 + sound * 0.15)
    score = round(weighted * 100)
    if score > 80:
        level = "🔴 High"
    elif score > 40:
        level = "🟠 Medium"
    else:
        level = "🟢 Low"
    return score, level

# === Threat Prediction ===
def classify(sensor_data):
    return clf.predict([sensor_data])[0]

# === Logging ===
def log_result(threat_data, env_data, prediction, warnings, score, level):
    log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ThreatSensors": {
            "IR": threat_data[0],
            "RF": threat_data[1],
            "EM": threat_data[2],
            "Vibration": threat_data[3]
        },
        "Environment": {
            "Heat": env_data[0],
            "Smoke": env_data[1],
            "EM Radiation": env_data[2],
            "Radiation": env_data[3],
            "Sound": env_data[4],
            "ImpactScore": score,
            "ImpactLevel": level
        },
        "Prediction": prediction,
        "Warnings": warnings
    }
    os.makedirs("logs", exist_ok=True)
    with open("logs/full_log.json", "a") as f:
        f.write(json.dumps(log) + "\n")

# === Streamlit UI ===
st.set_page_config(page_title="VASTAV-AI", page_icon="💣", layout="centered")
st.title("Project Vastav: Real vs Fake objects")
st.markdown("🔍 AI-based bomb threat classification with environmental impact analysis.")

if st.button("📡 Scan Suspicious Object"):
    threat_data = simulate_threat_sensors()
    ir, rf, em, vib = threat_data
    env_data = simulate_environment_sensors()
    heat, smoke, em_rad, radiation, sound = env_data

    prediction = classify(threat_data)
    if prediction.lower() in ["fake", "inactive"]:
        env_data = [round(random.uniform(0.0, 0.2), 2) for _ in range(5)]
    else:
        env_data = simulate_environment_sensors()

    heat, smoke, em_rad, radiation, sound = env_data
    rf_result = analyze_rf_signature(rf)
    warnings = detect_sensor_anomalies(ir, rf, em, vib)
    parinaam_score, impact_level = calculate_parinaam_score(heat, smoke, em_rad, radiation, sound)

    # Display Threat Detection
    st.subheader("💡 Object Threat Analysis")
    col1, col2 = st.columns(2)
    col1.metric("IR (Heat)", ir)
    col2.metric("RF Signal", rf)
    col1.metric("EM Field", em)
    col2.metric("Vibration", "Yes" if vib else "No")
    st.success(f"🧠 Prediction: **{prediction.upper()}**")
    st.info(rf_result)

    if warnings:
        st.warning("⚠️ Sensor Anomalies Detected:")
        for w in warnings:
            st.markdown(f"- {w}")
    else:
        st.success("✅ Sensor data consistent")

    # Display Environmental Impact
    st.subheader("🌍 Environmental Impact (PARINAAM)")
    env_col1, env_col2 = st.columns(2)
    env_col1.metric("🔥 Heat Index", heat)
    env_col2.metric("💨 Smoke Level", smoke)
    env_col1.metric("📡 EM Radiation", em_rad)
    env_col2.metric("☢️ Radiation", radiation)
    env_col1.metric("🔊 Sound Level", sound)

    st.subheader("📊 PARINAAM Score")
    st.markdown(f"**Score:** {parinaam_score} / 100")
    if impact_level == "🔴 High":
        st.error(f"Impact Level: {impact_level}")
    elif impact_level == "🟠 Medium":
        st.warning(f"Impact Level: {impact_level}")
    else:
        st.success(f"Impact Level: {impact_level}")

    log_result(threat_data, env_data, prediction, warnings, parinaam_score, impact_level)

st.markdown("---")