from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
import json
import os
import base64

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

        # Add Image Uploader
        self.file_chooser = FileChooserListView()
        self.file_chooser.multiselect = True  # Enable multiple file selection
        self.layout.add_widget(self.file_chooser)

        # Add and Cancel buttons
        button_layout = BoxLayout(orientation='horizontal')
        add_button = Button(text='Add Exercise')
        cancel_button = Button(text='Cancel')
        upload_button = Button(text='Upload Images')
        
        add_button.bind(on_release=self.add_exercise)
        cancel_button.bind(on_release=self.cancel_adding)
        upload_button.bind(on_release=self.upload_images)
        
        button_layout.add_widget(add_button)
        button_layout.add_widget(cancel_button)
        button_layout.add_widget(upload_button)

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
        
        image_info_list = []
        if self.file_chooser.selection:
            for file_path in self.file_chooser.selection:
                with open(file_path, 'rb') as img_file:
                    image_data = img_file.read()
                image_base64 = base64.b64encode(image_data).decode('utf-8')

                image_info = {
                    'filename': os.path.basename(file_path),  # Store only the file name, not the path
                    'image_data': image_base64
                }
                image_info_list.append(image_info)

        exercise_data = {
            "name": exercise_name,
            "description": exercise_description,
            "bodypart1": bodypart1,
            "bodypart2": bodypart2,
            "bodypart3": bodypart3,
            "angle1": angle1,
            "angle2": angle2,
            "images": image_info_list
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
        self.file_chooser.selection = []

    def cancel_adding(self, instance):
        # Close the screen or popup without saving data
        pass

    def upload_images(self, instance):
        if self.file_chooser.selection:
            selected_files = self.file_chooser.selection

            image_info_list = []

            # Load existing image info from the JSON file if it exists
            if os.path.exists('image_info.json'):
                with open('image_info.json', 'r') as json_file:
                    image_info_list = json.load(json_file)

            for file_path in selected_files:
                # Read each image file as binary data
                with open(file_path, 'rb') as img_file:
                    image_data = img_file.read()

                # Convert the binary image data to base64
                image_base64 = base64.b64encode(image_data).decode('utf-8')

                # Create a dictionary for each image
                image_info = {
                    'filename': file_path,
                    'image_data': image_base64
                }

                image_info_list.append(image_info)

            # Save the updated list of image info to the JSON file
            with open('image_info.json', 'w') as json_file:
                json.dump(image_info_list, json_file, indent=4)

            # Optionally, clear the selection in the file chooser
            self.file_chooser.selection = []