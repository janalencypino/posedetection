import json
import exer_class_pose_detect
from exercise_class import ExerciseTemplate

_desc_json          = None
def populate_exercises():
    exer_json_file  = open('exercises_config.json', 'r')
    exer_json       = json.load(exer_json_file)
    for exercise in exer_json:
        _exer_dict  = exer_json[exercise]
        _exer_obj   = ExerciseTemplate.add_exercise(
            exer_name   = exercise,
            img_path    = _exer_dict['img_path'],
            reps        = _exer_dict['reps'],
            sets        = _exer_dict['sets'],
            duration    = _exer_dict['duration'],
        )
        exer_class_pose_detect.cv_monitor(_exer_obj)

    desc_json_file  = open('premade_desc.json', 'r')
    desc_json       = json.load(desc_json_file)

    global _desc_json
    _desc_json      = desc_json

def default_exer_list():
    return [[ExerciseTemplate.get_exercise("sit_ups"),
             ExerciseTemplate.get_exercise("lunges"),
             ExerciseTemplate.get_exercise("push_ups")],

            [ExerciseTemplate.get_exercise("lunges"),
             ExerciseTemplate.get_exercise("jumping_jacks"),
             ExerciseTemplate.get_exercise("push_ups")]]

def default_exer_desc():
    global _desc_json
    return _desc_json