_exercise_dict  = {}
class BaseExercise:
    def __init__(self,
            exer_name: str,
            img_path: str,
            reps: int,
            sets: int):
        
        self.exer_name  = exer_name
        self.img_path   = img_path
        self.reps       = reps
        self.sets       = sets

    def add_exercise(exer_name: str,
                    img_path: str,
                    reps: int,
                    sets: int):
        if (exer_name in _exercise_dict):
            return _exercise_dict[exer_name]

        exercise    = BaseExercise(exer_name, img_path, reps, sets)
        _exercise_dict[exer_name]   = exercise
        return exercise
    
    def get_exercise(exer_name):
        return ((exer_name in _exercise_dict) and _exercise_dict[exer_name]) or None