# VCV Gesture Voltage Control With All Free VCV Modules
## Description
The python script included in this repo will use mediapipe hand tracking and keypoint detection to make turning vcv rack knobs easier. Signals from the coordinates of your index finger will determine how far two knobs are turned: the reverb mix knob for plateau and cutoff frequency knob for the vcf filter.
[![Watch the video](https://img.youtube.com/vi/XEEX_NDXvdY/maxresdefault.jpg)](https://www.youtube.com/watch?v=XEEX_NDXvdY)
## Python Dependencies to Install:
- pip install python-osc
- pip install opencv-python 
- pip install mediapipe 
## Software Required:
- vcv rack
## Necessary VCV Rack Modules (only the ones that aren't included by default):
- Entrian Player: Timeline
- trowasoft cvOSCcv
- Plateau
## How to use
1. Open the included vcv rack patch after all dependencies and modules have been installed
2. Determine the output you wish to use for the audio
- Find the audio8 plugin/box on the screen
- A drag down menu to select the audio output will appear upon clicking on the middle menu of the box
![Screenshot 2025-02-07 130048](https://github.com/user-attachments/assets/3c25cdd9-5dae-4493-9e31-6722fab434ca)
3. Enable cvOSCcv connection
- Find the cvOSCcv plugin/box on the screen
- click on master config to show OSC configuration
![showConfig](https://github.com/user-attachments/assets/9be99779-b28f-4820-936a-2ecdb3a8a416)
- click on enable to allow UDP connection over local network
![enableConnection](https://github.com/user-attachments/assets/a8e10b6b-a8c9-40c5-9c22-86c0990407bf)
4. Set up web camera
- In the python script there should be a line that says:
cap = cv2.VideoCapture(0)
- When 0 is passed to cv2.VideoCapture() as shown, the first available camera will be used. If you are running this on a laptop with a built-in camera, then the program will use the feed from that camera. If you don't have a built in camera, then the feed from whatever webcam you connect to your laptop will be used. If you have a built-in camera but want to use an external webcam, then you pass 1, 2, 3, ... and so on depending on which external webcam you with to use. If you are only using one other external webcam, you likely will need to pass 1:
cv2.VideoCapture(1)
5. Run python script as is in whichever terminal you are using:
<example_shell> python osc.py
