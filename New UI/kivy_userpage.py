from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, SlideTransition

import kivy_homepage as home
import kivy_config as cfg

def bake_user_elements(manager: ScreenManager):
    user_layout = BoxLayout(
        size_hint       = [0.75, 0.25],
        pos_hint        = {
            'center_x': 0.50,
            'center_y': 0.55
        }
    )

    for i in range(5):
        button_layout   = BoxLayout(
            orientation ='vertical',
            size_hint   = [0.20, 1.0],
            pos_hint    = {
                'center_x': (2*i + 1)*0.10,
                'center_y': 0.25
            }
        )
        button          = Button(
            background_normal   = "",
            size_hint           = [0.80, 0.75],
            background_color    = (0,0,0,0)
        )
        button_img      = Image(source=cfg.user_icon, fit_mode = "fill")
        button_label    = Label(
            text        = 'User ' + str(i + 1),
            size_hint   = [1.0, 0.25],
        )

        button.pos_hint = {
            'center_x': 0.5,
            'center_y': 0.5
        }

        def button_factory(button: Button, button_img: Image, i: int, source):
            def button_adjust_pos(button, pos):
                button_img.pos  = pos

            def button_adjust_size(button, size):
                button_img.size = size

            def button_on_release(button):
                home.app_data['user_id']    = i
                manager.transition          = SlideTransition(direction="left")
                manager.current             = home.HomePage.index_to_screen(3)

            button.bind(pos         = button_adjust_pos)
            button.bind(size        = button_adjust_size)
            button.bind(on_release  = button_on_release)
            button.add_widget(button_img)

        def button_label_factory(button_label: Label):
            def on_resize(button_label, size):
                button_label.font_size  = 0.20*size[0]

            button_label.bind(size=on_resize)

        button_factory(button, button_img, i + 1, button_img.source)
        button_label_factory(button_label)

        button_layout.add_widget(button)
        button_layout.add_widget(button_label)
        user_layout.add_widget(button_layout)

    return user_layout
    
def page_recipe(manager: ScreenManager):
    app_layout      = FloatLayout()
    app_bg          = Image(source=cfg.user_page, fit_mode = "fill")
    q_label         = Label(
        text        = "WHO'S EXERCISING?",
        size_hint   = [0.30, 0.80],
        pos_hint    = {
            'center_x': 0.5,
            'center_y': 0.75
        },
        font_name   = cfg.font_name,
    )

    back_button             = home.HomePage.new_back_button(manager, 1)
    
    #   ===============================
    #       Label definition
    #   ===============================
    def on_label_resize(label, size):
        label.font_size = 0.32*size[0]

    q_label.bind(size=on_label_resize)

    #   ===============================
    #       App Layout Finalization
    #   ===============================
    app_layout.add_widget(app_bg)
    app_layout.add_widget(q_label)
    app_layout.add_widget(back_button)
    app_layout.add_widget(bake_user_elements(manager))

    return app_layout