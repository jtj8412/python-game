
import pygame
from sources.Object import *


class Bottom(Object):

    @staticmethod
    def Init():
        Object.AddImage_("imgs/bottom/bottom5.png", "Bottom")

    def __init__(self):
        super().__init__()
        self.AddSprite("Bottom", "Default")
        self.SetRect([130, 130])
        self.SetPivot([0, 100])
        self.SetMass(10)
        self.SetLayer(Layer.BackObject)
        self.SpeedX(-Value.game_speed)
        self.SetTag("Bottom")
        self.SetYpos(Value.SCREEN_SIZE[1])

    def Start(self):
        self.SetXpos(Value.GetSummonXpos())

    def Update(self):
        right = self.GetRight()
        if right < 0:
            self.Disable()



