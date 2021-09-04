from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.uix.image import Image
from kivy.clock import Clock

class Pipe(Widget):

    gap_size = NumericProperty(60)
    cap_size = NumericProperty(20)
    pipe_c = NumericProperty(0)
    bottom_b_p = NumericProperty(0)
    bottom_c_p = NumericProperty(0)
    top_b_p = NumericProperty(0)
    top_c_p = NumericProperty(0)

    #Texture
    pipe_body_tex = ObjectProperty(None)
    lower_pipe_tex_coords = ListProperty((0, 0, 1, 0, 1, 1, 0, 1))
    top_pipe_tex_coords = ListProperty((0, 0, 1, 0, 1, 1, 0, 1))


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pipe_body_tex = Image(source = "pipe_body.png").texture
        self.pipe_body_tex.wrap = 'repeat'

    def on_size(self, *args):
        lower_b_s = self.bottom_c_p - self.bottom_b_p
        
        self.lower_pipe_tex_coords[5] = lower_b_s/20.0
        self.lower_pipe_tex_coords[7] = lower_b_s/20.0

        top_b_s = self.top - self.top_b_p

        self.top_pipe_tex_coords[5] = top_b_s / 20.0
        self.top_pipe_tex_coords[7] = top_b_s / 20.0

    def on_pipe_c(self, *args):
        Clock.schedule_once(self.on_size, 0)
