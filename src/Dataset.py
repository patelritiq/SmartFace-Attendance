import cv2
import pickle
import numpy as np
import os

video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier("../models/haarcascade_frontalface_default.xml")

faces_data = []

i = 0

name = input("Enter Your Name: ")

# Collect 100 face samples
TOTAL_SAMPLES = 100
SAMPLE_INTERVAL = 5  # Take every 5th frame to avoid duplicates

while len(faces_data) < TOTAL_SAMPLES:
    ret, frame = video.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for x, y, w, h in faces:
        if i % SAMPLE_INTERVAL == 0 and len(faces_data) < TOTAL_SAMPLES:
            crop_img = frame[y : y + h, x : x + w, :]
            gray_crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
            resized_img = cv2.resize(gray_crop_img, (75, 50))
            faces_data.append(resized_img)

            # Display progress
            cv2.putText(
                frame,
                f"Collected: {len(faces_data)}/{TOTAL_SAMPLES}",
                (50, 50),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (50, 50, 255),
                1,
            )
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)

        i += 1

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv2.destroyAllWindows()

faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape(-1, 3750)


# Ensure data directory exists
os.makedirs("../data", exist_ok=True)

# Clear existing data files to start fresh
if os.path.exists("../data/names.pkl"):
    os.remove("../data/names.pkl")
if os.path.exists("../data/faces_data.pkl"):
    os.remove("../data/faces_data.pkl")

# Create labels matching the number of collected faces
names = [name] * len(faces_data)
with open("../data/names.pkl", "wb") as f:
    pickle.dump(names, f)

# Save face data
with open("../data/faces_data.pkl", "wb") as f:
    pickle.dump(faces_data, f)

print(f"\n✓ Dataset created successfully!")
print(f"✓ Collected {len(faces_data)} samples for {name}")
print(f"✓ Data saved to ../data/ directory")
