from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.graphics import Color, Rectangle, RoundedRectangle, Rotate, PushMatrix, PopMatrix
from kivy.animation import Animation

import kivy_homepage as home
import kivy_config as cfg

_routine_options    = [None, None]
_start_button       = None
_routine_choice     = -1
_routine_list       = []

class QuasiButtonLabel(Label):
    def __init__(self, **kwargs):
        super(QuasiButtonLabel, self).__init__(**kwargs)
        self.background_normal  = cfg.button_params['bg_normal']
        self.background_color   = cfg.button_params['bg_color']
        self.color              = cfg.button_params['color']

        with self.canvas.before:
            self.color_template = Color(*self.background_color)
            self.rect           = RoundedRectangle(
                pos             =(0, 0),
                size            =(200, 100),
                radius          =(10, 10)
            )
            self.text           = self.text

    def on_pos(self, instance, pos):
        self.rect.pos           = pos

    def on_size(self, instance, size):
        self.rect.size          = size
        self.font_size          = 0.10*size[0]

    def on_background_color(self, instance, color):
        self.color_template.rgba    = color
    
    def on_text_size(self, instance, text_size):
        self.text_size              = self.width*0.8

class RoutineWidgetLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(FloatLayout, self).__init__(**kwargs)

        self.exer_icon      = Image(
            source          = '',
            size_hint       = [0.8, 0.4],
            pos_hint        = {'center_x': 0.5, 'center_y': 0.7},
            fit_mode        = 'fill',
        )

        self.exer_reps      = Label(
            text            = 'Repetitions: 0',
            size_hint       = [0.8, 0.2],
            pos_hint        = {'center_x': 0.5, 'center_y': 0.3},
            color           = (0,0,0,1),
        )

        self.exer_sets      = Label(
            text            = 'Sets: 0',
            size_hint       = [0.8, 0.2],
            pos_hint        = {'center_x': 0.5, 'center_y': 0.1},
            color           = (0,0,0,1),
        )

        self.add_widget(self.exer_icon)
        self.add_widget(self.exer_reps)
        self.add_widget(self.exer_sets)
        self.text_scale     = 0.20

    def on_size(self, instance, size):
        self.exer_reps.font_size    = self.text_scale*size[0]
        self.exer_sets.font_size    = self.text_scale*size[0]

    def on_pos(self, instance, pos):
        self.exer_icon.pos  = pos
        self.exer_reps.pos  = pos
        self.exer_sets.pos  = pos

    def get_reps(self):
        '''
        Returns the number of reps for this particular exercise.
        '''
        return int(self.exer_reps.text[13:])

    def set_reps(self, reps: int):
        '''
        Updates the number of reps for this particular exercise.
        '''
        self.exer_reps.text = 'Repetitions: ' + str(reps)

    def get_nsets(self):
        '''
        Returns the number of sets for this particular exercise.
        '''
        return int(self.exer_sets.text[6:])

    def set_nsets(self, sets: int):
        '''
        Updates the number of sets for this particular exercise.
        '''
        self.exer_sets.text = 'Sets: ' + str(sets)

    def get_image_source(self):
        '''
        Returns the image path for this particular exercise.
        Provided just in case this is needed.
        '''
        return self.exer_icon.source

    def set_image_source(self, src: str):
        '''
        Updates the image path for this particular exercise.
        '''
        self.exer_icon.source    = src

