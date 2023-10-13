from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.graphics import Color, RoundedRectangle
from typing import Callable

import kivy_homepage as home
import kivy_config as cfg

#   ==================================
#       Configurable parameters
#   ==================================
inlet_widget_rel_size   = 0.96

#   ==================================
#       Private variables
#   ==================================
_app_layout_elements    = []

def counter_recipe(manager: ScreenManager):
    counter_layout      = FloatLayout(
        size_hint       = [0.24, 0.36],
        pos_hint        = {'center_x': 0.15, 'center_y': 0.52}
    )

    #   ==========================================
    #           Create background
    #   ==========================================
    counter_empty_button    = Button(
        size_hint           = [1.0, 1.0],
        pos_hint            = {'center_x': 0.5, 'center_y': 0.5},
        background_color    = (0, 0, 0, 0),
        background_normal   = cfg.button_params['bg_normal'],
        disabled            = True
    )
    counter_layout.add_widget(counter_empty_button)

    with counter_empty_button.canvas.before:
        Color(24/255, 24/255, 24/255, 1)
        border_rect             = RoundedRectangle(
            radius              = (10, 10),
            pos_hint            = {'center_x': 0.50, 'center_y': 0.50}
        )
        Color(64/255, 0, 128/255, 1)
        inner_rect              = RoundedRectangle(
            radius              = (10, 10),
            pos_hint            = {'center_x': 0.50, 'center_y': 0.50}
        )

    def on_layout_size(instance, size):
        border_rect.size        = size
        inner_rect.size         = (inlet_widget_rel_size*size[0],
                                   inlet_widget_rel_size*size[1])

    def on_layout_pos(instance, pos):
        border_rect.pos         = pos
        inner_rect.pos          = (pos[0] + (instance.size[0] - inner_rect.size[0])*0.5,
                                   pos[1] + (instance.size[1] - inner_rect.size[1])*0.5)

    counter_empty_button.bind(size = on_layout_size)
    counter_empty_button.bind(pos = on_layout_pos)

    #   ==========================================
    #           Create text labels
    #   ==========================================
    label_layout    = GridLayout(
        size_hint   = [1.0, 1.0],
        pos_hint    = {'center_x': 0.5, 'center_y': 0.5},
        rows        = 2,
        cols        = 1
    )
    
    label_text      = Label(
        text        = 'Count:',
        color       = cfg.button_params['bg_color'],
        font_name   = cfg.font_name,
        size_hint   = [1.0, 0.35],
        halign      = 'center',
        valign      = 'bottom'
    )

    label_value     = Label(
        text        = '0',
        color       = cfg.button_params['bg_color'],
        font_name   = cfg.font_name,
        size_hint   = [1.0, 0.65],
        halign      = 'center',
        valign      = 'top'
    )

    def on_label_text_size(instance, size):
        label_text.font_size    = 0.20*size[0]
        label_text.text_size    = (instance.size[0], None)

    def on_label_value_size(instance, size):
        label_value.font_size    = 0.40*size[0]
        label_value.text_size    = (instance.size[0], None)

    label_text.bind(size=on_label_text_size)
    label_value.bind(size=on_label_value_size)

    label_layout.add_widget(label_text)
    label_layout.add_widget(label_value)

    counter_layout.add_widget(label_layout)
    return counter_layout

def exercise_recipe(manager: ScreenManager):
    fake_layout         = FloatLayout(
        size_hint       = [0.35, 0.60],
        pos_hint        = {'center_x': 0.472, 'center_y': 0.50},
    )

    fake_layout.image       = Image(
        source              = '',
        fit_mode            = 'fill',
        size_hint           = [1.0, 1.0],
        pos_hint            = {'center_x': 0.50, 'center_y': 0.50}
    )
    fake_layout.add_widget(fake_layout.image)

    return fake_layout

