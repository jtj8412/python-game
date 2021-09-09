
import pygame
import random
from sources.Object import *


class Heal(Object):

    time = 0
    move_speed = 150
    heal = 180

    @staticmethod
    def Init():
        Object.AddImage_("imgs/heal/1.png", "Heal1")
        Object.AddImage_("imgs/heal/2.png", "Heal2")
        Object.AddImage_("imgs/heal/3.png", "Heal3")
        Object.sounds.update({"Heal": pygame.mixer.Sound("sounds/heal.ogg")})
        Object.sounds["Heal"].set_volume(1)

    def __init__(self):
        super().__init__()
        self.AddSprite("Heal1", "Default")
        self.AddSprite("Heal2", "Default")
        self.AddSprite("Heal3", "Default")
        self.SetScale("Default", [1.2, 1.2])
        self.SetTriggerOn()
        self.SetRect([60, 60])
        self.SpeedX(-Value.game_speed)
        self.SetTag("Heal")
        self.time = 0

    def Start(self):
        self.SetState("Default")
        self.SetXpos(Value.GetSummonXpos() + self.GetRectX())
        self.SetYpos(random.randrange(220, 430))

    def Update(self):
        self.time += Time.deltaTime
        if self.time < 0.4:
            self.SetSpeedY(-self.move_speed)
        elif 0.4 <= self.time < 0.8:
            self.SetSpeedY(self.move_speed)
        else:
            self.time = self.time - Time.deltaTime

        if self.GetRight() < 0:
            self.Disable()

    def Collision(self, obj):
        if obj.GetTag() == "Player":
            Object.sounds["Heal"].play()
            obj = ObjectManager.FindObject("HP")
            obj.TranslateX(self.heal)
            if obj.GetXpos() > 0:
                obj.SetXpos(0)
            self.Disable()




