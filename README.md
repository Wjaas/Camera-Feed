# Live Camera Stream with Face Detection

This project is a Flask-based web application that streams live video from a Raspberry Pi camera module while detecting faces in real time. The face detection is implemented using OpenCV's Haar cascade classifier.

## Features
- Streams live video from a Raspberry Pi camera.
- Detects faces and draws green rectangles around them.
- Provides a web-based interface to view the live stream.

## Requirements

Ensure you have the following installed on your Raspberry Pi:

- Python 3
- Flask
- OpenCV (`opencv-python`)
- NumPy
- PiCamera2 library

## Installation

### Update your system
```bash
sudo apt update && sudo apt upgrade -y
```

### Install required dependencies
```bash
sudo apt install python3-opencv python3-flask python3-picamera2
```

### Download the Haar cascade file
```bash
wget https://github.com/opencv/opencv/raw/master/data/haarcascades/haarcascade_frontalface_default.xml
```
Place the file in the same directory as `camera.py`.

### Clone or download this repository
```bash
git clone https://github.com/yourusername/face-detection-stream.git
cd face-detection-stream
```

## Running the Application

Run the following command:
```bash
python camera.py
```

The server will start, and you can access the stream via:
```
http://<your-device-ip>:8080
```

## How It Works

1. The `camera.py` script initializes the Raspberry Pi camera.
2. It captures frames continuously and detects faces using OpenCV's Haar cascade classifier.
3. The detected faces are highlighted with green rectangles.
4. The Flask server serves the live video stream through a web interface.

## Troubleshooting

### Face detection not working?
- Ensure the `haarcascade_frontalface_default.xml` file is in the same directory as `camera.py`.
- Check that OpenCV is installed correctly by running:
  ```bash
  python -c "import cv2; print(cv2.__version__)"
  ```

### Cannot access the stream?
- Make sure your Raspberry Pi is connected to the same network as your viewing device.
- Check the Flask server logs for errors.

## License
This project is open-source and available under the MIT License.

