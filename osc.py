#import necessary libraries
import cv2
import mediapipe as mp
from pythonosc.udp_client import SimpleUDPClient

#create a UDP client that sends messages to input port of cvOSCcv
client = SimpleUDPClient("127.0.0.1", 7001)  

#initialize mediapipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

#create a hands object, only low confidence needed to detect and track hand
hands = mp_hands.Hands(static_image_mode=False,
                        max_num_hands=2,
                        min_detection_confidence=0.67,
                        min_tracking_confidence=0.67)

#open webcam
cap = cv2.VideoCapture(0)

#get frame width and height
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  

#get center/origin of frame 
origin_x = frame_width // 2
origin_y = frame_height // 2

while cap.isOpened():
    ret, frame = cap.read()

    #check if frame exists
    if not ret:
        break

    #convert frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #process frame and detect hands
    results = hands.process(rgb_frame)

    #draw X axis and Y axis  
    cv2.line(frame, (0, origin_y), (frame_width, origin_y), (0, 0, 255), 2)  # Horizontal X-axis (Red)
    cv2.line(frame, (origin_x, 0), (origin_x, frame_height), (0, 0, 255), 2)  # Vertical Y-axis (Red)

    #add axis labels
    cv2.putText(frame, "Cutoff Frequency", (10, origin_y - 10),  
                cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)  # Left side, above X-axis

    cv2.putText(frame, "Reverb Mix", (frame_width // 2 - 60, 30),
                cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)  # Top center

    #draw landmarks if hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            #draw all hand landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            #search for 8th index (index finger tip keypoint). array length varies after each 
            #iteration so need to loop through all
            for idx, landmark in enumerate(hand_landmarks.landmark):
                if idx == 8:
                    h, w, c = frame.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)

                    #convert cx, cy to centered coordinate system
                    centered_x = cx - origin_x  
                    centered_y = -(cy - origin_y) 

                    #convert centered coordinates to voltage range (0V to 10V)
                    cutoff_freq = float((cx / frame_width) * 10)  
                    verb_mix = float((cy / frame_height) * 10)  

                    #send signals to VCV Rack
                    client.send_message("/cut/off", cutoff_freq)
                    client.send_message("/mix/verb", verb_mix)

                    #display X, Y values near the fingertip
                    cv2.putText(frame, f"({centered_x}, {centered_y})", (cx + 10, cy - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    #8th index found, no more processing is necessary
                    break

    #show the output frame
    cv2.imshow("Hand Tracking", frame)

    #program closes if q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()