from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.uix.widget import Widget
from fitquest_kivy_widgets import BackgroundLabel, ImageButton

import kivy_homepage as home
import kivy_config as cfg

_config             = {
    'index_to_rep'  : 5,
}

_data           = {
    'select'    : {
        'exercise'  : "",
        'reps'      : -1,
        'sets'      : -1,
    },
    'list'      : [],
}

_widgets        = {
    'start'     : None,
    'insert'    : None
}

def _update_insert_btn_state(_dict: dict = None):
    _dict                   = ((_dict is None) and _data['select']) or _dict
    insert_button: Button   = _widgets['insert']
    if (insert_button is None):
        return
    
    if ((_dict['exercise'] != '') and
        (_dict['reps'] != -1) and
        (_dict['sets'] != -1) and 
        (insert_button.get_disabled())):

        insert_button.set_disabled(False)

    elif ((_dict['exercise'] == '') and
          (_dict['reps'] == -1) and
          (_dict['sets'] == -1) and 
          (not insert_button.get_disabled())):

        insert_button.set_disabled(False)

def _clear_selection_data(_dict: dict = _data["select"]):
    _dict['exercise']   = ""
    _dict['reps']       = -1
    _dict['reps']       = -1
    _update_insert_btn_state(_dict)
    
class FQScrollLayout(FloatLayout):
    def __init__(self, **kwargs):
        '''
        This constructor function expects at least two parameters:
        - size_hint = [float, float]
        - pos_hint  = dict{<str>: float}
        '''
        super(FQScrollLayout, self).__init__(**kwargs)

        self._top_label     = BackgroundLabel(
            size_hint       = [1.0, 0.25],
            pos_hint        = {'center_x': 0.5, 'y': 0.75},
            halign          = 'center'
        )

        self._bot_label = BackgroundLabel(
            size_hint   = [1.0, 1.0],
            pos_hint    = {'center_x': 0.5, 'y': 0.0}
        )

        self._top_label.change_bg_color((80/255, 0, 136/255, 1))
        self._top_label.change_color((1, 1, 1, 1))
        self._top_label.set_font_size(False, 0.20)
        self._top_label.set_bg_radius((20, 20, 2, 2))

        self._bot_label.change_bg_color((1, 1, 1, 1))
        self._bot_label.set_bg_radius((20, 20, 20, 20))

        #   ==================================================
        #           Top and Bottom Backgrounds added,
        #           Add the ScrollView widget.
        #   ==================================================
        self._scroll        = ScrollView(
            size_hint       = [0.80, 0.75],
            pos_hint        = {'center_x': 0.5, 'center_y': 0.40}
        )

        self._scroll_grid   = GridLayout(
            size_hint       = [1.0, None],
            pos_hint        = {'x': 0.0},
            spacing         = 20,
        )

        self.add_widget(self._bot_label)
        self.add_widget(self._top_label)

        self._bot_label.add_widget(self._scroll)
        self._scroll.add_widget(self._scroll_grid)

    def set_top_text(self, text: str):
        self._top_label.text        = text

    def set_top_text_scale(self, text_scale: float):
        self._top_label: BackgroundLabel
        self._top_label.set_font_size(False, text_scale)

    def set_grid_cols(self, cols: int | None):
        self._scroll_grid.cols      = cols

    def set_grid_rows(self, rows: int | None):
        self._scroll_grid.rows      = rows

    def set_grid_spacing(self, spacing: float):
        self._scroll_grid.spacing   = spacing

    def set_grid_min_height(self, height: float | None):
        height                      = (((height is None) and self._scroll_grid.minimum_height)
                                      or height)
        self._scroll_grid.height    = height

    def get_top_text(self) -> str:
        return self._top_label.text

    def get_top_text_scale(self) -> float:
        return self._top_label.get_font_size(False)

    def get_grid_cols(self) -> int:
        return self._scroll_grid.cols

    def get_grid_rows(self) -> int:
        return self._scroll_grid.rows

    def get_grid_spacing(self) -> float:
        return self._scroll_grid.spacing
    
    def get_scroll(self) -> ScrollView:
        return self._scroll
    
    #   ========================================
    #           Event Dispatch methods
    #   ========================================
    def on_size(self, instance, size):
        self._top_label.size        = [size[0]*self._top_label.size_hint[0],
                                       size[1]*self._top_label.size_hint[1]]
        self._bot_label.size        = [size[0]*self._bot_label.size_hint[0],
                                       size[1]*self._bot_label.size_hint[1]]
        self._bot_label.size        = [size[0]*self._bot_label.size_hint[0],
                                       size[1]*self._bot_label.size_hint[1]]

        self._scroll.size           = [self._bot_label.size[0]*self._scroll.size_hint[0],
                                       self._bot_label.size[1]*self._scroll.size_hint[1]]

        self._scroll_grid.height    = self._scroll_grid.minimum_height
        self._scroll_grid.width     = self._scroll_grid.minimum_width

    def on_pos(self, instance, pos):
        self._top_label.pos         = pos
        self._bot_label.pos         = pos
        # Calculate scroll offset
        scroll_center_x             = pos[0] + self._bot_label.size[0]*(self._scroll.pos_hint['center_x'])
        scroll_center_x            -= self._scroll.size[0]*0.5
        scroll_center_y             = pos[1] + self._bot_label.size[1]*(self._scroll.pos_hint['center_y'])
        scroll_center_y            -= self._scroll.size[1]*0.5
        # Final positions calculated, apply translation.
        self._scroll.pos            = [scroll_center_x, scroll_center_y]

    def add_grid_widget(self, widget: Widget):
        self._scroll_grid.add_widget(widget)

    def clear_grid_widgets(self):
        self._scroll_grid.clear_widgets()

