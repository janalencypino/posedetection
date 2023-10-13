from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle

import kivy_config as cfg

class BackgroundLabel(Label):
    def __init__(self, **kwargs):
        super(BackgroundLabel, self).__init__(**kwargs)

        self.font_name      = cfg.font_name
        self._font_scale    = -1.0
        self._font_size     = 48
        self.rect_radius    = (0, 0, 0, 0)

        with self.canvas.before:
            self.rect_color = Color(1, 1, 1, 1)
            self.rect       = RoundedRectangle(
                pos         = self.pos,
                size        = self.size,
                radius      = self.rect_radius
            )

    def on_size(self, instance, size):
        self.rect.size      = size
        if (self._font_scale < 0.0):
            instance.font_size  = self._font_size
        else:
            instance.font_size  = self._font_scale*size[0]

    def on_pos(self, instance, pos):
        self.rect.pos       = pos

    def change_color(self,
                     color: (float, float, float, float)
                     = (1, 1, 1, 1)):
        self.color          = color

    def change_bg_color(self,
                        color: (float, float, float, float)
                        = (1, 1, 1, 1)):
        self.rect_color.rgba    = color

    def set_bg_radius(self,
                      radius: (float, float, float, float)
                      = (5, 5, 5, 5)):
        self.rect_radius    = radius
        self.rect.radius    = radius

    def set_font_size(self, fixed: bool = True,
                      new_size: float = 48):
        if (fixed):
            self._font_size     = new_size
        else:
            self._font_scale    = new_size
            self.font_size      = new_size*self.size[0]

    def get_bg_radius(self) -> int:
        return self.rect_radius
    
    def get_font_size(self, fixed: bool = True) -> float:
        return ((fixed) and self._font_size) or self._font_scale
 
class ImageButton(Button):
    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)

        self.background_normal  = ""
        if (not "background_color" in kwargs):
            self.background_color   = (0,0,0,0)
            
        self._on_text_loop      = 0
        self._image             = Image(
            pos                 = self.pos,
            size                = self.size,
            source              = "",
            opacity             = 0,
            fit_mode            = "fill",
        )

        self.add_widget(self._image)

    # Lock text from being updated.
    def on_text(self, instance, text):
        if (self._on_text_loop > 0):
            return
        
        self.text           = ""

    def on_pos(self, instance, pos):
        self._image.pos     = pos

    def on_size(self, instance, size):
        self._image.size    = size

    def set_image_source(self, source):
        self._image.source  = source
        if (self._image.opacity == 0):
            self._image.opacity = 1