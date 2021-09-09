
import pygame
from sources.Value import Value
from sources.Time import Time

# 이미지 관련 처리 클래스
class Sprite:
    images = []
    duration = 0.25
    duration_cnt = 0.0
    index = 0
    isLoop = True
    isEnd = False

    def __init__(self):
        self.images = []

    def Reset(self):
        self.index = 0
        self.duration_cnt = 0.0
        self.isEnd = False

    def GetSizeX(self):
        return self.size[index][0]

    def GetSizeY(self):
        return self.size[index][1]

    def Render(self, screen, obj):
        if self.index == len(self.images):
            self.Reset()
        self.duration_cnt += Time.deltaTime
        xPos = obj.GetXpos() - self.GetSizeX(self.index) * (obj.GetPivotX() / 100)
        yPos = obj.GetYpos() - self.GetSizeY(self.index) * (obj.GetPivotY() / 100)
        screen.blit(self.GetImage(), [xPos, yPos])

        if (self.duration / self.GetImageLength() * (self.index + 1)) <= self.duration_cnt:
            self.index += 1

    def AddImage(self, image):
        self.images.append(image)

    def SetScale(self, scale):
        for i in range(len(self.images)):
            rect = self._GetRect(i)
            self.images[i] = pygame.transform.scale(self.images[i], (int(rect[0] * scale[0]), int(rect[1] * scale[1])))

    def SetLoop(self, loop):
        self.isLoop = loop

    def SetTime(self, duration):
        self.duration = duration

    def SetDuration(self, duration):
        self.duration = duration

    def GetLoop(self):
        return self.isLoop

    def GetImage(self):
        return self.images[self.index]

    def _GetRect(self, idx):
        return self.images[idx].get_rect().size

    def GetSizeX(self, idx):
        return self._GetRect(idx)[0]

    def GetSizeY(self, idx):
        return self._GetRect(idx)[1]

    def GetImageLength(self):
        return len(self.images)

    def IsSpriteEnd(self):
        return self.GetImageLength() == self.index

