from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.clock import Clock
from exercise_class import Exercise
from functools import partial

import kivy_homepage as home
import kivy_config as cfg

_cooldown_factor    = 0.5
_cooldown_step      = 5.0
_widgets            = {
    'counter'       : None,
}

class CooldownPage(FloatLayout):
    def __init__(self, **kwargs):
        super(CooldownPage, self).__init__(**kwargs)

        self.app_bg = Image(source=cfg.user_page, fit_mode = "fill")
        self.add_widget(self.app_bg)

    def add_label(self, text: str, text_size: float = 40, scale: bool = False):
        if (not hasattr(self, 'label')):
            self.label  = []

        _label_y        = 0.8 - 0.4*len(self.label)
        _label          = Label(
            text        = text,
            size_hint   = [0.80, 0.4],
            pos_hint    = {'center_x': 0.5, 'y': _label_y},
            font_name   = cfg.font_name,
            font_size   = text_size,
            text_size   = [0.80, 1],
            halign      = 'center'
        )
        _label_dict     = {
            'label'         : _label,
            'scale'         : scale,
            'text_size'     : text_size,
            'text_scale'    : _label.text_size[:],
        }

        self.add_widget(_label)
        self.label.append(_label_dict)
        return _label

    def on_pos(self, instance, pos):
        print("Repositioning")

    def on_size(self, instance, size):
        self.app_bg.size    = self.size
        if (hasattr(self, 'label')):
            for _label_dict in self.label:
                _label      = _label_dict['label']
                _label.size = [size[0]*_label.size_hint[0],
                               size[1]*_label.size_hint[1]]
                
                _label.text_size        = [_label_dict['text_scale'][0]*size[0],
                                           _label_dict['text_scale'][1]*size[1]]
                
                if _label_dict['scale']:
                    _label.font_size    = _label_dict['text_size']*_label.size[0]
                else:
                    _label.font_size    = _label_dict['text_size']

def page_recipe(manager: ScreenManager):
    app_layout          = CooldownPage()
    app_layout.add_label("Well done. Rest for a while before you continue " +
                         "your exercise. You'll resume your routine in: ",
                         0.05, True)
    
    _widgets['counter'] = app_layout.add_label("0", 0.20, True)
    _widgets['manager'] = manager
    return app_layout

def get_counter_value() -> int:
    if _widgets['counter'] is None:
        return 0
    return int(_widgets['counter'].text)

def set_counter_value(value: int):
    if _widgets['counter'] is None:
        return
    _widgets['counter'].text    = str(value)

class LoadScreen(Screen):
    def has_remaining_exercise() -> bool:
        if not 'exercise_list' in home.app_data:
            return False
        
        return len(home.app_data['exercise_list']) > 0

    def get_cooldown_time() -> int:
        import math
        # Get the exercise list
        if not 'exercise_list' in home.app_data:
            return 1

        exer_list       = home.app_data['exercise_list']
        # Assume the exercise list has already been modified
        # prior to the on_enter event.
        if len(exer_list) < 1:
            return 1
        
        exercise: Exercise  = exer_list[0]
        duration: float     = exercise.duration * _cooldown_factor
        duration: int       = int(math.ceil(duration // _cooldown_step) * _cooldown_step)
        return duration

    def on_redirect(self, *args):
        import kivy_exercise_page

        Clock.unschedule(self.countdown)
        self.countdown          = None

        manager: ScreenManager  = _widgets['manager']
        if LoadScreen.has_remaining_exercise():
            manager.current         = home.HomePage.index_to_screen(7)
            kivy_exercise_page.on_page_load()
        else:
            manager.current         = home.HomePage.index_to_screen(9)

    def on_tick(self, *args):
        self.time          -= 1
        set_counter_value(self.time)
        if self.time < 1:
            set_counter_value(0)
            Clock.unschedule(self.countdown)
            self.countdown  = Clock.schedule_once(
                partial(LoadScreen.on_redirect, self),
                0.25,
            )
            return

    def on_enter(self):
        self.time: int      = LoadScreen.get_cooldown_time()
        set_counter_value(self.time)
        
        self.countdown      = Clock.schedule_interval(
            partial(LoadScreen.on_tick, self),
            1.0,
        )