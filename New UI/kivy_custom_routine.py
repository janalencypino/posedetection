from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from fitquest_kivy_widgets import BackgroundLabel, ImageButton

import kivy_homepage as home
import kivy_config as cfg

_data           = {
    'select'    : {
        'exercise'  : "",
        'reps'      : -1,
        'sets'      : -1,
    },
}

def exercise_recipe(manager: ScreenManager):
    exer_layout     = RelativeLayout(
        size_hint   = [0.24, 0.66],
        pos_hint    = {'center_x': 0.20, 'center_y': 0.44}
    )

    exer_top_label  = BackgroundLabel(
        size_hint   = [1.00, 0.25],
        pos_hint    = {'center_x': 0.50, 'y': 0.75},
        text        = 'EXERCISES:'
    )

    #   =============================
    #           Top Area
    #   =============================
    exer_top_label.change_bg_color(
        color       = (80/255, 0, 136/255, 1)
    )
    exer_top_label.change_color()   # Default parameters are used.
    exer_top_label.set_font_size(
        fixed       = False,
        new_size    = 0.20
    )
    exer_top_label.set_bg_radius(
        radius      = (20, 20, 2, 2)
    )

    #   =============================
    #           Bottom Area
    #   =============================
    exer_bottom_label   = BackgroundLabel(
        size_hint       = [1.00, 1.00],
        pos_hint        = {'center_x': 0.50, 'center_y': 0.5},
    )
    exer_bottom_label.set_bg_radius(
        radius          = (20, 20, 20, 20)
    )

    exer_bottom_scroll  = ScrollView(
        size_hint       = [0.90, 0.70],
        pos_hint        = {'center_x': 0.5, 'y': 0.025},
    )

    def make_exercise_widgets(exer_bottom_scroll: ScrollView):
        from exercise_class import exercise_dict, BaseExercise

        def new_grid():
            return GridLayout(
                size_hint   = [1.0, 0.75],
                pos_hint    = {'center_x': 0.5, 'top': 0.95},
                cols        = 2,
                spacing     = 20,
            )
        
        def on_scrollview_end(instance, value):
            instance.value  = value

        grid                = new_grid()
        iterable_i          = -1

        exer_bottom_scroll.add_widget(grid)
        exer_bottom_scroll.bind(on_scroll_stop = on_scrollview_end)

        for key, exercise in exercise_dict().items():
            exercise: BaseExercise
            iterable_i     += 1

            widget          = ImageButton(
                size_hint           = [0.475, 1],
                pos_hint            = {'x': ((iterable_i % grid.cols)*0.5) + 0.025, 'center_y': 0.40},
                background_color    = (144/255, 80/255, 192/255, 1),
            )
            widget.set_image_source(exercise.img_path)
            widget.data     = key
            
            grid.add_widget(widget)

    make_exercise_widgets(exer_bottom_scroll)

    exer_layout.add_widget(exer_bottom_label)
    exer_layout.add_widget(exer_bottom_scroll)
    exer_layout.add_widget(exer_top_label)
    return exer_layout

def count_recipe(manager: ScreenManager):
    count_layout    = RelativeLayout(
        size_hint   = [0.24, 0.32],
        pos_hint    = {'center_x': 0.50, 'center_y': 0.612}
    )

    count_top_label = BackgroundLabel(
        size_hint   = [1.00, 0.25],
        pos_hint    = {'center_x': 0.50, 'y': 0.75},
        text        = 'EXERCISES:'
    )

    #   =============================
    #           Top Area
    #   =============================
    count_top_label.change_bg_color(
        color       = (80/255, 0, 136/255, 1)
    )
    count_top_label.change_color()   # Default parameters are used.
    count_top_label.set_font_size(
        fixed       = False,
        new_size    = 0.20
    )
    count_top_label.set_bg_radius(
        radius      = (20, 20, 2, 2)
    )

    #   =============================
    #           Bottom Area
    #   =============================
    count_bottom_label  = BackgroundLabel(
        size_hint       = [1.00, 1.00],
        pos_hint        = {'center_x': 0.50, 'center_y': 0.5},
    )
    count_bottom_label.set_bg_radius(
        radius          = (20, 20, 20, 20)
    )

    count_bottom_scroll  = ScrollView(
        size_hint       = [0.90, None],
        pos_hint        = {'center_x': 0.5, 'y': 0.025},
    )

    def make_count_widgets(count_bottom_scroll: ScrollView):
        from exercise_class import exercise_dict, BaseExercise

        def new_grid():
            grid                = GridLayout(
                size_hint       = [1.0, None],
                pos_hint        = {'center_x': 0.5, 'center_y': 0.50},
                cols            = 4,
                spacing         = 15,
            )
            grid.bind
            return grid

        grid                = new_grid()
        iterable_i          = 0

        count_bottom_scroll.add_widget(grid)
        count_bottom_scroll.do_scroll_x = False
        count_bottom_scroll.do_scroll_y = True

        def count_callback_factory(widget: Button, index: int, font_scale: float = 0.20):
            def count_callback(instance):
                global _data
                _data['select']['reps'] = index

            def on_size(instance, size):
                instance.font_size  = font_scale*size[0]

            widget.bind(on_release  = count_callback)
            widget.bind(size        = on_size)

        for i in range(1,13):
            exercise: BaseExercise
            iterable_i     += 1

            widget                  = Button(
                text                = str(5*iterable_i),
                size_hint           = [0.25, None],
                pos_hint            = {'x': (((iterable_i - 1) % grid.cols)*0.5) + 0.025},
                background_normal   = "",
                background_color    = (144/255, 80/255, 192/255, 1),
                font_name           = cfg.font_name,
            )
            count_callback_factory(widget, iterable_i, 0.28)
            
            grid.add_widget(widget)

    make_count_widgets(count_bottom_scroll)

    count_layout.add_widget(count_bottom_label)
    count_layout.add_widget(count_bottom_scroll)
    count_layout.add_widget(count_top_label)
    return count_layout

def page_recipe(manager: ScreenManager):
    app_layout      = FloatLayout()
    app_bg          = Image(source=cfg.user_page, fit_mode = "fill")

    app_layout.add_widget(app_bg)
    app_layout.add_widget(exercise_recipe(manager))
    app_layout.add_widget(count_recipe(manager))
    return app_layout