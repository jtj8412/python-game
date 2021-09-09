
import pygame
from sources.Object import *


class Prize(Object):

    ZOOM = 2
    zoom = 0
    reduce = 0.98
    mode = None

    @staticmethod
    def Init():
        Object.AddImage_("imgs/prize/1.png", "Prize1")
        Object.AddImage_("imgs/prize/2.png", "Prize2")
        Object.AddImage_("imgs/prize/3.png", "Prize3")
        Object.AddImage_("imgs/prize/4.png", "Prize4")
        Object.AddImage_("imgs/prize/5.png", "Prize5")
        Object.AddImage_("imgs/prize/6.png", "Prize6")
        Object.AddImage_("imgs/prize/7.png", "Prize7")

    def __init__(self):
        super().__init__()
        self.AddSprite("Prize1", "Default1")
        self.AddSprite("Prize2", "Default2")
        self.AddSprite("Prize3", "Default3")
        self.AddSprite("Prize4", "Default4")
        self.AddSprite("Prize5", "Default5")
        self.AddSprite("Prize6", "Default6")
        self.AddSprite("Prize7", "Default7")
        self.SetLayer(Layer.UI)
        self.SetTag("Prize")
        self.SetPivot([50, 100])
        self.SetTriggerOn()

    def Start(self):
        self.zoom = self.ZOOM
        self.SetPos([Value.SCREEN_SIZE[0] / 2, -100])
        self.mode = 7 - int(Memory.current_score / 40000)
        if self.mode > 7:
            self.mode = 7
        self.SetState("Default" + str(self.mode))
        self.SpeedY(950)

    def Physics(self):
        super().Physics()
        if self.GetYpos() > Value.SCREEN_SIZE[1] / 2 - 30:
            self.SetSpeedY(0)






