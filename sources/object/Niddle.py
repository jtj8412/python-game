import pygame
from sources.Object import *


class Niddle(Object):

    power = 1000
    damage = 150
    mode = None

    @staticmethod
    def Init():
        Object.AddImage_("imgs/trap/niddle.png", "Niddle1")
        Object.AddImage_("imgs/trap/niddle2.png", "Niddle2")

    def __init__(self):
        super().__init__()
        self.AddSprite("Niddle1", "Default1")
        self.AddSprite("Niddle2", "Default2")
        self.SetRect([275, 140])
        self.SetPivot([50, 100])
        self.SetMass(10)
        self.SetLayer(Layer.BackObject)
        self.SpeedX(-Value.game_speed)
        self.SetTag("Niddle")
        self.SetYpos(Value.SCREEN_SIZE[1] - 130)
        self.SetScale("Default1", [0.9, 0.8])
        self.SetScale("Default2", [0.9, 0.8])

    def Start(self):
        self.SetSpeed([-Value.game_speed, 0])
        if random.randrange(0, 4) == 0:
            self.mode = 1
        else:
            self.mode = 0

    def Collision(self, obj):
        if obj.GetTag() != "Player":
            return
        if obj.IsDamaged():
            return

        head = self.GetYpos() - self.GetRectY() * (self.GetPivotY() / 100) + self.GetRectOffsetY()
        if obj.GetYpos() - 1 < head:
            obj.SpeedY(-self.power)
            obj.SetState("Jump2")
            obj.Damaged()
            ObjectManager.FindObject("HP").Damage(self.damage)

    def Update(self):
        if self.GetRight() < 0 or self.GetBottom() < 0:
            self.Disable()

        if self.mode == 1:
            if self.GetXpos() < Player.base_xPos + 400:
                self.SetSpeed([-Value.game_speed, -1400])

    def GetWidth(self):
        return Value.pixel * 3

    def SetNum(self, num):
        if num == 1:
            self.SetRect([90, 145])
            self.SetState("Default2")
            self.SetXpos(Value.GetSummonXpos() + Value.pixel * 0.5)
            obj = ObjectManager.FindDisabled("Star")
            obj.SetXpos(self.GetXpos())
            obj.SetYpos(self.GetYpos() - 210)
            obj = ObjectManager.FindDisabled("Bottom")
            obj.SetXpos(self.GetXpos() - Value.pixel * 0.5)
        elif num == 3:
            self.SetRect([275, 145])
            self.SetState("Default1")
            self.SetXpos(Value.GetSummonXpos() + Value.pixel * 1.5)
            for i in range(3):
                ObjectManager.FindDisabled("Bottom").SetXpos(self.GetXpos() - Value.pixel + (1.5 - i * 1) * Value.pixel)
            for i in range(2):
                obj = ObjectManager.FindDisabled("Star")
                obj.SetXpos(self.GetXpos() - (i + 0.65) * (obj.GetRectX() + 18))
                obj.SetYpos(self.GetYpos() - 210 + i * 30)
            for i in range(2):
                obj = ObjectManager.FindDisabled("Star")
                obj.SetXpos(self.GetXpos() + (i + 0.65) * (obj.GetRectX() + 18))
                obj.SetYpos(self.GetYpos() - 210 + i * 30)
