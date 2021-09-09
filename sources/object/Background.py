import pygame
from sources.Object import *


class Background(Object):

    @staticmethod
    def Init():
        Object.AddImage_("imgs/background/background4.png", "Background")

    def __init__(self):
        super().__init__()
        self.AddSprite("Background", "Default")
        self.SetLayer(Layer.Background)
        self.SetTriggerOn()
        self.SetTag("Background")
        self.SetPivot([0, 100])
        self.SetScale("Default", [1.3, 1.5])
        self.SetSpeed([-Value.game_speed / 10, 0])
        self.SetPos([0, Value.SCREEN_SIZE[1]])
        if ObjectManager.FindObjectWithTag("Background"):
            self.TranslateX(self.GetSpriteX())

    def Update(self):
        right = self.GetXpos() + self.GetSpriteX() * ((100 - self.GetPivotX()) / 100) + self.GetRectOffsetX()
        if right < 0:
            self.SetXpos(Value.SCREEN_SIZE[0] + right)

    def Render(self, screen):
        if self.GetXpos() < Value.SCREEN_SIZE[0]:
            super().Render(screen)

