
import pygame
from sources.Object import *


class HP_Frame(Object):

    @staticmethod
    def Init():
        Object.AddImage_("imgs/UI/hp_frame.png", "HP_Frame")

    def __init__(self):
        super().__init__()
        self.AddSprite("HP_Frame", "Default")
        self.SetLayer(Layer.UI)
        self.SetTag("HP_Frame")
        self.SetPivot([0, 0])
        self.SetPos([0, 0])



