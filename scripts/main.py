import cv2
import random
import pickle
import json
from datetime import datetime
from ultralytics import YOLO
import os

# === Load Trained Classifier ===
with open("./models/classifier.pkl", "rb") as f:
    clf = pickle.load(f)

# === Simulate Sensor Data for a Detected Object ===
def simulate_sensor_data():
    ir = round(random.uniform(0.0, 1.0), 2)
    rf = round(random.uniform(0.0, 1.0), 2)
    em = round(random.uniform(0.0, 1.0), 2)
    vib = random.choice([0, 1])
    return [ir, rf, em, vib]

# === Log Result ===
def log_result(obj_type, sensor_data, prediction):
    log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "object_detected": obj_type,
        "IR": sensor_data[0],
        "RF": sensor_data[1],
        "EM": sensor_data[2],
        "Vibration": sensor_data[3],
        "prediction": prediction
    }

    os.makedirs("../logs", exist_ok=True)
    with open("../logs/threat_log.json", "a") as f:
        f.write(json.dumps(log) + "\n")

# === Load YOLOv8 model ===
model = YOLO("yolov8n.pt")  # You can use yolov8s.pt if you want better accuracy

# === Open webcam ===
cap = cv2.VideoCapture(0)

print("VASTAV-AI is running... Press 'q' to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO object detection
    results = model(frame)
    boxes = results[0].boxes

    for box in boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        label = model.names[cls_id]

        # Draw box and label
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # Simulate sensor data
        sensor_data = simulate_sensor_data()

        # Predict threat type
        prediction = clf.predict([sensor_data])[0]

        # Display result
        result_text = f"{prediction.upper()} THREAT"
        cv2.putText(frame, result_text, (x1, y2 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Save to log
        log_result(label, sensor_data, prediction)

    cv2.imshow("VASTAV-AI Threat Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
