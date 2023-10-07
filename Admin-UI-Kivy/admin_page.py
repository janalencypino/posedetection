from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main layout
        layout = FloatLayout(size=(300, 300))
        
        # Background
        bg = Image(source='static/fitquest_bg.png', allow_stretch=True, keep_ratio=False)
        layout.add_widget(bg)
        
        # Logo
        logo = Image(source='static/logo-no-background.png', pos_hint={'x': 0.5, 'y': 0.5}, size_hint=(0.3, 0.3), allow_stretch=True, keep_ratio=True)
        layout.add_widget(logo)
        
        # Buttons layout
        buttons = BoxLayout(orientation='vertical', spacing=10, size_hint=(None, None), size=(200, 100), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        user_btn = Button(text="User", height=50)
        user_btn.bind(on_press=self.user_btn_pressed)
        buttons.add_widget(user_btn)
        
        admin_btn = Button(text="Admin", height=50)
        admin_btn.bind(on_press=self.admin_btn_pressed)
        buttons.add_widget(admin_btn)
        
        layout.add_widget(buttons)
        
        # Add layout to screen
        self.add_widget(layout)

    def user_btn_pressed(self, instance):
        pass

    def admin_btn_pressed(self, instance):
        self.manager.current = 'admin_dashboard'

class AdminDashboard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Image(source='static/fitquest_bg_logo.png', allow_stretch=True, keep_ratio=False))
        self.add_widget(Label(text="Admin Dashboard"))

'''
class JSONEditorApp(App):
    def build(self):
        self.title = 'JSON Editor'
        self.root = JSONEditor()
        return self.root

class JSONEditor(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Load JSON data from the file
        self.load_data()

        # Text input for editing JSON data
        self.json_input = TextInput(text=json.dumps(self.data, indent=4))
        self.add_widget(self.json_input)

        # Buttons for editing and saving
        edit_button = Button(text='Edit Data')
        save_button = Button(text='Save Data')

        edit_button.bind(on_release=self.edit_data)
        save_button.bind(on_release=self.save_data)

        self.add_widget(edit_button)
        self.add_widget(save_button)

    def load_data(self):
        try:
            # Read JSON data from a file (assuming the file is named "data.json")
            with open("exercises.json", "r") as json_file:
                self.data = json.load(json_file)
        except FileNotFoundError:
            self.data = {}  # If the file doesn't exist, initialize with an empty dictionary

    def edit_data(self, instance):
        # Parse the JSON data from the input field
        try:
            edited_data = json.loads(self.json_input.text)
            self.data = edited_data  # Update the data with the edited content
        except json.JSONDecodeError:
            pass  # Handle invalid JSON input here if needed

    def save_data(self, instance):
        # Save the updated data back to the JSON file
        with open("exercises.json", "w") as json_file:
            json.dump(self.data, json_file, indent=4)  # Optionally, use 'indent' for pretty formatting
'''

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main_screen'))
        sm.add_widget(AdminDashboard(name='admin_dashboard'))
        
        # Load and play background music
        self.sound = SoundLoader.load('audio/bss_fighting.mp3')  # Replace with your audio file
        if self.sound:
            self.sound.loop = True  # Enable looping
            self.sound.volume = 0.5  # Set volume to 50%
            self.sound.play()
        else:
            print("Unable to load the sound")
            
        return sm

    def on_stop(self):
        # Stop the sound when the app is closed
        if self.sound:
            self.sound.stop()

if __name__ == "__main__":
    MyApp().run()
