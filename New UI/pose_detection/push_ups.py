import cv2
import mediapipe as mp
import numpy as np
from pose_detection.calculate_angle import *
from pose_detection.return_code import ReturnCode

mp_drawing  = mp.solutions.drawing_utils
mp_pose     = mp.solutions.pose

# Curl counter variables
counter = 0 
stage = None
ave = 0
inside = 161

def check(image) -> int:
    ret_code    = ReturnCode.FAILURE
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks   = results.pose_landmarks.landmark
            
            # Get coordinates
            shoulder    = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow       = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            wrist       = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            hip         = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            knee        = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            ankle       = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            
            # Calculate angle
            angle       = calculate_angle(shoulder, elbow, wrist)
            
            angle2      = calculate_angle(hip, knee, ankle)

            # Visualize angle
            cv2.putText(image, str(angle2), 
                        tuple(np.multiply(hip, [640, 480]).astype(int)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                    )
            
            # print(angle)
            
            # push-up counter logic
            if angle <= 70:
                stage = "down"      
            elif stage =='down' and angle >= 160:
                stage       = "up"
                if angle2 < 160 and angle2 < 180:
                    stage   = "wrong"
                else: 
                    ret_code    = ReturnCode.FAILURE    
            #    print(counter)
            if stage == 'up' and angle < 160:
                ave += inside
                inside  = 161
                stage   = "down"
        except:
            pass

    return ret_code    