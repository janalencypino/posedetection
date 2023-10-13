from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, NoTransition
from kivy.uix.layout import Layout
from typing import Callable

import kivy_config as cfg

app_data    = {}
    
class HomePage(App):
    _manager    = ScreenManager()
    def index_to_screen(index: int):
        return 'screen_' + str(index)

    def screen_to_index(scr_text: str) -> int:
        return int(scr_text[7:])
    
    def get_manager():
        return HomePage._manager
    
    def build(self):
        from kivy.core.window import Window
        Window.size     = cfg.default_app_size
        Window.top      = 80
        Window.left     = 128
        return HomePage._manager
    
    def new_trans_button(manager: ScreenManager, return_index: int,
                         do_transition: bool = True, callback: Callable[[None], None] = None,
                         back_button: Button = None):
        back_button             = ((not (back_button is None)) and back_button) or Button(
            text                = cfg.back_button_params['text'],
            size_hint           = cfg.back_button_params['size_hint'],
            pos_hint            = cfg.back_button_params['pos_hint'],
            font_name           = cfg.font_name,
            background_color    = cfg.button_params['bg_color'],
            background_normal   = cfg.button_params['bg_normal'],
            color               = cfg.button_params['color']
        )
        
        #   ===============================
        #       Back button definition
        #   ===============================
        def on_back_button_resize(back_button, size):
            back_button.font_size   = 0.24*size[0]

        def on_back_button_return(back_button):
            cur_index   = HomePage.screen_to_index(manager.current)
            if (return_index < 3):
                app_data['user_id'] = None
 
            # We're going back.
            if (not do_transition):
                manager.transition      = NoTransition()
            elif (return_index < cur_index):
                manager.transition      = SlideTransition(direction="right")
            else:
                manager.transition      = SlideTransition(direction="left")

            manager.current         = HomePage.index_to_screen(return_index)
            if (not (callback is None)):
                callback()

        back_button.bind(size=on_back_button_resize)
        back_button.bind(on_release=on_back_button_return)

        return back_button
    
def page_recipe(manager: ScreenManager):
    app_layout = FloatLayout()
    app_bg     = Image(source=cfg.home_page, fit_mode = "fill")
    button     = Button(
                    text                = 'START',
                    size_hint           = [0.30, 0.2],
                    pos_hint            = {'center_x': 0.75, 'center_y': 0.2},
                    font_name           = cfg.font_name,
                    background_color    = cfg.button_params['bg_color'],
                    background_normal   = cfg.button_params['bg_normal'],
                    color               = cfg.button_params['color']
                )
    
    def on_resize(instance, size):
        instance.font_size  = 0.24*size[0]

    def move_to_userpage(instance):
        manager.transition  = SlideTransition(direction="left")
        manager.current     = HomePage.index_to_screen(2)

    button.bind(size=on_resize)
    button.bind(on_release=move_to_userpage)

    app_layout.add_widget(app_bg)
    app_layout.add_widget(button)

    return app_layout

def add_screen_page(manager: ScreenManager,
                    app_layout: Layout,
                    _name: str,
                    screen_class = Screen):
    screen  = screen_class(name = _name)
    screen.add_widget(app_layout)
    manager.add_widget(screen)
    return screen

def render_app(app: App):
    import load_default_exercises as load_exer
    import kivy_ready_made_routine as kv_routine
    kv_routine.load_exercises(load_exer.default_exer_list(),
                              load_exer.default_exer_desc())
    # HomePage.get_manager().current  = HomePage.index_to_screen(7)
    app.run()

def prep_pages():
    import kivy_userpage
    import kivy_user_routine_choice
    import kivy_ready_made_routine
    import kivy_custom_routine
    import kivy_exercise_countdown
    import kivy_exercise_page
    import exercise_class

    app     = HomePage(title="FitQuest")
    manager = HomePage._manager

    add_screen_page(manager,
                    page_recipe(manager),
                    HomePage.index_to_screen(1)
                )
    add_screen_page(manager,
                    kivy_userpage.page_recipe(manager),
                    HomePage.index_to_screen(2)
                )
    add_screen_page(manager,
                    kivy_user_routine_choice.page_recipe(manager),
                    HomePage.index_to_screen(3)
                )
    add_screen_page(manager,
                    kivy_ready_made_routine.page_recipe(manager),
                    HomePage.index_to_screen(4)
                )
    add_screen_page(manager,
                    kivy_custom_routine.page_recipe(manager),
                    HomePage.index_to_screen(5)
                )
    add_screen_page(manager,
                    kivy_exercise_countdown.page_recipe(manager),
                    HomePage.index_to_screen(6),
                    kivy_exercise_countdown.LoadScreen  
                )
    add_screen_page(manager,
                    kivy_exercise_page.page_recipe(manager),
                    HomePage.index_to_screen(7)
                )
    return app

def preload_exercises():
    import load_default_exercises as load_exer
    load_exer.populate_exercises()

if __name__ == '__main__':
    preload_exercises()
    render_app(prep_pages())