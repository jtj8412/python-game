
import pygame
from sources.Object import *
from sources.Layer import *
from sources.Value import *

# 모든 오브젝트를 관리하는 클래스
class ObjectManager:

    obj_list = []
    del_list = []
    obj_pool = {}

    @staticmethod
    def Init():
        for i in range(Layer.Length):
            ObjectManager.obj_list.append({})

    @staticmethod
    def KeyEvent(events):
        for event in events:
            if event.type == pygame.QUIT:
                Value.isRun = False
                Value.isGame = False
            if event.type == pygame.KEYDOWN:
                if Value.gameover:
                    Value.isGame = False
                if event.key == ord('d'):
                    Value.isDebug = not Value.isDebug
        for layer in range(Layer.Length):
            for obj in ObjectManager.obj_list[layer].values():
                if not obj.IsEnable():
                    continue
                obj.KeyEvent(events)
        ObjectManager._DelObject()

    @staticmethod
    def Update():
        if Value.gameover:
            return
        for layer in range(Layer.Length):
            for obj in ObjectManager.obj_list[layer].values():
                if obj.IsEnable():
                    obj.Update()
        ObjectManager._DelObject()


    @staticmethod
    def Physics():
        obj_list = []
        for layer in range(Layer.Length):
            for obj in ObjectManager.obj_list[layer].values():
                if obj.IsEnable():
                    obj_list.append(obj)
        for obj in obj_list:
            obj.Physics()
        for i in range(0, len(obj_list) - 1):
            for j in range(i + 1, len(obj_list)):
                if ObjectManager.CheckCollision(obj_list[i], obj_list[j]):
                    if obj_list[i].GetMass() > obj_list[j].GetMass():
                        obj_list[j].Restitute(obj_list[i])
                    elif obj_list[i].GetMass() < obj_list[j].GetMass():
                        obj_list[i].Restitute(obj_list[j])
                    obj_list[i].Collision(obj_list[j])
                    obj_list[j].Collision(obj_list[i])
        ObjectManager._DelObject()

    @staticmethod
    def CheckCollision(obj1, obj2):
        l1, t1, r1, b1 = obj1.GetLeft(), obj1.GetTop(), obj1.GetRight(), obj1.GetBottom()
        l2, t2, r2, b2 = obj2.GetLeft(), obj2.GetTop(), obj2.GetRight(), obj2.GetBottom()

        if r1 >= l2 and b1 >= t2 and l1 <= r2 and t1 <= b2:
            return True
        return False

    @staticmethod
    def Render(screen):
        for layer in range(Layer.Length):
            for obj in ObjectManager.obj_list[layer].values():
                if obj.IsEnable():
                    obj.Render(screen)
        if Value.isDebug:
            for layer in range(Layer.Length):
                for obj in ObjectManager.obj_list[layer].values():
                    if not obj.IsEnable():
                        continue
                    obj.DebugRender(screen)
        if Value.background_color < 255:
            screen.fill((255, int(Value.background_color), int(Value.background_color)), None, pygame.BLEND_RGBA_MULT)
            Value.background_color += 50 * Time.deltaTime

    @staticmethod
    def AddObject(obj, obj_name, layer=Layer.Default):
        if not obj.GetLayer() == Layer.Default:
            layer = obj.GetLayer()
        obj.SetName(obj_name)
        ObjectManager.obj_list[layer].update({obj.GetName(): obj})
        obj.Disable()
        return obj

    @staticmethod
    def PopObject(obj):
        for layer in range(Layer.Length):
            if ObjectManager.obj_list[layer].get(obj.GetName()):
                ObjectManager.obj_list[layer].pop(obj.GetName())
                return obj

    @staticmethod
    def DelObject(obj):
        for i in range(len(ObjectManager.del_list)):
            if ObjectManager.del_list[i].GetName() == obj.GetName():
                return
        ObjectManager.del_list.append(obj)

    @staticmethod
    def _DelObject():
        while len(ObjectManager.del_list) != 0:
            obj = ObjectManager.PopObject(ObjectManager.del_list.pop())
            del obj

    @staticmethod
    def FindObject(obj_name):
        obj = None
        for layer in range(Layer.Length):
            obj = ObjectManager.obj_list[layer].get(obj_name)
            if obj:
                break
        return obj

    @staticmethod
    def FindObjectWithTag(tag_name):
        for layer in range(Layer.Length):
            for obj in ObjectManager.obj_list[layer].values():
                if obj.GetTag() == tag_name:
                    return obj
        return None

    '''
    @staticmethod
    def AddDisabled(obj):
        ObjectManager.obj_pool.append(obj)
    '''

    @staticmethod
    def AddDisabled(obj):
        arr = ObjectManager.obj_pool.get(obj.GetTag())
        if not arr:
            ObjectManager.obj_pool.update({obj.GetTag(): [obj]})
        else:
            arr.append(obj)


    '''
    @staticmethod
    def FindDisabled(obj_name):
        obj = None
        for i in range(len(ObjectManager.obj_pool)):
            if obj_name in ObjectManager.obj_pool[i].GetName():
                obj = ObjectManager.obj_pool.pop(i)
                obj.enable = True
                obj.Start()
                break
        return obj
    '''
    @staticmethod
    def FindDisabled(tag):
        arr = ObjectManager.obj_pool.get(tag)
        obj = arr.pop(0)
        obj.enable = True
        obj.Start()
        return obj

    @staticmethod
    def FindDisabledWithTag(tag_name):
        obj = None
        for i in range(len(ObjectManager.obj_pool)):
            if ObjectManager.obj_pool[i].GetTag() == tag_name:
                obj = ObjectManager.obj_pool[i]
                obj.Enable()
                ObjectManager.obj_pool.pop(i)
                break
        return obj

    @staticmethod
    def SetLayer(obj, layer):
        if obj.GetName() == "":
            return
        ObjectManager.PopObject(obj)
        ObjectManager.AddObject(obj, obj.GetName(), layer)

    @staticmethod
    def GetObjectLength():
        return len(ObjectManager.obj_list)

    @staticmethod
    def AllStop():
        for layer in range(Layer.Length):
            for obj in ObjectManager.obj_list[layer].values():
                if obj.GetName() != "Player":
                    obj.SetSpeed([0, 0])
                else:
                    obj.SetSpeed([0, -900])
                    obj.SetStatic()
                    obj.SetAccel([0, Value.gravity])
        Value.game_speed = 0
        ObjectManager.FindDisabled("Prize")

    @staticmethod
    def Clear():
        for layer in range(Layer.Length):
            for obj in ObjectManager.obj_list[layer].values():
                del obj
            ObjectManager.obj_list[layer].clear()
        ObjectManager.obj_pool.clear()
        Value.isGame = True
        Value.gameover = False