class FQExerciseCabaret(FloatLayout):
    def __init__(self, **kwargs):
        super(FQExerciseCabaret, self).__init__(**kwargs)

        self.bg             = BackgroundLabel(
            size_hint       = [1.0, 1.0],
            pos_hint        = {'x': 0.0, 'y': 0.0}
        )
        self.button             = Button(
            size_hint           = [1.0, 1.0],
            pos_hint            = {'x': 0.0, 'y': 0.0},
            background_normal   = "",
            background_color    = (0, 0, 0, 0),
        )
        self.bg.change_bg_color((172/255, 48/255, 1, 1))

        self.exer_image         = Image(
            size_hint           = [0.45, 0.525],
            pos_hint            = {'x': 0.65, 'center_y': 0.50},
            opacity             = 0
        )

        self.reps_label         = Label(
            text                = "Reps: ",
            size_hint           = [0.70, 0.075],
            pos_hint            = {'x': -0.12, 'center_y': 0.65},
        )
        self.sets_label         = Label(
            text                = "Sets: ",
            size_hint           = [0.70, 0.075],
            pos_hint            = {'x': -0.12, 'center_y': 0.45},
        )
        self.exer_label         = Label(
            text                = "Exercise: ",
            size_hint           = [0.70, 0.075],
            pos_hint            = {'x': 0.05, 'center_y': 0.25},
        )

        self.add_widget(self.button)
        self.add_widget(self.bg)
        self.add_widget(self.reps_label)
        self.add_widget(self.sets_label)
        self.add_widget(self.exer_label)
        self.add_widget(self.exer_image)

    #   =========================================
    #           Event dispatch methods
    #   =========================================
    def on_size(self, instance, size):
        for child in instance.children:
            child.size    = [size[0]*child.size_hint[0],
                             size[1]*child.size_hint[1]]

    def on_pos(self, instance: Widget, pos):
        for child in instance.children:
            target_pos      = pos[:]
            if 'x' in child.pos_hint:
                target_pos[0]   += self.size[0]*child.pos_hint['x']
            elif 'center_x' in child.pos_hint:
                target_pos[0]   += self.size[0]*child.pos_hint['center_x']
                target_pos[0]   -= child.size[0]*0.5
            elif 'right' in child.pos_hint:
                target_pos[0]   += self.size[0]*child.pos_hint['right']
                target_pos[0]   -= child.size[0]

            if 'y' in child.pos_hint:
                target_pos[1]   += self.size[1]*child.pos_hint['y']
            elif 'center_y' in child.pos_hint:
                target_pos[1]   += self.size[1]*child.pos_hint['center_y']
                target_pos[1]   -= child.size[1]*0.5
            elif 'top' in child.pos_hint:
                target_pos[1]   += self.size[1]*child.pos_hint['top']
                target_pos[1]   -= child.size[1]

            child.pos       = target_pos

    #   =========================================
    #                   Public API
    #   =========================================
    def get_reps(self) -> int:
        '''
        Returns the number of reps for this particular exercise
        widget
        '''
        return int(self.reps_label.text[6:])

    def set_reps(self, value: int):
        self.reps_label.text    = 'Reps: ' + str(value)

    def get_nsets(self) -> int:
        '''
        Returns the number of sets for this particular exercise
        widget
        '''
        return int(self.sets_label.text[6:])

    def set_nsets(self, value: int):
        self.sets_label.text    = 'Sets: ' + str(value)

    def get_exercise(self) -> str:
        '''
        Returns the exercise to be performed for this widget
        '''
        return self.exer_label.text[10:]

    def set_exercise(self, exer: str):
        '''
        Sets the exercise to be performed for this widget
        '''
        self.exer_label.text    = 'Exercise: ' + str(exer)

    def get_exercise_img(self) -> str:
        return self.exer_image.source

    def set_exercise_img(self, image: str|None = ''):
        if ((self.exer_image.source == None) and (image != '')):
            self.exer_image.opacity = 1

        elif ((self.exer_image.source != None) and (image == '')):
            self.exer_image.opacity = 0

        self.exer_image.source  = image

