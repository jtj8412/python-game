
import pygame
from sources.Sprite import *
from sources.Layer import *
from sources.ObjectManager import *
from sources.Value import Value
from sources.Time import Time

# 오브젝트 (상속용)
class Object:
    _images = {}

    name = ""
    tag = ""

    enable = True

    pos = [0, 0]
    accel = [0, 0]
    speed = [0, 0]
    rect = [0, 0]
    rect_offset = [0, 0]
    pivot = [50, 100]

    sprites = {}
    cur_sprite = ""
    transparent = 255
    layer = Layer.Default

    sounds = {}

    isPhysics = False
    isTrigger = False
    mass = 1

    @staticmethod
    def Init():
        Object.AddImage_("imgs/none.png", "None")

    def __init__(self):
        self.pos = [0, 0]
        self.accel = [0, 0]
        self.speed = [0, 0]
        self.rect = [0, 0]
        self.rect_pos = [0, 0]
        self.pivot = [50, 100]
        self.sprites = {}

    def Start(self):
        pass

    def KeyEvent(self, events):
        pass

    # 가속도만큼 속도 증가 / 속도만큼 위치 변경
    def Physics(self):
        self.SpeedX(self.GetAccelX() * Time.deltaTime)
        self.SpeedY(self.GetAccelY() * Time.deltaTime)
        if self.GetSpeedY() > Value.max_speedY:
            self.SetSpeedY(Value.max_speedY)
        self.TranslateX(self.GetSpeedX() * Time.deltaTime)
        self.TranslateY(self.GetSpeedY() * Time.deltaTime)

    # 충돌체가 겹쳤을 때 밀어내기
    def Restitute(self, obj):
        if not self.IsPhysics() or obj.IsTrigger() or self.IsTrigger():
            return

        l1, t1, r1, b1 = self.GetLeft(), self.GetTop(), self.GetRight(), self.GetBottom()
        l2, t2, r2, b2 = obj.GetLeft(), obj.GetTop(), obj.GetRight(), obj.GetBottom()

        width_max = (r1 - l1) if r1 - l1 < r2 - l2 else (r2 - l2)
        height_max = (b1 - t1) if b1 - t1 < b2 - t2 else (b2 - t2)

        width = width_max
        if 0 <= r1 - l2 <= width_max:
            width = r1 - l2
        elif 0 <= l1 - r2 <= width_max:
            width = l1 - r2
        elif 0 <= r2 - l1 <= width_max:
            width = r2 - l1
        elif 0 <= l2 - r1 <= width_max:
            width = l2 - r1

        height = b2 - t1 if b2 - t1 < b1 - t2 else b1 - t2
        if not (0 <= height <= height_max):
            height = height_max

        if height <= width:

            self.TranslateY((height + 0.1) if self.GetYpos() > obj.GetYpos() else -(height + 0.1))
            self.SetAccelY(Value.gravity)
            self.SetSpeedY(0)
            if self.mass == obj.mass and obj.GetPhysics():
                obj.TranslateY(height if self.GetYpos() < obj.GetYpos() else -height)
                obj.SetAccelY(Value.gravity)
                obj.SetSpeedY(0)
        else:
            self.TranslateX(width + 0.01 if self.GetXpos() > obj.GetXpos() else -(width + 0.01))
            self.SetAccelX(0)
            self.SetSpeedX(0)
            if self.mass == obj.mass and obj.GetPhysics():
                obj.TranslateX(width + 0.01 if self.GetXpos() < obj.GetXpos() else -(width + 0.01))
                obj.SetAccelX(0)
                obj.SetSpeedX(0)

    def Update(self):
        pass

    def Collision(self, obj):
        pass

    def Render(self, screen):
        if not self.sprites.get(self.cur_sprite):
            return
        self.GetCurrentSprite().Render(screen, self)

    # 충돌체 크기 확인 (디버그용)
    def DebugRender(self, screen):
        x = self.GetXpos() - (self.GetRectX() * self.GetPivotX() / 100) + self.GetRectOffsetX()
        y = self.GetYpos() - (self.GetRectY() * self.GetPivotY() / 100) + self.GetRectOffsetY()
        w, h = self.GetRectX(), self.GetRectY()
        pygame.draw.rect(screen, Value.COLOR_KEY, [x, y, w, h], 2)

    @staticmethod
    def AddImage_(file_name, image_name="Default"):
        image = pygame.image.load(file_name).convert_alpha()
        Object._images.update({image_name: image})

    def AddSprite(self, image_name, sprite_name):
        image = Object._images.get(image_name)
        sprite = self.GetSprite(sprite_name)
        if not sprite:
            self.sprites.update({sprite_name: Sprite()})
            sprite = self.GetSprite(sprite_name)
        if self.cur_sprite == "":
            self.cur_sprite = sprite_name
        sprite.AddImage(image)

    def Delete(self):
        ObjectManager.DelObject(self)

    ###############
    # Set and Get #
    ###############
    def SetName(self, name):
        self.name = name

    def SetXpos(self, x):
        self.pos[0] = x

    def SetYpos(self, y):
        self.pos[1] = y

    def SpeedX(self, x):
        self.speed[0] += x

    def SpeedY(self, y):
        self.speed[1] += y

    def Speed(self, speed):
        self.speed[0] += speed[0]
        self.speed[1] += speed[1]

    def SetSpeedX(self, x):
        self.speed[0] = x

    def SetSpeedY(self, y):
        self.speed[1] = y

    def AccelX(self, x):
        self.accel[0] += x

    def AccelY(self, y):
        self.accel[1] += y

    def Accel(self, accel):
        self.accel[0] += accel[0]
        self.accel[1] += accel[1]

    def SetAccelX(self, x):
        self.accel[0] = x

    def SetAccelY(self, y):
        self.accel[1] = y

    def SetSprite(self, sprite_name):
        self.sprites[self.cur_sprite].Reset()
        self.cur_sprite = sprite_name

    def SetPos(self, pos):
        self.pos = pos

    def SetRect(self, rect_size):
        self.rect = rect_size

    def SetRectOffset(self, rect_offset):
        self.rect_offset = rect_offset

    def SetScale(self, state, scale):
        self.sprites[state].SetScale(scale)

    def SetSpeed(self, speed):
        self.speed = speed

    def SetAccel(self, accel):
        self.accel = accel

    def SetLayer(self, layer):
        self.layer = layer
        ObjectManager.SetLayer(self, layer)

    def SetSpriteDuration(self, sprite_name, duration):
        self.sprites[sprite_name].SetDuration(duration)

    def SetPivot(self, pivot):
        self.pivot[0] = pivot[0]
        self.pivot[1] = pivot[1]

    def SetTag(self, tag):
        self.tag = tag

    def SetStatic(self):
        if self.isPhysics:
            self.accel[1] -= Value.gravity
            self.isPhysics = False

    def SetDynamic(self):
        if not self.isPhysics:
            self.accel[1] += Value.gravity
            self.isPhysics = True

    def SetTriggerOn(self):
        self.isTrigger = True

    def SetTriggerOff(self):
        set.isTrigger = False

    def SetMass(self, mass):
        self.mass = mass

    def SetState(self, state):
        self.SetSprite(state)

    def SetTransparent(self, transparent):
        self.transparent = transparent

    def Enable(self):
        ObjectManager.FindDisabled(self.GetTag())
        return self

    def Disable(self):
        self.enable = False
        ObjectManager.AddDisabled(self)

    def GetLayer(self):
        return self.layer

    def GetName(self):
        return self.name

    def GetPos(self):
        return self.pos

    def GetXpos(self):
        return self.pos[0]

    def GetYpos(self):
        return self.pos[1]

    def GetRect(self):
        return self.rect

    def GetScaleX(self):
        return self.scale[0]

    def GetScaleY(self):
        return self.scale[1]

    def GetTag(self):
        return self.tag

    def GetRectOffset(self):
        return self.rect_offset

    def IsPhysics(self):
        return self.isPhysics

    def GetMass(self):
        return self.mass

    def GetLeft(self):
        return self.GetXpos() - self.GetRectX() * (self.GetPivotX() / 100) + self.GetRectOffsetX()

    def GetRight(self):
        return self.GetXpos() + self.GetRectX() * ((100 - self.GetPivotX()) / 100) + self.GetRectOffsetX()

    def GetTop(self):
        return self.GetYpos() - self.GetRectY() * (self.GetPivotY() / 100) + self.GetRectOffsetY()

    def GetBottom(self):
        return self.GetYpos() + self.GetRectY() * ((100 - self.GetPivotY()) / 100) + self.GetRectOffsetY()

    def GetSpeedX(self):
        return self.speed[0]

    def GetSpeedY(self):
        return self.speed[1]

    def GetAccelX(self):
        return self.accel[0]

    def GetAccelY(self):
        return self.accel[1]

    def GetRectX(self):
        return self.rect[0]

    def GetRectY(self):
        return self.rect[1]

    def GetSpriteX(self):
        return self.GetCurrentSprite().GetSizeX(0)

    def GetSpriteY(self):
        return self.GetCurrentSprite().GetSizeY()

    def GetRectOffsetX(self):
        return self.rect_offset[0]

    def GetRectOffsetY(self):
        return self.rect_offset[1]

    def GetPivotX(self):
        return self.pivot[0]

    def GetPivotY(self):
        return self.pivot[1]

    def GetSprite(self, sprite_name):
        return self.sprites.get(sprite_name)

    def GetCurrentSprite(self):
        return self.sprites.get(self.cur_sprite)

    def GetState(self):
        return self.cur_sprite

    def GetTransparent(self):
        return self.transparent

    def IsEnable(self):
        return self.enable

    def IsTrigger(self):
        return self.isTrigger

    def IsStateEnd(self):
        return self.GetCurrentSprite().IsSpriteEnd()

    def TranslateX(self, x):
        self.pos[0] += x

    def TranslateY(self, y):
        self.pos[1] += y

    def Translate(self, vec):
        self.pos[0] += vec[0]
        self.pos[1] += vec[1]


from sources.object.Player import *
from sources.object.Bottom import *
from sources.object.Star import *
from sources.object.Background import *
from sources.object.Wall import *
from sources.object.Missile import *
from sources.object.Stone import *
from sources.object.Barrier import *
from sources.object.Niddle import *
from sources.object.HP_Frame import *
from sources.object.HP import *
from sources.object.Score import *
from sources.object.Heal import *
from sources.object.Decoration import *
from sources.object.Prize import *
