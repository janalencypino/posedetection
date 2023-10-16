from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import json

class AdminAddExercise(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')  # Main layout
        
        # Exercise Name input
        self.exercise_name = TextInput(hint_text='Exercise Name')
        self.layout.add_widget(self.exercise_name)
        
        # Exercise Description input
        self.exercise_description = TextInput(hint_text='Exercise Description')
        self.layout.add_widget(self.exercise_description)
        
        # Body Parts input
        self.bodypart1 = TextInput(hint_text='Body Part 1')
        self.layout.add_widget(self.bodypart1)

        self.bodypart2 = TextInput(hint_text='Body Part 2')
        self.layout.add_widget(self.bodypart2)

        self.bodypart3 = TextInput(hint_text='Body Part 3')
        self.layout.add_widget(self.bodypart3)

        # Joint Angles input
        self.angle1 = TextInput(hint_text='Joint Angles 1')
        self.layout.add_widget(self.angle1)
        
        self.angle2 = TextInput(hint_text='Joint Angles 2')
        self.layout.add_widget(self.angle2)

        # Add and Cancel buttons
        button_layout = BoxLayout(orientation='horizontal')
        add_button = Button(text='Add Exercise')
        cancel_button = Button(text='Cancel')
        
        add_button.bind(on_release=self.add_exercise)
        cancel_button.bind(on_release=self.cancel_adding)
        
        button_layout.add_widget(add_button)
        button_layout.add_widget(cancel_button)
        
        self.layout.add_widget(button_layout)

        # Attach the main layout to this screen
        self.add_widget(self.layout)

        # Load existing JSON data from the file
        self.load_data()

    # ... keep all your other methods (load_data, add_exercise, cancel_adding) unchanged ...

    def load_data(self):
        try:
            # Read existing JSON data from a file (e.g., "exercises.json")
            with open("exercises.json", "r") as json_file:
                self.exercises = json.load(json_file)
        except FileNotFoundError:
            self.exercises = []  # If the file doesn't exist, initialize with an empty list

    def add_exercise(self, instance):
        exercise_name = self.exercise_name.text
        exercise_description = self.exercise_description.text
        bodypart1 = self.bodypart1.text
        bodypart2 = self.bodypart2.text
        bodypart3 = self.bodypart3.text
        angle1 = self.angle1.text
        angle2 = self.angle2.text

        # Validate input here if needed
        
        exercise_data = {
            "name": exercise_name,
            "description": exercise_description,
            "bodypart1": bodypart1,
            "bodypart2": bodypart2,
            "bodypart3": bodypart3,
            "angle1": angle1,
            "angle2": angle2
        }

        # Append the new exercise data to the existing exercises list
        self.exercises.append(exercise_data)

        # Save the updated exercise data to the JSON file
        with open("exercises.json", "w") as json_file:
            json.dump(self.exercises, json_file, indent=4)

        # Optionally, clear the input fields
        self.exercise_name.text = ''
        self.exercise_description.text = ''
        self.bodypart1.text = ''
        self.bodypart2.text = ''
        self.bodypart3.text = ''
        self.angle1.text = ''
        self.angle2.text = ''

    def cancel_adding(self, instance):
        # Close the screen or popup without saving data
        pass