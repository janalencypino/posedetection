import cv2
import mediapipe as mp
import numpy as np
from pose_detection.calculate_angle import *
from pose_detection.return_code import ReturnCode

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Curl counter variables
stage = None

## Setup mediapipe instance
def check(image):
    ret_code    = ReturnCode.FAILURE
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        # Recolor image to RGB
        image.flags.writeable = False
        
        # Make detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            hip = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            
            # Calculate angle
            angle = calculate_angle(hip, knee, ankle)
            
            # Visualize angle
            # cv2.putText(image, str(angle), 
            #               tuple(np.multiply(hip, [640, 480]).astype(int)), 
            #               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
            #                    )
            
            #print(angle)
            # Lunge counter logic
            if angle <120:
                stage = "up"
                print(f"high_knees.check >> stage is now up")
            if stage =='up' and angle >150:
                stage="down"
                print(f"high_knees.check >> stage is now down")
                ret_code    = ReturnCode.SUCCESS
                # print(counter)
                        
        except:
            pass
        
    return ret_code