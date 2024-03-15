import pygame, os


animations = {}
for f in os.listdir("Game/Animations/"):
    animations[f] = {}
    for a in os.listdir("Game/Animations/"+f+"/"):
        animations[f][a.split(".")[0]] = pygame.image.load("Game/Animations/"+f+"/"+a)


class Animation():
    def __init__(self, name, startingframe = 0, delay = 30):
        self.anim = animations[name]
        
        self.maxframe = len(self.anim)-1
        if startingframe >= self.maxframe or startingframe < 0:
            self.frame = 0
        else:
            self.frame = startingframe

        self.counter = 0
        self.delay = delay

    def getframe(self):
        f = self.anim[str(self.frame)]

        self.counter += 1
        if self.counter == self.delay:
            if self.frame == self.maxframe:
                self.frame = 0
            else:
                self.frame += 1
            self.counter = 0

        return f
    
    def get_rect(self):
        return self.anim["0"].get_rect()