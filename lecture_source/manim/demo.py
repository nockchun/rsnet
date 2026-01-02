from manim import *

class hello(Scene):
    def construct(self):
        t = Tex("English... Only...")
        self.play(Write(t))

        circ = Circle(radius=2.4, color=RED)
        self.play(Create(circ))

        self.wait(3)
