from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.clock import Clock

import kivy_exercise_page as exer_page
import kivy_homepage as home
import kivy_config as cfg

countdown_label     = None
counter_event       = None
_manager            = None

def get_tick():
    if (countdown_label is None):
        return 0
    return int(countdown_label.text)

def set_tick(value: int):
    if (countdown_label is None):
        return
    countdown_label.text = str(value)

class LoadScreen(Screen):
    def to_exercise_page(*args):
        global counter_event
        counter_event       = None
        _manager.current    = home.HomePage.index_to_screen(7)
        exer_page.on_page_preload()
        exer_page.on_page_load()

    def update_tick(*args):
        set_tick(get_tick() - 1)
        if (get_tick() < 1):
            global counter_event
            Clock.unschedule(counter_event)
            counter_event   = Clock.schedule_once(LoadScreen.to_exercise_page, 0.25)

    def on_enter(self):
        global counter_event
        if (not (counter_event is None)):
            Clock.unschedule(counter_event)
            
        counter_event   = Clock.schedule_interval(LoadScreen.update_tick, 1)
        set_tick(5)

def page_recipe(manager: ScreenManager):
    global _manager
    _manager        = manager
    app_layout      = FloatLayout()
    app_bg          = Image(source=cfg.user_page, fit_mode = "fill")

    exer_label      = Label(
        text        = 'Ready in:',
        halign      = 'center',
        pos_hint    = {'center_x': 0.5, 'center_y': 0.65},
        size_hint   = [0.5, 0.5],
        font_name   = cfg.font_name,
        font_size   = 192,
    )

    global countdown_label
    countdown_label = Label(
        text        = '0',
        halign      = 'center',
        pos_hint    = {'center_x': 0.5, 'center_y': 0.35},
        size_hint   = [0.5, 0.5],
        font_name   = cfg.font_name,
        font_size   = 256,
    )

    app_layout.add_widget(app_bg)
    app_layout.add_widget(exer_label)
    app_layout.add_widget(countdown_label)
    return app_layout