def exercise_recipe(manager: ScreenManager):
    exer_layout             = FQScrollLayout(
        size_hint           = [0.24, 0.56],
        pos_hint            = {'center_x': 0.20, 'center_y': 0.49},
    )
    exer_layout.set_grid_cols(2)
    exer_layout.set_grid_spacing(20)
    exer_layout.set_top_text("EXERCISES:")

    scroll                          = exer_layout.get_scroll()
    scroll.pos_hint['center_y']     = 0.388
    scroll.size_hint[1]             = 0.64

    iterable_i          = -1

    from exercise_class import exercise_dict, ExerciseTemplate
    for key, exercise in exercise_dict().items():
        exercise: ExerciseTemplate
        iterable_i     += 1

        widget                  = ImageButton(
            size_hint           = [0.80, None],
            background_color    = (144/255, 80/255, 192/255, 1),
        )
        widget.data             = key
        widget.set_image_source(exercise.img_path)

        def on_btn_factory(widget):
            def on_btn_click(instance):
                _data['select']['exercise'] = widget.data
                _update_insert_btn_state()

            widget.bind(on_release=on_btn_click)
        
        on_btn_factory(widget)
        exer_layout.add_grid_widget(widget)

    return exer_layout

def reps_recipe(manager: ScreenManager):
    reps_layout    = FQScrollLayout(
        size_hint   = [0.24, 0.40],
        pos_hint    = {'center_x': 0.50, 'center_y': 0.672}
    )
    reps_layout.set_top_text("Reps:")
    reps_layout.set_top_text_scale(0.16)
    reps_layout.set_grid_cols(4)

    scroll                          = reps_layout.get_scroll()
    scroll.pos_hint['center_y']     = 0.38
    scroll.size_hint_y              = 0.60

    def make_reps_widgets(reps_layout: ScrollView):
        from exercise_class import exercise_dict, ExerciseTemplate

        # ==================================
        #       Configurable section
        # ==================================
        _widget_count       = 12

        iterable_i          = 0
        def reps_callback_factory(widget: Button, index: int, font_scale: float = 0.20):
            def reps_callback(instance):
                global _data
                _data['select']['reps'] = index
                _update_insert_btn_state()


            def on_size(instance, size):
                instance.font_size  = font_scale*size[0]

            widget.bind(on_release  = reps_callback)
            widget.bind(size        = on_size)

        for i in range(1, _widget_count + 1):
            widget                  = Button(
                text                = str(_config['index_to_rep']*i),
                size_hint           = [0.25, None],
                background_normal   = "",
                background_color    = (192/255, 128/255, 1, 1),
                font_name           = cfg.font_name,
            )
            reps_callback_factory(widget, i, 0.48)
            
            reps_layout.add_grid_widget(widget)

    make_reps_widgets(reps_layout)
    return reps_layout

def sets_recipe(manager: ScreenManager):
    sets_layout     = FQScrollLayout(
        size_hint   = [0.24, 0.32],
        pos_hint    = {'center_x': 0.50, 'center_y': 0.282}
    )
    sets_layout.set_top_text("SETS:")
    sets_layout.set_grid_cols(4)
    sets_layout.get_scroll().pos_hint       = {
        'center_x'  : 0.50,
        'center_y'  : 0.35,
    }
    sets_layout.get_scroll().size_hint_y    = 0.50
    
    scroll                          = sets_layout.get_scroll()
    # scroll.pos_hint['center_y']     = 0.38
    # scroll.size_hint_y              = 0.60

    def make_sets_widgets(sets_layout: ScrollView):
        # ==================================
        #       Configurable section
        # ==================================
        _widget_count       = 4

        iterable_i          = 0
        def sets_callback_factory(widget: Button, index: int, font_scale: float = 0.20):
            def sets_callback(instance):
                global _data
                _data['select']['sets'] = index
                _update_insert_btn_state()

            def on_size(instance, size):
                instance.font_size  = font_scale*size[0]

            widget.bind(on_release  = sets_callback)
            widget.bind(size        = on_size)

        for i in range(1, _widget_count + 1):
            widget                  = Button(
                text                = str(i),
                size_hint           = [0.25, None],
                background_normal   = "",
                background_color    = (192/255, 128/255, 1, 1),
                font_name           = cfg.font_name,
            )
            sets_callback_factory(widget, i, 0.48)
            
            sets_layout.add_grid_widget(widget)

    make_sets_widgets(sets_layout)
    return sets_layout

