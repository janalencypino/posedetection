# Import the necessary Kivy modules
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import json

class ExerciseApp(App):
    def build(self):
        self.title = 'Exercise App'
        self.root = ExerciseScreen()
        return self.root

class ExerciseScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Exercise Name input
        self.exercise_name = TextInput(hint_text='Exercise Name')
        self.add_widget(self.exercise_name)
        
        # Exercise Description input
        self.exercise_description = TextInput(hint_text='Exercise Description')
        self.add_widget(self.exercise_description)
        
         # Body Parts input
        self.bodypart1 = TextInput(hint_text='Body Part 1')
        self.add_widget(self.bodypart1)

        self.bodypart2 = TextInput(hint_text='Body Part 2')
        self.add_widget(self.bodypart2)

        self.bodypart3 = TextInput(hint_text='Body Part 3')
        self.add_widget(self.bodypart3)

        # Joint Angles input
        self.angle1 = TextInput(hint_text='Joint Angles 1')
        self.add_widget(self.angle1)
        
        self.angle2 = TextInput(hint_text='Joint Angles 2')
        self.add_widget(self.angle2)

        # Add and Cancel buttons
        button_layout = BoxLayout(orientation='horizontal')
        add_button = Button(text='Add Exercise')
        cancel_button = Button(text='Cancel')
        
        add_button.bind(on_release=self.add_exercise)
        cancel_button.bind(on_release=self.cancel_adding)
        
        button_layout.add_widget(add_button)
        button_layout.add_widget(cancel_button)
        
        self.add_widget(button_layout)
    
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
        
        # Save exercise data to a JSON file
        with open("exercises.json", "a") as json_file:
            json.dump(exercise_data, json_file)
        
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

if __name__ == '__main__':
    ExerciseApp().run()
