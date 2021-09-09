
import pygame
from sources.Object import *


class HP(Object):

    @staticmethod
    def Init():
        Object.AddImage_("imgs/UI/hp.png", "HP")
        Object.sounds.update({"Gameover": pygame.mixer.Sound("sounds/gameover.wav")})

    def __init__(self):
        super().__init__()
        self.AddSprite("HP", "Default")
        self.SetLayer(Layer.UI)
        self.SetTag("HP")
        self.SetPivot([0, 0])
        self.SetPos([2, 2])
        self.SetSpeedX(-Value.hp_minus)

    def Damage(self, value):
        self.TranslateX(-value)

    def Update(self):
        if self.GetXpos() <= -self.GetSpriteX() and not Value.gameover:
            ObjectManager.AllStop()
            pygame.mixer.music.stop()
            ObjectManager.FindObject("Player").SetState("Stand")
            Memory.Save()
            Object.sounds["Gameover"].play()
            ObjectManager.FindObject("Player").SetStatic()
            Value.gameover = True

    def Render(self, screen):
        super().Render(screen)
        if Value.gameover:
            font = pygame.font.Font('ariblk.ttf', 40)
            surf = font.render("Gameover", True, [255, 255, 255])
            rect = surf.get_rect()
            rect.center = (Value.SCREEN_SIZE[0] / 2, Value.SCREEN_SIZE[1] / 2)
            screen.blit(surf, rect)





