from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.graphics import Color, RoundedRectangle, Rotate, PushMatrix, PopMatrix

import kivy_homepage as home
import kivy_config as cfg

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

        def opt_button_factory(opt_button, opt_button_image):
            def on_button_size(instance, size):
                opt_button_image.size   = size

            def on_button_pos(instance, pos):
                opt_button_image.pos   = pos

            opt_button.bind(size=on_button_size)
            opt_button.bind(pos=on_button_pos)

        opt_button_factory(opt_button, opt_button_image)

        # ==========================================
        #       The Three Image Sub-Layouts
        # ==========================================

        # ==========================================
        #               Routine Text
        # ==========================================
        rot_width, rot_off_x    = 0.06096, 0.016
        rotated_layout          = FloatLayout(
            size_hint           = [rot_width, 1.0],
            pos_hint            = {'x': rot_off_x, 'y': 0.0},
        )

        rotated_text            = Label(
            size_hint           = [1, 1],
            font_size           = 48,
            font_name           = cfg.font_name,
            # disabled            = True,
        )

        rotated_text.text   = 'ROUTINE ' + str(i+1)  
        rotated_layout.add_widget(rotated_text)

        def opt_button_image_factory(opt_button_image, child):
            import math
            debug_angle     = 90
            origin          = [0,0]

            def on_button_size(instance, size):
                child.size  = [size[0]*child.size_hint[0],
                               size[1]*child.size_hint[1]]

                if (len(child.children) <= 1):
                    return
                
                for i in range(1, len(child.children)):
                    child.children[i].size  = size

            def on_button_pos(instance, pos):
                # Calculate the center
                start_pos       = [pos[0] + (instance.size[0] - child.size[0])*child.pos_hint['x'],
                                   pos[1] + (instance.size[1] - child.size[1])*child.pos_hint['y']] 
                child.pos       = start_pos

                rot_theta       = debug_angle*math.pi/180.0
                theta           = math.atan2(start_pos[1], start_pos[0]) - rot_theta
                center_theta    = math.atan2(child.size[1], child.size[0]) - rot_theta
                
                center_dist     = math.dist(origin, child.size)/2
                rot_center      = [center_dist*math.cos(center_theta),
                                   center_dist*math.sin(center_theta)]

                dist        = math.dist(origin, start_pos)
                start_pos   = [math.cos(theta)*dist,
                               math.sin(theta)*dist]

                # fin_center  = start_pos + rot_center
                child.children[0].center = [start_pos[0] + rot_center[0],
                                            start_pos[1] + rot_center[1]]

                child.children[0].canvas.before.clear()
                child.children[0].canvas.after.clear()
                with child.children[0].canvas.before:
                    PushMatrix()
                    Rotate(angle=debug_angle, center=child.children[0].center)
                with child.children[0].canvas.after:
                    PopMatrix()

                if (len(child.children) <= 1):
                    return
                
                for i in range(1, len(child.children)):
                    child.children[i].pos   = pos
                    
            opt_button_image.bind(size=on_button_size)
            opt_button_image.bind(pos=on_button_pos)

        opt_button_image_factory(opt_button_image, rotated_layout)

        opt_button_image.add_widget(rotated_layout)

        # ==========================================
        #            Rest of the layout
        # ==========================================
        # remain_width    = 1 - (rot_width + rot_off_x)
        # content_layout  = FloatLayout(
        #     size_hint   = [remain_width, 1],
        #     pos_hint    = {'x': (rot_width + rot_off_x), 'y': 0}
        # )

        # vis_label       = Label(
        #     text        = 'vis label',
        #     pos_hint    = {'center_x': 0.5, 'center_y': 0.5}
        # )
        # desc_label      = Label(
        #     text        = 'desc label',
        #     pos_hint    = {'center_x': 0.5, 'center_y': 0.5}
        # )

        # content_layout.add_widget(vis_label)
        # content_layout.add_widget(desc_label)

        # opt_button_image.add_widget(content_layout, 1)

        # ==========================================
        #      Add the child widgets to button
        # ==========================================
        opt_button.add_widget(opt_button_image)

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

    back_button     = home.HomePage.new_back_button(manager, 3)

    app_layout.add_widget(app_bg)
    app_layout.add_widget(title_widget)
    app_layout.add_widget(back_button)
    app_layout.add_widget(option_recipe(manager))
    return app_layout