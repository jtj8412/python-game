
import pygame
from sources.Object import *


class Decoration(Object):

    @staticmethod
    def Init():
        Object.AddImage_("imgs/decoration/decoration1.png", "Decoration1")
        Object.AddImage_("imgs/decoration/decoration2.png", "Decoration2")
        Object.AddImage_("imgs/decoration/decoration3.png", "Decoration3")
        Object.AddImage_("imgs/decoration/decoration4.png", "Decoration4")
        Object.AddImage_("imgs/decoration/decoration5.png", "Decoration5")
        Object.AddImage_("imgs/decoration/decoration6.png", "Decoration6")

    def __init__(self):
        super().__init__()
        self.AddSprite("Decoration1", "Default1")
        self.AddSprite("Decoration2", "Default2")
        self.AddSprite("Decoration3", "Default3")
        self.AddSprite("Decoration4", "Default4")
        self.AddSprite("Decoration5", "Default5")
        self.AddSprite("Decoration6", "Default6")
        self.SetPivot([50, 100])
        self.SetStatic()
        self.SetLayer(Layer.Background)
        self.SpeedX(-Value.game_speed)
        self.SetTag("Decoration")
        self.SetScale("Default5", [0.6, 0.6])
        self.SetYpos(590)

    def Start(self):
        rand = random.randrange(1, 7)
        self.SetState("Default" + str(rand))
        self.SetXpos(Value.GetSummonXpos() + Value.pixel * 0.5)

    def Update(self):
        super().Update()
        if self.GetRight() < 0:
            self.Disable()



