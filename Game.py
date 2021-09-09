
import pygame
import random
from sources.Object import *
from sources.ObjectManager import *
from sources.Sprite import *
from sources.Layer import *
from sources.Value import Value
from sources.Memory import *

#####################################################################
#####################################################################

screen = pygame.display.set_mode(Value.SCREEN_SIZE)
pygame.display.set_caption(Value.TITLE_NAME)
clock = pygame.time.Clock()


#####################################################################
#####################################################################

def Init():
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


def InitGame():
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


def Main():
    image = pygame.image.load("imgs/main.jpg").convert()
    image = pygame.transform.scale(image, (Value.SCREEN_SIZE[0], Value.SCREEN_SIZE[1]))
    pygame.mixer.music.load("sounds/main.ogg")
    pygame.mixer.music.play()
    while True:
        screen.blit(image, [0, 0])
        pygame.display.update()
        clock.tick(Time.fps)
        for event in (pygame.event.get()):
            if event.type == pygame.KEYDOWN:
                Value.isGame = True
                pygame.mixer.music.stop()
                return
            if event.type == pygame.QUIT:
                Value.isRun = False
                return


def Reset():
    global trap_num, pixel_cnt, prev_delay
    ObjectManager.Clear()
    trap_num = random.randrange(0, len(TRAP_DELAY))
    pixel_cnt = 0
    prev_delay = 0
    Value.Reset()
    Memory.Init()


#####################################################################
#####################################################################

TRAP_DELAY = [1, 3, 3, 5, 6, 9, 5, 7, 1]
trap_num = random.randrange(0, len(TRAP_DELAY))
pixel_cnt = 0
prev_num = 0
prev_trap_cycle = 6


def Update():
    global pixel_cnt, trap_num, prev_num, prev_trap_cycle

    if prev_trap_cycle != Value.TRAP_CYCLE:
        prev_trap_cycle = Value.TRAP_CYCLE
        pixel_cnt -= 1

    Value.move_dist += Value.game_speed * Time.deltaTime
    Value.diff = Value.move_dist - Value.pixel

    if Value.move_dist >= Value.pixel:
        Value.move_dist = Value.diff
        pixel_cnt += 1
        if pixel_cnt == Value.TRAP_CYCLE:
            ###### TRAP ######
            if trap_num == 0:
                ObjectManager.FindDisabled("Barrier")
            elif trap_num == 1:
                ObjectManager.FindDisabled("Niddle").SetNum(3)
            elif trap_num == 2:
                obj = ObjectManager.FindDisabled("Star")
                obj.SetXpos(Value.GetSummonXpos() + Value.pixel * 1.5)
                obj.TranslateY(-130)
            elif trap_num == 3:
                for i in range(3):
                    obj = ObjectManager.FindDisabled("Star")
                    obj.SetXpos(Value.GetSummonXpos() + Value.pixel * 1.5 + i * Value.pixel)
                    obj.TranslateY(-130)
            elif trap_num == 4:
                ObjectManager.FindDisabled("Wall")
            elif trap_num == 5:
                obj = ObjectManager.FindDisabled("Wall")
                ObjectManager.FindDisabled("Wall").SetXpos(obj.GetXpos() + Value.pixel * 3)
            elif trap_num == 6:
                ObjectManager.FindDisabled("Missile").TranslateX(TRAP_DELAY[prev_num] * 110)
            elif trap_num == 7:
                ObjectManager.FindDisabled("Stone")
            elif trap_num == 8:
                ObjectManager.FindDisabled("Niddle").SetNum(1)
            ###### TRAP ######
            pixel_cnt = -TRAP_DELAY[trap_num]
            prev_num = trap_num
            trap_num = int(random.randrange(0, len(TRAP_DELAY)))

        if pixel_cnt >= 0 or prev_num == 6 or prev_num == 7:
            ObjectManager.FindDisabled("Bottom")
            if random.randrange(0, 30) == 0:
                ObjectManager.FindDisabled("Heal")
            else:
                ObjectManager.FindDisabled("Star")
            if random.randrange(0, 30) == 0:
                ObjectManager.FindDisabled("Decoration")



Init()
while Value.isRun:
    Main()
    InitGame()
    Time.Init()
    while Value.isGame:
        ObjectManager.KeyEvent(pygame.event.get())
        ObjectManager.Physics()
        Update()
        ObjectManager.Update()
        ObjectManager.Render(screen)

        pygame.display.update()
        Time.UpdateTime()
        clock.tick_busy_loop(Time.fps)
    Reset()
pygame.quit()

#####################################################################
#####################################################################

