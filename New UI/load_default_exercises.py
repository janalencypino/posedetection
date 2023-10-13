import json
from exercise_class import BaseExercise

_desc_json          = None
def populate_exercises():
    exer_json_file  = open('exercises_config.json', 'r')
    exer_json       = json.load(exer_json_file)
    for exercise in exer_json:
        _exer_dict  = exer_json[exercise]
        BaseExercise.add_exercise(
            exer_name   = exercise,
            img_path    = _exer_dict['img_path'],
            reps        = _exer_dict['reps'],
            sets        = _exer_dict['sets'],
        )

    desc_json_file  = open('premade_desc.json', 'r')
    desc_json       = json.load(desc_json_file)

    global _desc_json
    _desc_json      = desc_json

def default_exer_list():
    return [[BaseExercise.get_exercise("sit_ups"), BaseExercise.get_exercise("lunges"), BaseExercise.get_exercise("push_ups")],
            [BaseExercise.get_exercise("lunges"), BaseExercise.get_exercise("jumping_jacks"), BaseExercise.get_exercise("push_ups")]]

def default_exer_desc():
    global _desc_json
    return _desc_json