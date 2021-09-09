
import pygame
from sources.Object import *
from sources.Memory import *


class Score(Object):

    pygame.font.init()
    font = pygame.font.Font('ariblk.ttf', 20)
    surf1 = font.render("Score : ", True, [255, 255, 255])
    rect1 = None
    surf2 = font.render("HighScore : ", True, [255, 255, 255])
    rect2 = None

    def __init__(self):
        super().__init__()
        self.rect1 = self.surf1.get_rect()
        self.rect2 = self.surf2.get_rect()
        self.rect1.center = (Value.SCREEN_SIZE[0] - 250, 30)
        self.rect2.center = (Value.SCREEN_SIZE[0] - 275, 75)

    def Render(self, screen):
        screen.blit(self.surf1, self.rect1)
        screen.blit(self.surf2, self.rect2)
        surf1 = self.font.render(str(Memory.current_score), True, [255, 255, 255])
        surf2 = self.font.render(str(Memory.high_score), True, [255, 255, 255])
        rect1 = surf1.get_rect()
        rect2 = surf2.get_rect()
        rect1.center = (Value.SCREEN_SIZE[0] - 50, 30)
        rect2.center = (Value.SCREEN_SIZE[0] - 50, 75)
        screen.blit(surf1, rect1)
        screen.blit(surf2, rect2)