def option_recipe(manager: ScreenManager):
    option_layout   = FloatLayout(
        size_hint   = [0.75, 0.56],
        pos_hint    = {'center_x': 0.5, 'center_y': 0.50}
    )

    for i in range(2):
        opt_button              = Button(
            size_hint           = [1.00, 0.45],
            pos_hint            = {'center_x': 0.5, 'center_y': (4 - (2*i + 1))*0.25},
            background_normal   = cfg.button_params['bg_normal'],
            background_color    = (0,0,0,0)
        )

        # ==========================================
        #           The Image Backdrop
        # ==========================================

        opt_button_image        = Image(
            source              = cfg.option_img_path,
            fit_mode            = 'fill',
            size_hint           = [1.00, 1.00],
        )

        def opt_button_factory(opt_button, opt_button_image, i):
            click_layer         = None
            def on_button_size(instance, size):
                opt_button_image.size   = size
                
                global _routine_choice
                if (_routine_choice == i):
                    nonlocal click_layer
                    if (click_layer is None):
                        return
                    click_layer.size    = size

            def on_button_pos(instance, pos):
                opt_button_image.pos    = pos
                
                global _routine_choice
                if (_routine_choice == i):
                    nonlocal click_layer
                    if (click_layer is None):
                        return
                    click_layer.pos     = pos


            def on_button_click(instance):
                global _routine_choice

                if (_routine_choice > -1):
                    print("Previous, current:", _routine_choice, i)
                    _routine_options[_routine_choice].canvas.after.clear()

                _start_button.disabled      = (_routine_choice == i)
                if (_routine_choice == i):
                    _routine_choice         = -1
                else:
                    _routine_choice         = i

                start_opacity, end_opacity  = 0.2, 0.0
                opt_button_image.canvas.after.clear()
                if (_routine_choice == i):
                    # Create click layer.
                    start_opacity, end_opacity  = end_opacity, start_opacity
                
                nonlocal click_layer
                if (end_opacity <= 0.0):
                    click_layer = None
                    return
                
                with opt_button_image.canvas.after:
                    Color(0.0, 0.0, 0.0, end_opacity)
                    click_layer         = Rectangle(
                        size            = opt_button_image.size,
                        pos             = opt_button_image.pos,
                    )

            opt_button.bind(size=on_button_size)
            opt_button.bind(pos=on_button_pos)
            opt_button.bind(on_release=on_button_click)
            opt_button.add_widget(opt_button_image)

        opt_button_factory(opt_button, opt_button_image, i)
        _routine_options[i]     = opt_button_image

        # ==========================================
        #       The Three Image Sub-Layouts
        # ==========================================

        # ==========================================
        #               Routine Text
        # ==========================================
        
        rot_width               = 0.06
        rotated_layout          = FloatLayout(
            size_hint           = [rot_width, 1.0],
            pos_hint            = {'x': 0.0, 'y': 0.0},
        )

        rotated_text            = Label(
            size_hint           = [1, 1],
            pos_hint            = {'x': 0.0, 'y': -0.04},
            font_size           = 54,
            font_name           = cfg.font_name,
        )

        rotated_text.text   = 'ROUTINE ' + str(i+1)  
        rotated_layout.add_widget(rotated_text)

        def opt_button_image_factory(opt_button_image, child):
            def on_btn_image_size(instance, size):
                for outer_child in instance.children:
                    if outer_child.size_hint is None:
                        pass
                        # outer_child.size    = outer_child.size
                    else:
                        outer_child.size    = [size[0]*outer_child.size_hint[0],
                                               size[1]*outer_child.size_hint[1]]

            def on_btn_image_pos(instance, pos):
                for outer_child in instance.children:
                    if outer_child.pos_hint is None:
                        outer_child.pos = pos
                        continue

                    offset          = [0, 0]
                    pos_key         = ''
                    if 'x' in outer_child.pos_hint:
                        offset[0]   = instance.size[0]*outer_child.pos_hint['x']
                        pos_key     = 'x'
                    elif 'center_x' in outer_child.pos_hint:
                        offset[0]   = instance.size[0]*outer_child.pos_hint['center_x'] + outer_child.size[0]*0.5
                        pos_key     = 'center_x'
                    elif 'right' in outer_child.pos_hint:
                        offset[0]   = instance.size[0]*(1 - outer_child.pos_hint['right'])
                        pos_key     = 'right'

                    pos_key         = ''
                    if 'y' in outer_child.pos_hint:
                        offset[1]   = instance.size[1]*outer_child.pos_hint['y']
                        pos_key     = 'y'
                    elif 'center_y' in outer_child.pos_hint:
                        offset[1]   = instance.size[1]*outer_child.pos_hint['center_y'] + outer_child.size[1]*0.5
                        pos_key     = 'center_y'
                    elif 'top' in outer_child.pos_hint:
                        offset[1]   = instance.size[1]*(1 - outer_child.pos_hint['top'])
                        pos_key     = 'top'

                    outer_child.pos = [pos[0] + offset[0],
                                       pos[1] + offset[1]]

            label_loop_depth    = 0
            def on_label_pos(instance, pos):
                nonlocal label_loop_depth
                if label_loop_depth > 0:
                    return
                
                import math
                debug_angle     = 90
                origin          = [0,0]

                # With rotation (q)A(q^-1), calculate (q^-1)
                delta_theta     = debug_angle*math.pi/180
                theta           = math.atan2(pos[1], pos[0]) - delta_theta
                dist            = math.dist(origin, pos)
                center_theta    = math.atan2(instance.center[1], instance.center[0]) - delta_theta
                center_dist     = math.dist(origin, instance.center)

                child_center    = [center_dist*math.cos(center_theta),
                                   center_dist*math.sin(center_theta)]
                child_pos       = [dist*math.cos(theta),
                                   dist*math.sin(theta)]

                label_loop_depth    += 1
                instance.center      = child_center
                label_loop_depth    -= 1

                instance.canvas.before.clear()
                instance.canvas.after.clear()
                with instance.canvas.before:
                    PushMatrix()
                    Rotate(angle=debug_angle, center=instance.center)
                with instance.canvas.after:
                    PopMatrix()

                on_btn_image_pos(instance, child_pos)

            opt_button_image.bind(size=on_btn_image_size)
            opt_button_image.bind(pos=on_btn_image_pos)
            child.bind(pos=on_label_pos)
            opt_button_image.add_widget(child)

        opt_button_image_factory(opt_button_image, rotated_layout)

        # ==========================================
        #            Rest of the layout
        # ==========================================
        
        remain_off_x    = 0.0
        remain_width    = 1 - (rot_width + remain_off_x)
        content_layout  = RelativeLayout(
            size_hint   = [remain_width, 1],
            pos_hint    = {'x': (rot_width + remain_off_x), 'y': 0}
        )

        description_label   = Label(
            size_hint       = [1, 0.4],
            font_name       = cfg.font_name,
            halign          = 'center',
            color           = (0, 0, 0, 1)
        )

        image_widget_layout = FloatLayout(
            size_hint       = [1, 0.7],
            pos_hint        = {'x': 0, 'y': 0.3}
        )

        def content_layout_factory(label, layout):
            def on_label_size(instance, size):
                instance.text_size  = [size[0]*0.95, size[1]*0.95]
                instance.font_size  = 0.28*size[1]

            label.bind(size=on_label_size)

            # ==========================================
            #            Image Widget Layout
            # ==========================================
            for j in range(3):
                center_x        = 1.0 - (3*j + 2)*0.1
                layout_widget   = RoutineWidgetLayout(
                    size_hint   = [0.08, 0.8],
                    pos_hint    = {'center_x': center_x, 'center_y': 0.5}
                )
                layout.add_widget(layout_widget)

        content_layout_factory(description_label, image_widget_layout)
        content_layout.add_widget(image_widget_layout)
        content_layout.add_widget(description_label)

        opt_button_image.add_widget(content_layout)

        # ==========================================
        #      Add the child widgets to button
        # ==========================================

        # ==========================================
        #       Add button to option layout.
        # ==========================================
        option_layout.add_widget(opt_button)

    return option_layout

