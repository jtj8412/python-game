
import pygame
from sources.Object import *
from sources.Memory import *


class Player(Object):

    move_speed = 100
    jump_power = 1400

    base_xPos = 400

    damaged_time = 0
    damaged_duration = 2
    isDamaged = False

    @staticmethod
    def Init():
        Object.AddImage_("imgs/cookie2/stand.png", "Player_Stand")
        Object.AddImage_("imgs/cookie2/run1.png", "Player_Run1")
        Object.AddImage_("imgs/cookie2/run2.png", "Player_Run2")
        Object.AddImage_("imgs/cookie2/run3.png", "Player_Run3")
        Object.AddImage_("imgs/cookie2/run4.png", "Player_Run4")
        Object.AddImage_("imgs/cookie2/jump.png", "Player_Jump")
        Object.AddImage_("imgs/cookie2/Jump2.png", "Player_Jump2")
        Object.sounds.update({"Damaged": pygame.mixer.Sound("sounds/damaged.wav")})
        Object.sounds.update({"Jump": pygame.mixer.Sound("sounds/jump.wav")})

    def __init__(self):
        super().__init__()
        self.AddSprite("Player_Stand", "Stand")
        self.AddSprite("Player_Run1", "Run")
        self.AddSprite("Player_Run2", "Run")
        self.AddSprite("Player_Run3", "Run")
        self.AddSprite("Player_Run4", "Run")
        self.AddSprite("Player_Jump", "Jump")
        self.AddSprite("Player_Jump2", "Jump2")
        self.SetScale("Run", [0.7, 0.7])
        self.SetScale("Stand", [0.75, 0.75])
        self.SetScale("Jump", [0.75, 0.75])
        self.SetScale("Jump2", [0.75, 0.75])
        self.SetPivot([50, 100])
        self.SetRect([70, 120])
        self.SetDynamic()
        self.SetTag("Player")
        self.SetPos([self.base_xPos, Value.SCREEN_SIZE[1] - Value.pixel])
        self.SetState("Run")

    def Start(self):
        pygame.mixer.music.load("sounds/bgm.mp3")
        pygame.mixer.music.play()

    def KeyEvent(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.GetState() == "Run":
                        self.SetSpeedY(-self.jump_power)
                        self.SetState("Jump")
                        Object.sounds["Jump"].play()
                    elif self.GetState() == "Jump":
                        self.SetSpeedY(-self.jump_power * 4 / 5)
                        self.SetState("Jump2")
                        Object.sounds["Jump"].play()

    def Update(self):
        if self.GetSpeedX() < 0:
            self.SetAccelX((self.base_xPos - self.GetXpos()) * 20)
        elif self.GetSpeedX() > 0:
            self.SetAccelX(0)
        if self.GetXpos() < self.base_xPos and self.GetAccelX() == 0 and not Value.gameover:
            self.SetSpeedX(self.move_speed)

        if self.GetXpos() > self.base_xPos:
            self.SetAccelX(0)
            self.SpeedX(0)
            self.TranslateX(self.base_xPos - self.GetXpos())

        if self.GetTop() > Value.SCREEN_SIZE[1] + 250 or self.GetRight() < -100:
            obj = ObjectManager.FindObject("HP")
            obj.SetXpos(-obj.GetSpriteX())

        if Memory.current_score > 160000:
            Value.TRAP_CYCLE = 2
        elif Memory.current_score > 120000:
            Value.TRAP_CYCLE = 3
        elif Memory.current_score > 80000:
            Value.TRAP_CYCLE = 4
        elif Memory.current_score > 40000:
            Value.TRAP_CYCLE = 5

        if Value.background_color == 255:
            self.isDamaged = False

    def Collision(self, obj):
        if not obj.IsTrigger() and (self.GetState() == "Jump" or self.GetState() == "Jump2") and (not obj.GetTag() == "Niddle" or self.IsDamaged()):
            if self.GetBottom() <= obj.GetTop():
                self.SetState("Run")
        if "Star" in obj.GetName():
            Memory.current_score += 100
            if Memory.high_score <= Memory.current_score:
                Memory.high_score = Memory.current_score

    def IsDamaged(self):
        return self.isDamaged and not Value.background_color >= 255

    def Damaged(self):
        self.isDamaged = True
        Value.background_color = 140
        Object.sounds["Damaged"].play()





