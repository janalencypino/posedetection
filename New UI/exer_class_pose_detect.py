from exercise_class import ExerciseTemplate

import pose_detection.sit_ups
import pose_detection.push_ups
import pose_detection.lunges
import pose_detection.high_knees
import pose_detection.bicep_curl_up
import pose_detection.squats
import pose_detection.glute_bridge

cv_monitor_dict = {
    "sit_ups"       : pose_detection.sit_ups.check,
    "push_ups"      : pose_detection.push_ups.check,
    'lunges'        : pose_detection.lunges.check,
    'high_knees'    : pose_detection.high_knees.check,
    'bicep_curl_up' : pose_detection.bicep_curl_up.check,
}

def cv_monitor(exercise: ExerciseTemplate):
    if exercise.exer_name in cv_monitor_dict:
        exercise.monitor    = cv_monitor_dict[exercise.exer_name]
