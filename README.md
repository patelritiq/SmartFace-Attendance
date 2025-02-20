
# SmartFace Attendance

SmartFace Attendance is a face recognition-based attendance system that captures faces using a webcam, recognizes them, and logs attendance in CSV format.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd SmartFace Attendance
   ```

2. Install the required libraries:
   ```bash
   pip install opencv-python scikit-learn numpy pywin32
   ```

## Usage

1. To collect face data, run the `Dataset.py` script:
   ```bash
   python Dataset.py
   ```
   Enter your name when prompted. The script will collect 100 face samples.

2. To start the attendance system, run the `Attendance.py` script:
   ```bash
   python Attendance.py
   ```

3. Press 'o' to mark attendance and 'q' to quit the application.

## Dependencies

- OpenCV
- scikit-learn
- NumPy
- Pickle
- CSV
- pywin32 (for text-to-speech)

## File Structure

- `Attendance.py`: Main script for the attendance system
- `Dataset.py`: Script for collecting face samples
- `haarcascade_frontalface_default.xml`: Pre-trained model for face detection
- `bg.png`: Background image for the UI
- `data/`: Directory containing:
  - `faces_data.pkl`: Stores face data
  - `names.pkl`: Stores corresponding labels
- `Attendance/`: Directory for storing attendance CSV files

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
