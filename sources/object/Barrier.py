
import pygame
from sources.Object import *


class Barrier(Object):

    @staticmethod
    def Init():
        Object.AddImage_("imgs/wall/barrier.png", "Barrier")

    def __init__(self):
        super().__init__()
        self.AddSprite("Barrier", "Default")
        self.SetRect([85, 210])
        self.SetPivot([50, 100])
        self.SetMass(10)
        self.SetLayer(Layer.BackObject)
        self.SpeedX(-Value.game_speed)
        self.SetTag("Barrier")
        self.SetYpos(590)

    def Start(self):
        self.SetXpos(Value.GetSummonXpos() + Value.pixel * 0.5)
        ObjectManager.FindDisabled("Bottom").SetXpos(self.GetXpos() - Value.pixel * 0.5)
        obj = ObjectManager.FindDisabled("Star")
        obj.SetXpos(self.GetXpos())
        obj.SetYpos(self.GetTop() - 50)

    def Update(self):
        super().Update()
        if self.GetRight() < 0:
            self.Disable()


