import os
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image


class Form(BoxLayout):
    def __init__(self, **kwargs):
        super(Form, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.data = {}  # Dictionary to store user inputs

        # Main Content Layout
        self.content_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.content_layout)

        # Background Image
        self.bg_image = Image(source='static/fitquest_bg_logo.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.bg_image)

        # Routine Name input
        self.routine_name = TextInput(hint_text='Routine Name')
        self.add_widget(self.routine_name)

        # Routine Description input
        self.routine_description = TextInput(hint_text='Routine Description')
        self.add_widget(self.routine_description)

        # Create dropdowns
        self.dropdown1 = DropDown()
        self.dropdown2 = DropDown()
        self.dropdown3 = DropDown()

        # Load options from JSON file
        with open('exercises_names.json', 'r') as file:
            options = json.load(file)
            for option in options['exercise']:
                btn = Button(text=option, size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn, exercise_option=option: self.dropdown1.select(exercise_option))
                self.dropdown1.add_widget(btn)
                btn = Button(text=option, size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn, exercise_option=option: self.dropdown2.select(exercise_option))
                self.dropdown2.add_widget(btn)
                btn = Button(text=option, size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn, exercise_option=option: self.dropdown3.select(exercise_option))
                self.dropdown3.add_widget(btn)

        # Add widgets to the layout
        self.add_widget(Label(text='Exercise 1:'))
        self.spinner1 = Spinner(text='Select an exercise', values=options['exercise'], on_text=self.select_dropdown1)
        self.add_widget(self.spinner1)
        self.input_layout1 = self.create_input_layout()
        self.add_widget(self.input_layout1)
        self.add_widget(Label(text='Exercise 2:'))
        self.spinner2 = Spinner(text='Select an exercise', values=options['exercise'], on_text=self.select_dropdown2)
        self.add_widget(self.spinner2)
        self.input_layout2 = self.create_input_layout()
        self.add_widget(self.input_layout2)
        self.add_widget(Label(text='Exercise 3:'))
        self.spinner3 = Spinner(text='Select an exercise', values=options['exercise'], on_text=self.select_dropdown3)
        self.add_widget(self.spinner3)
        self.input_layout3 = self.create_input_layout()
        self.add_widget(self.input_layout3)

        add_button = Button(text='Add', size_hint=(1, None), height=60)
        add_button.bind(on_release=self.add_data)
        self.add_widget(add_button)

    def select_dropdown1(self, spinner, text):
        self.data['exercise1'] = self.spinner1.text

    def select_dropdown2(self, spinner, text):
        self.data['exercise2'] = self.spinner2.text

    def select_dropdown3(self, spinner, text):
        self.data['exercise3'] = self.spinner3.text

    def create_input_layout(self):
        input_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=44)
        text_input1 = TextInput(hint_text='Enter number of sets', multiline=False)
        input_layout.add_widget(text_input1)
        text_input2 = TextInput(hint_text='Enter number of counts', multiline=False)
        input_layout.add_widget(text_input2)
        return input_layout

    def add_data(self, obj):
        data = {
            'routine_name': self.routine_name.text,
            'routine_description': self.routine_description.text,
            'exercises': []
        }

        selected_exercises = [self.spinner1.text, self.spinner2.text, self.spinner3.text]

        for i, exercise_name in enumerate(selected_exercises):
            sets_input, counts_input = self.input_layout1.children if i == 0 else self.input_layout2.children if i == 1 else self.input_layout3.children
            exercise_data = {
                'name': exercise_name,
                'sets': sets_input.text,
                'counts': counts_input.text,
            }
            data['exercises'].append(exercise_data)

        routines = []

        # Check if the file exists
        if os.path.exists('routines.json'):
            with open('routines.json', 'r') as f:
                try:
                    existing_data = json.load(f)
                    if isinstance(existing_data, list):
                        routines = existing_data
                except json.JSONDecodeError:
                    # Handle an empty or invalid JSON file
                    pass

        # Append the new data to the list of routines
        routines.append(data)

        with open('routines.json', 'w') as f:
            json.dump(routines, f, indent=4)  # Use indent for line breaks

class MyApp(App):
    def build(self):
        return Form()

if __name__ == '__main__':
    MyApp().run()
