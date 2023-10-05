from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        user_btn = Button(text="User", size_hint=(None, None), width=200, height=50)
        user_btn.bind(on_press=self.user_btn_pressed)
        layout.add_widget(user_btn)
        
        admin_btn = Button(text="Admin", size_hint=(None, None), width=200, height=50)
        admin_btn.bind(on_press=self.admin_btn_pressed)
        layout.add_widget(admin_btn)
        
        self.add_widget(layout)

    def user_btn_pressed(self, instance):
        # Logic for when the User button is pressed
        pass

    def admin_btn_pressed(self, instance):
        # Switch to the Admin Dashboard screen
        self.manager.current = 'admin_dashboard'

class AdminDashboard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Admin Dashboard"))

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main_screen'))
        sm.add_widget(AdminDashboard(name='admin_dashboard'))
        return sm

if __name__ == "__main__":
    MyApp().run()
