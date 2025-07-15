import random
import csv

# Simulate 100 samples
def generate_dataset():
    with open("./datasets/sensor_training.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["IR", "RF", "EM", "Vibration", "Label"])

        for _ in range(100):
            label = random.choice(["real", "fake", "inactive"])
            if label == "real":
                ir = round(random.uniform(0.6, 1.0), 2)
                rf = round(random.uniform(0.5, 1.0), 2)
                em = round(random.uniform(0.5, 1.0), 2)
                vib = 1
            elif label == "fake":
                ir = 0.0
                rf = 0.0
                em = 0.0
                vib = 0
            else:  # inactive
                ir = round(random.uniform(0.1, 0.3), 2)
                rf = 0.0
                em = round(random.uniform(0.1, 0.4), 2)
                vib = 0

            writer.writerow([ir, rf, em, vib, label])

generate_dataset()
print("Sensor training data generated.")