def info_recipe(manager: ScreenManager):
    info_layout         = FloatLayout(
        size_hint       = [0.32, 0.28],
        pos_hint        = {'center_x': 0.828, 'center_y': 0.56}
    )

    #   ==========================================
    #           Create background
    #   ==========================================
    info_empty_button   = Button(
        size_hint           = [1.0, 1.0],
        pos_hint            = {'center_x': 0.5, 'center_y': 0.5},
        background_color    = (0, 0, 0, 0),
        background_normal   = cfg.button_params['bg_normal'],
        disabled            = True
    )
    info_layout.add_widget(info_empty_button)

    with info_empty_button.canvas.before:
        Color(24/255, 24/255, 24/255, 1)
        border_rect             = RoundedRectangle(
            radius              = (10, 10),
            pos_hint            = {'center_x': 0.50, 'center_y': 0.50}
        )
        Color(64/255, 0, 128/255, 1)
        inner_rect              = RoundedRectangle(
            radius              = (10, 10),
            pos_hint            = {'center_x': 0.50, 'center_y': 0.50}
        )

    def on_layout_size(instance, size):
        border_rect.size        = size
        inner_rect.size         = (inlet_widget_rel_size*size[0],
                                   inlet_widget_rel_size*size[1])

    def on_layout_pos(instance, pos):
        border_rect.pos         = pos
        inner_rect.pos          = (pos[0] + (instance.size[0] - inner_rect.size[0])*0.5,
                                   pos[1] + (instance.size[1] - inner_rect.size[1])*0.5)

    info_layout.bind(size = on_layout_size)
    info_layout.bind(pos = on_layout_pos)

    #   ==========================================
    #           Create text labels
    #   ==========================================

    label_layout        = GridLayout(
        size_hint       = [1.0, 1.0],
        pos_hint        = {'center_x': 0.5, 'center_y': 0.5},
        rows            = 2,
        cols            = 2
    )
    
    #   Add a generic callback that will handle the
    #   dynamic font size scaling.
    def label_factory(scale: float):
        def on_label_size(instance, size):
            instance.font_size  = scale*size[0]

        return on_label_size
    
    label_exercise          = Label(
        text                = 'Exercise:',
        color               = cfg.button_params['bg_color'],
        font_name           = cfg.font_name,
        size_hint           = [0.40, 0.50],
        halign              = 'right'
    )

    label_exercise_value    = Label(
        color               = cfg.button_params['bg_color'],
        font_name           = cfg.font_name,
        halign              = 'left'
    )

    label_sets              = Label(
        text                = 'Reps:',
        color               = cfg.button_params['bg_color'],
        font_name           = cfg.font_name,
        size_hint           = [0.40, 0.50],
        halign              = 'right'
    )

    label_sets_value        = Label(
        text                = '0',
        color               = cfg.button_params['bg_color'],
        font_name           = cfg.font_name,
        halign              = 'left'
    )

    label_exercise.bind(size=label_factory(0.24))
    label_exercise_value.bind(size=label_factory(0.144))
    label_sets.bind(size=label_factory(0.24))
    label_sets_value.bind(size=label_factory(0.144))

    label_layout.add_widget(label_exercise)
    label_layout.add_widget(label_exercise_value)
    label_layout.add_widget(label_sets)
    label_layout.add_widget(label_sets_value)
    info_layout.add_widget(label_layout)
    return info_layout

def camera_recipe(manager: ScreenManager):
    pass

def add_layout_widget(app_layout, widget):
    _app_layout_elements.append(widget)
    app_layout.add_widget(widget)

def page_recipe(manager: ScreenManager):
    app_layout      = FloatLayout()
    app_bg          = Image(source=cfg.user_page, fit_mode = "fill")

    add_layout_widget(app_layout, app_bg)
    add_layout_widget(app_layout, counter_recipe(manager))
    add_layout_widget(app_layout, exercise_recipe(manager))
    add_layout_widget(app_layout, info_recipe(manager))
    # add_layout_widget(app_layout, camera_recipe(manager))

    return app_layout

class ExercisePage:
    '''
    Note:
    
    While Kivy child widgets added with add_widget are inserted
    starting at index 0, _app_layout_elements are instead
    appended, hence inserted at the last index (len(list) - 1).

    counter_layout index is 1,

    exercise_layout index is 2, and

    info_layout index is 3.
    '''

    def get_exercise_count():
        '''
        Returns the count value found at the left side of the page.
        '''
        app_layout      = _app_layout_elements[1]
        app_widget      = app_layout.children[0].children[0]
        return int(app_widget.text)
    
    def set_exercise_count(value: int):
        '''
        Sets the count value found at the left side of the page.
        '''
        app_layout      = _app_layout_elements[1]
        app_widget      = app_layout.children[0].children[0]
        app_widget.text = str(value)

    def get_exercise():
        '''
        Returns the current exercise routine (string).
        '''
        app_layout      = _app_layout_elements[3]
        app_widget      = app_layout.children[0].children[2]
        return app_widget.text
    
    def set_exercise(routine: str):
        '''
        Sets the current exercise routine (string).
        '''
        app_layout      = _app_layout_elements[3]
        app_widget      = app_layout.children[0].children[2]
        app_widget.text = routine

    def get_exercise_reps():
        '''
        Returns the current number of reps (int).
        '''
        app_layout      = _app_layout_elements[3]
        app_widget      = app_layout.children[0].children[0]
        return int(app_widget.text)
    
    def set_exercise_reps(reps: int):
        '''
        Sets the current number of reps (int).
        '''
        app_layout      = _app_layout_elements[3]
        app_widget      = app_layout.children[0].children[0]
        app_widget.text = str(reps)

    def get_exercise_image():
        '''
        Returns the path of the currently-rendered
        image file (usually an exercise image). (string)
        '''
        app_layout      = _app_layout_elements[2]
        app_widget      = app_layout.children[0]
        return app_widget.source
    
    def set_exercise_image(new_src: str):
        '''
        Returns the path of the currently-rendered
        image file (usually an exercise image). (string)
        '''
        app_layout          = _app_layout_elements[2]
        app_widget          = app_layout.children[0]
        app_widget.source   = new_src


    _subscriber_fun         = []
    def add_subscriber(fun: Callable[[None], None]):
        if (fun is None):
            return
        
        ExercisePage._subscriber_fun.append(fun)