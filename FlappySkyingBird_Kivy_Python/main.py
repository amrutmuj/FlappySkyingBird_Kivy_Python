from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from pipe import Pipe
from random import randint


class Background(Widget):
    cloud_texture = ObjectProperty(None)
    floor_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cloud_texture = Image(source="cloud.png").texture
        self.cloud_texture.wrap = 'repeat'
        self.cloud_texture.uvsize = (Window.width / self.cloud_texture.width, -1)

        self.floor_texture = Image(source="floor.png").texture
        self.floor_texture.wrap = 'repeat'
        self.floor_texture.uvsize = (Window.width / self.floor_texture.width, -1)

    def scroll_textures(self, time_passed):
        self.cloud_texture.uvpos = ((self.cloud_texture.uvpos[0] - time_passed/2.0), self.cloud_texture.uvpos[1])
        self.floor_texture.uvpos = ((self.floor_texture.uvpos[0] - time_passed/1.0), self.floor_texture.uvpos[1])
        texture = self.property('cloud_texture')
        texture_floor = self.property('floor_texture')
        texture_floor.dispatch(self)
        texture.dispatch(self)

class Bird(Image):
    velocity = NumericProperty(0)

    def on_touch_down(self, touch):
        self.source = "bird2.png"
        self.velocity = 150
        super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.source = "bird1.png"
        super().on_touch_up(touch)


class MainApp(App):
    pipes = []
    GRAVITY = 300

    def on_start(self):
        Clock.schedule_interval(self.root.ids.background.scroll_textures, 1/2000)

    def move_bird(self, time_passed):
        bird = self.root.ids.bird
        bird.y = bird.y + bird.velocity * time_passed
        bird.velocity = bird.velocity - self.GRAVITY * time_passed

    def start_game(self):
        Clock.schedule_interval(self.move_bird, 1 / 2000)

        #creating no of pipes
        num_pipes = 5
        dis_btw_pipes = Window.width / (num_pipes - 1)
        for i in range(num_pipes):
            pipe = Pipe()
            pipe.pipe_c = randint(96 + 80, self.root.height - 100)
            pipe.size_hint = (None, None)
            pipe.pos = (i*dis_btw_pipes, 96)
            pipe.size = (64, self.root.height - 96)

            self.pipes.append(pipe)
            self.root.add_widget(pipe)

        #Move Pipes
        Clock.schedule_interval(self.move_pipes, 1/100.)

    def move_pipes(self, time_passed):
        num_pipes = 5
        dis_btw_pipes = Window.width / (num_pipes - 1)
        #Move the pipe
        for pipe in self.pipes:
            pipe.x -= time_passed * 50

        #Repostioning of Pipe
        pipe_xs = list(map(lambda pipe: pipe.x, self.pipes))
        right_m_x = max(pipe_xs)
        if right_m_x <= Window.width - dis_btw_pipes:
            most_l_p = self.pipes[pipe_xs.index(min(pipe_xs))]
            most_l_p.x = Window.width

MainApp().run()
