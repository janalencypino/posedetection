from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, SlideTransition

import kivy_homepage as home
import kivy_config as cfg

def get_button_text_list():
    return ['READY-MADE ROUTINE', 'CUSTOMIZED ROUTINE']

def page_recipe(manager: ScreenManager):
    app_layout      = FloatLayout()
    app_bg          = Image(source=cfg.user_page, fit_mode = "fill")

    label           = Label(
        text        = 'SELECT YOUR ROUTINE:',
        size_hint   = [0.55, 0.20],
        pos_hint    = {'center_x': 0.50, 'center_y': 0.65},
        font_name   = cfg.font_name,
        font_size   = 80,
        # color       = cfg.button_params['color']
    )

    button_layout   = FloatLayout(
        size_hint=[0.8, 0.3],
        pos_hint={'center_x': 0.5, 'center_y': 0.45}
    )

    def get_button_release_func():
        def premade_fun():
            manager.current = home.HomePage.index_to_screen(4)

        def custom_fun():
            manager.current = home.HomePage.index_to_screen(5)

        return [premade_fun, custom_fun]

    btn_text_list   = get_button_text_list()
    btn_resp_list   = get_button_release_func()
    for i in range(2):
        button                  = Button(
            text                = btn_text_list[i],
            font_name           = cfg.font_name,
            size_hint           = [0.48, 0.6],
            pos_hint            = {'center_x': (2*i + 1)*0.25, 'center_y': 0.5},
            background_color    = cfg.button_params['bg_color'],
            background_normal   = cfg.button_params['bg_normal'],
            color               = cfg.button_params['color'],
        )

        def button_event_factory(button: Button, callback):
            def on_button_resize(button: Button, size):
                button.font_size    = 0.10*size[0]

            button.bind(size = on_button_resize)

            if (not (callback is None)):
                def on_button_release(button: Button):
                    callback()

                button.bind(on_release = on_button_release)

        button_event_factory(button, btn_resp_list[i])
        button_layout.add_widget(button)

    back_button             = home.HomePage.new_back_button(manager, 2)

    app_layout.add_widget(app_bg)
    app_layout.add_widget(label)
    app_layout.add_widget(back_button)
    app_layout.add_widget(button_layout)

    return app_layout