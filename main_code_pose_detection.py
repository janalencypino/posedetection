import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Main function where the video capture and processing is handled
def main():
    cap = setup_camera()
    counter = 0 
    stage = None

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            image = process_image(frame)
            results = pose.process(image)
            image = recolor_image(image)

            try:
                landmarks = results.pose_landmarks.landmark
                shoulder, elbow, wrist = get_coordinates(landmarks)
                angle = calculate_angle(shoulder, elbow, wrist)
                display_angle(image, angle, elbow)
                print(angle)
                stage, counter = curl_counter_logic(angle, stage, counter)
            except:
                pass

            render_curl_counter(image, counter, stage)
            render_detections(image, results)
            
            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

# Run the main function
if __name__ == "__main__":
    main()