def page_recipe(manager: ScreenManager):
    app_layout      = FloatLayout()
    app_bg          = Image(source=cfg.user_page, fit_mode = "fill")

    #   =======================================
    #       Top Widget Layout (quasi-button)
    #   =======================================

    title_widget    = QuasiButtonLabel(
        text        = 'READY-MADE ROUTINE',
        size_hint   = [0.50, 0.10],
        pos_hint    = {'center_x': 0.72, 'y': 0.88},
        font_name   = cfg.font_name,
    )

    def pass_list():
        home.app_data['exercise_list']  = _routine_list[_routine_choice]

    back_button     = home.HomePage.new_trans_button(manager, 3)
    start_button    = home.HomePage.new_trans_button(manager, 6, False, callback=pass_list)

    global _start_button
    start_button.text       = 'START'
    start_button.pos_hint   = {
        'center_x': 0.85,
        'center_y': start_button.pos_hint['center_y']
    }
    start_button.disabled   = True
    _start_button           = start_button

    app_layout.add_widget(app_bg)
    app_layout.add_widget(title_widget)
    app_layout.add_widget(back_button)
    app_layout.add_widget(start_button)
    app_layout.add_widget(option_recipe(manager))
    return app_layout

class RoutineOptionHandler:
    def get_option_description(index: int):
        '''
        Returns the description for the routine option.
        Acceptable values:
        - index -> {0, 1}
        - desc -> *
        '''
        btn_image       = _routine_options[index]
        label           = btn_image.children[0].children[0]
        return label.text
    
    def set_option_description(index: int, desc: str):
        '''
        Updates the description for the routine option.
        Acceptable values:
        - index -> {0, 1}
        - desc -> *
        '''
        btn_image       = _routine_options[index]
        label           = btn_image.children[0].children[0]
        label.text      = desc

    def get_option_widget_root(index: int) -> FloatLayout:
        '''
        Returns the widget root of the 3 custom
        RoutineWidgetLayout objects if you need
        direct access to the root for caching.

        Acceptable values:
        - index -> {0, 1}
        '''
        btn_image       = _routine_options[index]
        return btn_image.children[0].children[1]

    def get_option_widget(index: int, widget_index: int) -> RoutineWidgetLayout:
        '''
        Acceptable values for the parameters are the following:
        - index -> {0, 1}
        - widget_index -> {0, 1, 2}
        '''
        btn_image       = _routine_options[index]
        return btn_image.children[0].children[1].children[widget_index]
    
def load_exercises(exer_list, exer_desc_list):
    from exercise_class import BaseExercise

    global _routine_list
    _routine_list   = exer_list
    for i in range(len(_routine_list)):
        widget_root     = RoutineOptionHandler.get_option_widget_root(i)
        inner_list      = _routine_list[i]
        for j in range(len(inner_list)):
            base_exercise: BaseExercise         = inner_list[j]
            option_widget: RoutineWidgetLayout  = widget_root.children[j]
            option_widget.set_reps(base_exercise.reps)
            option_widget.set_nsets(base_exercise.sets)
            option_widget.set_image_source(base_exercise.img_path)

    for i in range(len(exer_desc_list)):
        RoutineOptionHandler.set_option_description(i, exer_desc_list[i])