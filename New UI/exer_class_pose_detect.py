from exercise_class import ExerciseTemplate

import pose_detection.sit_ups
import pose_detection.push_ups
import pose_detection.lunges
import pose_detection.plank
import pose_detection.bicep_curl_up

cv_monitor_dict = {
    "sit_ups"       : pose_detection.sit_ups.check,
    "push_ups"      : pose_detection.push_ups.check,
    'lunges'        : pose_detection.lunges.check,
    'plank'         : pose_detection.plank.check,
    'bicep_curl_up' : pose_detection.bicep_curl_up.check,
}

def cv_monitor(exercise: ExerciseTemplate):
    if exercise.exer_name in cv_monitor_dict:
        exercise.monitor    = cv_monitor_dict[exercise.exer_name]
