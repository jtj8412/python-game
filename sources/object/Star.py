
import pygame
import random
from sources.Object import *


class Star(Object):

    @staticmethod
    def Init():
        Object.AddImage_("imgs/star/1.png", "Star_Ani1")
        Object.AddImage_("imgs/star/2.png", "Star_Ani2")
        Object.AddImage_("imgs/star/3.png", "Star_Ani3")
        Object.AddImage_("imgs/star/4.png", "Star_Ani4")
        Object.AddImage_("imgs/star/effect1.png", "Star_Effect1")
        Object.AddImage_("imgs/star/effect2.png", "Star_Effect2")
        Object.AddImage_("imgs/star/effect3.png", "Star_Effect3")
        Object.AddImage_("imgs/star/effect4.png", "Star_Effect4")
        Object.AddImage_("imgs/star/effect5.png", "Star_Effect5")
        Object.AddImage_("imgs/star/effect6.png", "Star_Effect6")
        Object.sounds.update({"Star": pygame.mixer.Sound("sounds/star.wav")})
        Object.sounds["Star"].set_volume(1)

    def __init__(self):
        super().__init__()
        self.AddSprite("Star_Ani1", "Default")
        self.AddSprite("Star_Ani2", "Default")
        self.AddSprite("Star_Ani3", "Default")
        self.AddSprite("Star_Ani4", "Default")
        self.AddSprite("Star_Effect1", "Effect")
        self.AddSprite("Star_Effect2", "Effect")
        self.AddSprite("Star_Effect3", "Effect")
        self.AddSprite("Star_Effect4", "Effect")
        self.AddSprite("Star_Effect5", "Effect")
        self.AddSprite("Star_Effect6", "Effect")
        self.SetScale("Effect", [0.3, 0.3])
        self.SetTriggerOn()
        self.SetRect([70, 70])
        self.SpeedX(-Value.game_speed)
        self.SetTag("Star")
        self.SetSpriteDuration("Default", 0.5)
        self.SetSpriteDuration("Effect", 0.3)

    def Start(self):
        self.SetState("Default")
        self.SetXpos(Value.GetSummonXpos() + self.GetRectX())
        self.SetYpos(480)

    def Update(self):
        if (self.GetState() == "Effect" and self.IsStateEnd()) or self.GetRight() < 0:
            self.Disable()

    def Collision(self, obj):
        if self.GetState() == "Default" and obj.GetTag() == "Player":
            self.SetState("Effect")
            Object.sounds["Star"].play()




