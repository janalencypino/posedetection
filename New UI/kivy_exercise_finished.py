from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy_exercise_cooldown import CooldownPage
from exercise_class import Exercise
from functools import partial

import kivy_homepage as home
import kivy_config as cfg

def page_recipe(manager: ScreenManager):
    app_layout          = CooldownPage()
    app_layout.add_label("Excellent. You're done with the routine. " +
                         "To a better health, becoming fit is your daily quest.",
                         0.05, True)

    reset_button            = home.HomePage.new_trans_button(manager, 3, font_scale=0.144)
    reset_button.pos_hint   = {'center_x': 0.5, 'center_y': 0.16}
    reset_button.text       = 'SELECT ROUTINE'
    reset_button.size_hint  = [0.40, 0.16]

    app_layout.add_widget(reset_button)
    return app_layout