
from sources.Time import *

# 전역 변수 및 함수
class Value:
    TITLE_NAME = "Cookie Run"
    SCREEN_SIZE = (1280, 720)
    color_key = (14, 209, 69)
    pixel = 128.0
    TRAP_CYCLE = 6

    game_speed = 600.0
    hp_minus = 15

    gravity = 4000
    max_speedY = 1300.0

    move_dist = 130
    diff = 0

    background_color = 255

    gameover = False
    isGame = False
    isRun = True
    isDebug = False

    @staticmethod
    def Reset():
        Value.move_dist = 130
        Value.diff = 0
        Value.game_speed = 600.0

    @staticmethod
    def GetSummonXpos():
        return Value.SCREEN_SIZE[0] - Value.diff + Value.game_speed * Time.deltaTime


