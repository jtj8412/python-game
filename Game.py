
import pygame
import random
from sources.Object import *
from sources.ObjectManager import *
from sources.Sprite import *
from sources.Layer import *
from sources.Value import Value
from sources.Memory import *

class Game:
    #################### Member Variable ####################
    TRAP_DELAY = [1, 3, 3, 5, 6, 9, 5, 7, 1]
    screen = pygame.display.set_mode(Value.SCREEN_SIZE)
    clock = pygame.time.Clock()
    trap_num = random.randrange(0, len(TRAP_DELAY))
    pixel_cnt = 0
    prev_num = 0
    prev_trap_cycle = 6

    #################### Initialize Class #################### 
    def InitClass(self):
        pygame.display.set_caption(Value.TITLE_NAME)
        pygame.font.init()
        pygame.mixer.init()
        Memory.Init()
        ObjectManager.Init()
        Object.Init()
        Player.Init()
        Bottom.Init()
        Star.Init()
        Background.Init()
        Wall.Init()
        Missile.Init()
        Stone.Init()
        Barrier.Init()
        Niddle.Init()
        HP_Frame.Init()
        HP.Init()
        Heal.Init()
        Decoration.Init()
        Prize.Init()

    #################### Initialize Game(Object) ####################
    def InitGame(self):
        ObjectManager.AddObject(Player(), "Player").Enable()
        ObjectManager.AddObject(HP_Frame(), "HP_Frame").Enable()
        ObjectManager.AddObject(HP(), "HP").Enable()
        ObjectManager.AddObject(Background(), "Background0").Enable()
        ObjectManager.AddObject(Background(), "Background1").Enable()
        ObjectManager.AddObject(Score(), "Score").Enable()

        for i in range(10):
            obj = ObjectManager.AddObject(Bottom(), "Bottom" + str(i)).Enable()
            obj.SetXpos(i * Value.pixel)
        for i in range(10, 15):
            ObjectManager.AddObject(Bottom(), "Bottom" + str(i))
        for i in range(4):
            ObjectManager.AddObject(Niddle(), "Niddle" + str(i))
        for i in range(20):
            ObjectManager.AddObject(Star(), "Star" + str(i))
        for i in range(6):
            ObjectManager.AddObject(Wall(), "Wall" + str(i))
        for i in range(3):
            ObjectManager.AddObject(Missile(), "Missile" + str(i))
        for i in range(3):
            ObjectManager.AddObject(Barrier(), "Barrier" + str(i))
        for i in range(3):
            ObjectManager.AddObject(Stone(), "Stone" + str(i))
        for i in range(5):
            ObjectManager.AddObject(Heal(), "Heal" + str(i))
        for i in range(5):
            ObjectManager.AddObject(Decoration(), "Decoration" + str(i))
        ObjectManager.AddObject(Prize(), "Prize")

    #################### Start Screen ####################
    def StartScreen(self):
        image = pygame.image.load("imgs/main.jpg").convert()
        image = pygame.transform.scale(image, (Value.SCREEN_SIZE[0], Value.SCREEN_SIZE[1]))
        pygame.mixer.music.load("sounds/main.ogg")
        pygame.mixer.music.play()
        while True:
            self.screen.blit(image, [0, 0])
            pygame.display.update()
            self.clock.tick(Time.fps)
            for event in (pygame.event.get()):
                if event.type == pygame.KEYDOWN:
                    Value.isGame = True
                    pygame.mixer.music.stop()
                    return
                if event.type == pygame.QUIT:
                    Value.isRun = False
                    return

    #################### Reset Game #################### 
    def Reset(self):
        ObjectManager.Clear()
        self.trap_num = random.randrange(0, len(self.TRAP_DELAY))
        self.pixel_cnt = 0
        self.prev_delay = 0
        Value.Reset()
        Memory.Init()

    #################### Update Logic ####################
    def Update(self):
        if self.prev_trap_cycle != Value.TRAP_CYCLE:
            self.prev_trap_cycle = Value.TRAP_CYCLE
            self.pixel_cnt -= 1

        Value.move_dist += Value.game_speed * Time.deltaTime
        Value.diff = Value.move_dist - Value.pixel

        if Value.move_dist >= Value.pixel:
            Value.move_dist = Value.diff
            self.pixel_cnt += 1
            if self.pixel_cnt == Value.TRAP_CYCLE:
                
                if self.trap_num == 0:
                    ObjectManager.FindDisabled("Barrier")
                elif self.trap_num == 1:
                    ObjectManager.FindDisabled("Niddle").SetNum(3)
                elif self.trap_num == 2:
                    obj = ObjectManager.FindDisabled("Star")
                    obj.SetXpos(Value.GetSummonXpos() + Value.pixel * 1.5)
                    obj.TranslateY(-130)
                elif self.trap_num == 3:
                    for i in range(3):
                        obj = ObjectManager.FindDisabled("Star")
                        obj.SetXpos(Value.GetSummonXpos() + Value.pixel * 1.5 + i * Value.pixel)
                        obj.TranslateY(-130)
                elif self.trap_num == 4:
                    ObjectManager.FindDisabled("Wall")
                elif self.trap_num == 5:
                    obj = ObjectManager.FindDisabled("Wall")
                    ObjectManager.FindDisabled("Wall").SetXpos(obj.GetXpos() + Value.pixel * 3)
                elif self.trap_num == 6:
                    ObjectManager.FindDisabled("Missile").TranslateX(self.TRAP_DELAY[self.prev_num] * 110)
                elif self.trap_num == 7:
                    ObjectManager.FindDisabled("Stone")
                elif self.trap_num == 8:
                    ObjectManager.FindDisabled("Niddle").SetNum(1)
                
                self.pixel_cnt = -self.TRAP_DELAY[self.trap_num]
                self.prev_num = self.trap_num
                self.trap_num = int(random.randrange(0, len(self.TRAP_DELAY)))

            if self.pixel_cnt >= 0 or self.prev_num == 6 or self.prev_num == 7:
                ObjectManager.FindDisabled("Bottom")
                if random.randrange(0, 30) == 0:
                    ObjectManager.FindDisabled("Heal")
                else:
                    ObjectManager.FindDisabled("Star")
                if random.randrange(0, 30) == 0:
                    ObjectManager.FindDisabled("Decoration")

    #################### Run Game ####################
    def Run(self):
        self.InitClass()
        while Value.isRun:
            self.StartScreen()
            self.InitGame()
            Time.Init()
            while Value.isGame: # KeyEvent -> Physcis -> Update -> Render
                ObjectManager.KeyEvent(pygame.event.get())
                ObjectManager.Physics()
                self.Update()
                ObjectManager.Update()
                ObjectManager.Render(self.screen)

                pygame.display.update()
                Time.UpdateTime()
                self.clock.tick_busy_loop(Time.fps)
            self.Reset()
        pygame.quit()
######################################## End Class ########################################

if __name__ == "__main__":
    Game().Run()
