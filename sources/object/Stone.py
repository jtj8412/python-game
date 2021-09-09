
import pygame
from sources.Object import *


class Stone(Object):

    move_speed = 125
    power = 3500

    @staticmethod
    def Init():
        Object.AddImage_("imgs/stone/1.png", "Stone_Default1")
        Object.AddImage_("imgs/stone/2.png", "Stone_Default2")
        Object.AddImage_("imgs/stone/3.png", "Stone_Default3")

    def __init__(self):
        super().__init__()
        self.AddSprite("Stone_Default1", "Default")
        self.AddSprite("Stone_Default2", "Default")
        self.AddSprite("Stone_Default3", "Default")
        self.SetRect([210, 180])
        self.SetRectOffset([-50, -30])
        self.SetMass(10)
        self.SetTag("Stone")
        self.SetLayer(Layer.Missile)
        self.SetSpeed([-(Value.game_speed + self.move_speed), 60])

    def Start(self):
        #self.SetPos([1500, 470])
        self.SetPos([1950, 420])

    def Collision(self, obj):
        if obj.GetTag() != "Player":
            return
        if obj.IsDamaged():
            return

        head = self.GetYpos() - self.GetRectY() * (self.GetPivotY() / 100) + self.GetRectOffsetY()
        if obj.GetYpos() - 2 > head and not (self.GetRight() <= obj.GetLeft() + 1):
            obj.SpeedX(-self.power)
            obj.Damaged()
            ObjectManager.FindObject("HP").Damage(300)

    def Update(self):
        if self.GetRight() < -self.GetSpriteX():
            self.Disable()
