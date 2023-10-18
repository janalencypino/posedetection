from kivy_config import strict_mode

_exercise_dict  = {}
class ExerciseTemplate:
    def __init__(self,
                 exer_name: str,
                 img_path: str,
                 reps: int,
                 sets: int,
                 duration: int):
        
        self.exer_name  = exer_name
        self.img_path   = img_path
        self.reps       = reps
        self.sets       = sets
        self.duration   = duration

    def add_exercise(exer_name: str,
                    **kwargs):
        '''
        Argument list (*args) in order:
        -   img_path: str
        -   reps: int
        -   sets: int
        -   duration: int
        '''
        if (exer_name in _exercise_dict):
            return _exercise_dict[exer_name]

        exercise                    = ExerciseTemplate(exer_name, **kwargs)
        _exercise_dict[exer_name]   = exercise
        return exercise
    
    def get_exercise(exer_name: str):
        return ((exer_name in _exercise_dict) and _exercise_dict[exer_name]) or None
    
class Exercise(ExerciseTemplate):
    def __init__(self,
                 base: ExerciseTemplate):

        self._base      = base
        self.exer_name  = base.exer_name
        self.img_path   = base.img_path
        self.reps       = base.reps
        self.sets       = base.sets
        self.duration   = base.duration

    def copy(base: ExerciseTemplate):
        object =  Exercise(base)
        return object
    
    def add_exercise(exer_name: str, **kwargs):
        return None
    
    def get_exercise(exer_name: str) -> None:
        if strict_mode:
            raise RuntimeWarning("Do not use Exercise.get_exercise(). Please use ExerciseTemplate.get_exercise() only.")
        
        return None

def exercise_dict() -> dict:
    return _exercise_dict