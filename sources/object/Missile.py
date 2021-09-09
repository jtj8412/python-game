
import pygame
from sources.Object import *


class Missile(Object):

    move_speed = 500
    power = 1500
    damage = 100

    @staticmethod
    def Init():
        Object.AddImage_("imgs/missile/1.png", "Missile_Default1")
        Object.AddImage_("imgs/missile/2.png", "Missile_Default2")
        Object.AddImage_("imgs/missile/effect1.png", "Missile_Effect1")
        Object.AddImage_("imgs/missile/effect2.png", "Missile_Effect2")
        Object.AddImage_("imgs/missile/effect3.png", "Missile_Effect3")

    def __init__(self):
        super().__init__()
        self.AddSprite("Missile_Default1", "Default")
        self.AddSprite("Missile_Default2", "Default")
        self.AddSprite("Missile_Effect1", "Effect")
        self.AddSprite("Missile_Effect2", "Effect")
        self.AddSprite("Missile_Effect3", "Effect")
        self.SetSpriteDuration("Default", 0.08)
        self.SetSpriteDuration("Effect", 0.4)

        self.SetSpeedX(-(Value.game_speed + self.move_speed))
        self.SetScale("Default", [0.8, 0.8])
        self.SetRect([45, 40])
        self.SetPivot([50, 50])
        self.SetRectOffset([-20, 10])
        self.SetTag("Missile")

    def Start(self):
        self.SetState("Default")
        self.SetYpos(random.randrange(300, 550))
        self.SetXpos(Value.GetSummonXpos() + self.GetSpriteX() / 2)

    def Update(self):
        if (self.GetState() == "Effect" and self.IsStateEnd()) or self.GetXpos() < -self.GetSpriteX():
            self.Disable()

    def Collision(self, obj):
        if obj.GetName() != "Player":
            return
        if obj.IsDamaged():
            return

        if self.GetState() == "Default" and obj.GetName() == "Player":
            obj.SetSpeedX(0)
            obj.SpeedX(-self.power)
            self.SetState("Effect")
            obj.Damaged()
            ObjectManager.FindObject("HP").Damage(self.damage)





