
import sys


class Memory:
    current_score = 0
    high_score = 0

    @staticmethod
    def Init():
        file = open("temp.txt", "r")
        score = file.read()
        Memory.high_score = int(score)
        file.close()
        Memory.current_score = 0

    @staticmethod
    def Save():
        if Memory.current_score < Memory.high_score:
            return
        file = open("temp.txt", "w")
        file.write(str(Memory.current_score))
        Memory.high_score = Memory.current_score
        file.close()









