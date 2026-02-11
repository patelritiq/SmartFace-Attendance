# SmartFace Attendance - Quick Start Guide 🚀

## Installation (5 minutes) 📦 

1. **Clone & Navigate:**
   ```bash
   git clone https://github.com/patelritiq/SmartFace-Attendance.git
   cd SmartFace-Attendance
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Setup:**
   ```bash
   python -c "import cv2, sklearn, numpy; print('✓ Ready to go!')"
   ```

---

## Register Users (1 minute per user) 👤 

```bash
cd src
python Dataset.py
```

- Enter name when prompted
- Face the webcam
- Wait for 100 samples to be collected
- Repeat for each user

---

## Mark Attendance (Real-time) ✅ 

```bash
cd src
python Attendance.py
```

- Stand in front of camera
- Wait for name to appear
- **Ensure only ONE person in frame**
- Press **'o'** to mark attendance
- Press **'q'** to quit

---

## Important Notes ⚠️ 

### Multi-Face Validation
- ✅ **One face**: Attendance can be marked
- ❌ **Multiple faces**: "Multiple faces detected!" - attendance disabled
- ❌ **No face**: "No face detected" - attendance disabled

### Attendance Records
- Location: `Attendance/Attendance_DD-MM-YYYY.csv`
- Format: NAME, TIME
- One file per day

---

## Configuration & Customization 🔧 

### Adjust Sample Collection
**File**: `src/Dataset.py`
```python
TOTAL_SAMPLES = 100          # Increase for more robust dataset
SAMPLE_INTERVAL = 5          # Decrease for faster collection
```

### Tune KNN Parameters
**File**: `src/Attendance.py`
```python
knn = KNeighborsClassifier(n_neighbors=5)  # Try 3, 5, or 7
```
- K=3: More sensitive, may be less robust
- K=5: Balanced (recommended)
- K=7: More robust, slightly slower

### Customize UI
**Background Image**: Replace `assets/bg.png`
- Recommended size: 1280×720 pixels
- Ensure video feed area (640×480) fits

**Window Size**: Modify in `src/Attendance.py`
```python
cv2.resizeWindow("Frame", 800, 600)  # Adjust dimensions
```

---

## Troubleshooting 🐛 

| Issue | Solution |
|-------|----------|
| **Webcam not working** | Try changing camera index: `cv2.VideoCapture(1)` or `(2)` |
| **Face not detected** | Improve lighting, face camera directly, remove obstructions |
| **Wrong person identified** | Collect more samples, ensure diverse angles, better lighting |
| **Multiple faces warning** | Ensure only one person in frame (this is intentional!) |
| **Module not found** | Run: `pip install opencv-python scikit-learn numpy pywin32` |
| **Text-to-speech not working (non-Windows)** | Comment out `speak()` in `src/Attendance.py`, use `print()` instead |

### Detailed Solutions

**Webcam Issues:**
```python
# In Dataset.py or Attendance.py, try different camera indices:
video = cv2.VideoCapture(0)  # Try 0, 1, 2, etc.
```

**Face Detection Issues:**
- Ensure `models/haarcascade_frontalface_default.xml` exists
- Check lighting (avoid total darkness)
- Face camera directly
- Remove glasses/masks if causing issues

**Recognition Issues:**
- Increase `TOTAL_SAMPLES` to 150 or 200
- Collect samples in various lighting conditions
- Ensure diverse facial angles during dataset creation

**Non-Windows Text-to-Speech:**
```python
# In src/Attendance.py, replace speak() calls:
# speak("Attendance Taken..")  # Comment this
print("✓ Attendance Taken!")   # Use this instead
```

---

## Performance Metrics 📊 

### System Requirements
- **CPU**: Intel i3 or equivalent
- **RAM**: 4GB minimum, 8GB recommended
- **Webcam**: 720p or higher
- **Storage**: ~10MB per 100 users

### Performance Benchmarks
- **Face Detection**: ~30 FPS
- **Recognition Time**: <100ms per face
- **Dataset Creation**: 30-60 seconds per user
- **Accuracy**: High under normal lighting

---

## Project Structure 📁 

```
SmartFace-Attendance/
├── src/              # Python scripts
│   ├── Dataset.py    # User registration
│   └── Attendance.py # Attendance marking
├── models/           # Face detection model
├── assets/           # UI resources (bg.png)
├── data/             # Training data (auto-created)
└── Attendance/       # CSV logs (auto-created)
```

---

## Key Features 🎯 

✅ 100+ samples per user for accuracy  
✅ Real-time face recognition  
✅ Multi-face validation  
✅ CSV-based logging  
✅ Audio feedback  
✅ Cost-effective solution  

---

## Pro Tips 💡 

1. **Better Recognition**: Collect samples in various lighting conditions
2. **Faster Collection**: Reduce `SAMPLE_INTERVAL` to 3 (less diverse samples)
3. **More Robust**: Increase `TOTAL_SAMPLES` to 150-200
4. **Custom Background**: Replace `assets/bg.png` with your logo/branding
5. **Batch Registration**: Run `Dataset.py` multiple times for all users before starting attendance

---

**Need more details?** Check the full [README.md](README.md)

*Happy attendance tracking!* 👤✨
