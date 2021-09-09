
import pygame
from sources.Object import *


class Wall(Object):

    star = []
    mode = None

    @staticmethod
    def Init():
        Object.AddImage_("imgs/wall/wall2.png", "Wall_Default")

    def __init__(self):
        super().__init__()
        self.AddSprite("Wall_Default", "Default")
        self.SetTag("Wall")
        self.SetSpeedX(-Value.game_speed)
        self.SetLayer(Layer.BackObject)
        self.SetRect([110, 310])
        self.SetMass(9)
        self.SetScale("Default", [1, 0.7])
        self.star = []

    def Start(self):
        for i in range(4):
            self.star.append(ObjectManager.FindDisabled("Star"))
        self.SetXpos(Value.GetSummonXpos() + self.GetRectX() / 2 + Value.pixel * 2.5)
        self.SetYpos(730)
        self.mode = random.randrange(0, 3)
        self.SetSpeed([-Value.game_speed, 0])

    def SetXpos(self, x):
        super().SetXpos(x)
        for i in range(0, 2):
            self.star[i].SetXpos(self.GetXpos() - (i * 90 + 50))
        for i in range(2, 4):
            self.star[i].SetXpos(self.GetXpos() + ((i - 2) * 90 + 50))

    def SetYpos(self, y):
        super().SetYpos(y)
        for i in range(0, 2):
            self.star[i].SetYpos(self.GetTop() - (100 - i * 60))
        for i in range(2, 4):
            self.star[i].SetYpos(self.GetTop() - (100 - (i - 2) * 60))

    def Update(self):
        if self.GetRight() < 0:
            self.Disable()
            self.star.clear()
        if self.GetYpos() <= 500 or self.GetYpos() >= 900:
            self.SetSpeedY(0)

    def Collision(self, obj):
        if obj.GetName() == "Player" and self.GetTop() >= obj.GetBottom() - 1:
            if self.mode == 1:
                if self.GetYpos() > 500:
                    self.SetSpeedY(-400)
            if self.mode == 2:
                if self.GetYpos() < 900:
                    self.SetSpeedY(400)