def exercise_list_recipe(manager: ScreenManager):
    exer_layout             = FQScrollLayout(
        size_hint           = [0.24, 0.56],
        pos_hint            = {'center_x': 0.80, 'center_y': 0.49},
    )
    exer_layout.set_grid_cols(1)
    exer_layout.set_grid_spacing(20)
    exer_layout.set_top_text("LIST OF EXERCISES:")
    exer_layout.set_top_text_scale(0.12)

    #   Create button for inserting exercise elements
    insert_button                   = Button(
        text                        = "Insert",
        color                       = (0, 0, 0, 1),
        background_color            = (0.75, 0.75, 0.75, 1),
        background_normal           = "",
        size_hint                   = [1.00, 0.07],
        pos_hint                    = {
            'center_x' : 0.50,
            'center_y' : 0.716,
        },
        font_name                   = cfg.font_name,
        font_size                   = 40,
        disabled                    = True,
    )

    def on_routine_insert(instance):
        if ((_data['select']['exercise'] == '') or 
            (_data['select']['reps'] == -1) or
            (_data['select']['sets'] == -1)):
            #print a toast message not allowing the
            #addition of a new exercise routine.
            return
        
        from exercise_class import Exercise, ExerciseTemplate
        global _widgets

        exercise            = Exercise.copy(ExerciseTemplate.get_exercise(_data['select']['exercise']))
        exercise.reps       = _data['select']['reps']*_config['index_to_rep']
        exercise.sets       = _data['select']['sets']
        exercise.duration   = exercise.duration * exercise.reps / exercise._base.reps
        _data['list'].append(exercise)

        if (len(_data['list']) == 1):
            start_button: Button    = _widgets['start']
            start_button.set_disabled(False)

        # Add a new widget.
        widget                      = FQExerciseCabaret(
            size_hint               = [0.80, None],
        )

        widget.set_exercise_img(exercise.img_path)
        widget.set_exercise(exercise.exer_name)
        widget.set_reps(exercise.reps)
        widget.set_nsets(exercise.sets)
        
        # _data['select']['exercise']
        # _data['select']['reps']
        # _data['select']['sets']

        # Add the widget to the exercise layout.
        exer_layout.add_grid_widget(widget)

    insert_button.bind(on_release   = on_routine_insert)
    _widgets['insert']              = insert_button


    scroll                          = exer_layout.get_scroll()
    scroll.pos_hint['center_y']     = 0.336
    scroll.size_hint[1]             = 0.560

    iterable_i                      = -1
    # from exercise_class import exercise_dict, ExerciseTemplate
    # for key, exercise in exercise_dict().items():
    #     exercise: ExerciseTemplate
    #     iterable_i     += 1

    #     widget                  = ImageButton(
    #         size_hint           = [0.80, None],
    #         background_color    = (144/255, 80/255, 192/255, 1),
    #     )
    #     widget.data             = key
    #     widget.set_image_source(exercise.img_path)

    #     def on_btn_factory(widget):
    #         def on_btn_click(instance):
    #             _data['select']['exercise'] = widget.data

    #         widget.bind(on_release=on_btn_click)
        
    #     on_btn_factory(widget)
    #     exer_layout.add_grid_widget(widget)

    exer_layout.add_widget(insert_button)
    return exer_layout

def page_recipe(manager: ScreenManager):
    app_layout                  = FloatLayout()
    app_bg                      = Image(source=cfg.user_page, fit_mode = "fill")

    #   Back button
    back_button                 = home.HomePage.new_trans_button(manager, 3)
    exer_list  : FQScrollLayout = None

    #   Start button send data
    def on_start_send():
        home.app_data['exercise_list']  = _data['list']
        nonlocal exer_list
        exer_list.clear_grid_widgets()

    #   Start button
    start_button            = home.HomePage.new_trans_button(manager, 6, callback=on_start_send)
    start_button.text       = 'START'
    start_button.pos_hint   = {'center_x': 0.86, 'center_y': 0.12}
    start_button.set_disabled(True)

    global _widgets
    _widgets['start']       = start_button

    app_layout.add_widget(app_bg)
    app_layout.add_widget(back_button)
    app_layout.add_widget(start_button)
    app_layout.add_widget(exercise_recipe(manager))
    app_layout.add_widget(reps_recipe(manager))
    app_layout.add_widget(sets_recipe(manager))

    exer_list               = exercise_list_recipe(manager)
    app_layout.add_widget(exer_list)
    return app_layout