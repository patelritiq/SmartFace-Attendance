from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime


from win32com.client import Dispatch


def speak(str1):
    speak = Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)


video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier("../models/haarcascade_frontalface_default.xml")

with open("../data/names.pkl", "rb") as w:
    LABELS = pickle.load(w)
with open("../data/faces_data.pkl", "rb") as f:
    FACES = pickle.load(f)

print("Shape of Faces matrix --> ", FACES.shape)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

imgBackground = cv2.imread("../assets/bg.png")

# Ensure Attendance directory exists
os.makedirs("../Attendance", exist_ok=True)

COL_NAMES = ["NAME", "TIME"]

# Variable to track if attendance can be marked
can_mark_attendance = False
detected_name = ""

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    
    # Check number of faces detected
    num_faces = len(faces)
    
    # Multi-face validation
    if num_faces == 0:
        can_mark_attendance = False
        cv2.putText(
            frame,
            "No face detected",
            (50, 50),
            cv2.FONT_HERSHEY_COMPLEX,
            0.8,
            (0, 165, 255),
            2,
        )
    elif num_faces > 1:
        can_mark_attendance = False
        cv2.putText(
            frame,
            "Multiple faces detected! Only one person allowed.",
            (50, 50),
            cv2.FONT_HERSHEY_COMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )
        cv2.putText(
            frame,
            "Attendance marking disabled.",
            (50, 90),
            cv2.FONT_HERSHEY_COMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )
    else:
        can_mark_attendance = True
        cv2.putText(
            frame,
            "Press 'o' to mark attendance",
            (50, 50),
            cv2.FONT_HERSHEY_COMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )
    
    for x, y, w, h in faces:
        crop_img = frame[y : y + h, x : x + w, :]
        gray_crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        resized_img = cv2.resize(gray_crop_img, (75, 50)).flatten().reshape(1, -1)

        output = knn.predict(resized_img)
        detected_name = str(output[0])
        
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        exist = os.path.isfile("../Attendance/Attendance_" + date + ".csv")
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
        cv2.putText(
            frame,
            detected_name,
            (x, y - 15),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (255, 255, 255),
            1,
        )
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)
        attendance = [detected_name, str(timestamp)]
        
    # Resize the frame to fit in the background image
    resized_frame = cv2.resize(frame, (640, 480))
    imgBackground[162 : 162 + 480, 55 : 55 + 640] = resized_frame

    # Create a smaller window
    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Frame", 800, 600)  # Set window size to 800x600
    cv2.imshow("Frame", imgBackground)

    k = cv2.waitKey(1)
    if k == ord("o"):
        if not can_mark_attendance:
            # Show error message if multiple faces or no face detected
            if num_faces > 1:
                speak("Multiple faces detected. Please ensure only one person is present.")
                print("❌ Attendance NOT marked: Multiple faces detected!")
            elif num_faces == 0:
                speak("No face detected. Please position yourself in front of the camera.")
                print("❌ Attendance NOT marked: No face detected!")
            time.sleep(2)
        else:
            # Mark attendance only if exactly one face is detected
            speak("Attendance Taken..")
            time.sleep(2)
            if exist:
                with open("../Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(attendance)
                csvfile.close()
            else:
                with open("../Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(COL_NAMES)
                    writer.writerow(attendance)
                csvfile.close()
            print(f"✓ Attendance marked for {detected_name} at {timestamp}")
            
    if k == ord("q"):
        break
        
video.release()
cv2.destroyAllWindows()
