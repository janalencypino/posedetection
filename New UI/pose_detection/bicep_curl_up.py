import cv2
import mediapipe as mp
import numpy as np
from pose_detection.calculate_angle import *
from pose_detection.return_code import ReturnCode

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Curl counter variables
stage   = None
ave     = 0
inside  = 31

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
            shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            
            # Calculate angle
            angle = calculate_angle(shoulder, elbow, wrist)
            
            # print(angle)
            # Curl counter logic
            if angle > 160:
                stage = "down"
            if angle < 30 and stage =='down':
                stage = "up"
                ret_code    = ReturnCode.SUCCESS
                if inside > angle:
                    inside = angle
            if angle > 30 and stage == 'up':
                ave += inside
                inside = 31
                stage = "down"
                # print(ave)
            
            # perf = ave / counter (1-30)
            # if perf == 30 then ang rating star kay 5 stars
        except:
            pass

    return ret_code