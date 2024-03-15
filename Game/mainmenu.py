import pygame
from random import shuffle
from json import load, dump
from Music import MusicHandler
import Lava as lv
import Forest as fr
import Ice as ice #No need to thank my incredible name imagination.

def scale_mouse_pos(screen_size):
    mousepos = list(pygame.mouse.get_pos())
    ratio_x = (screen_size[0] - 1) / 380
    ratio_y = (screen_size[1] - 1) / 220
    return mousepos[0] / ratio_x, mousepos[1] / ratio_y

class MainMenu():

    def __init__(self):
        self.fond = pygame.image.load("Game/Assets/Menu.png")
        self.winfond = pygame.image.load("Game/Assets/WinMenu.png")

        # get config
        with open("Game/config.json",'r') as f:
            self.config = load(f)

        # load planets images
        self.lavahover = pygame.image.load("Game/Assets/Fire_hover.png")
        self.earthhover = pygame.image.load("Game/Assets/Earth_hover.png")
        self.icehover = pygame.image.load("Game/Assets/Ice_hover.png")

        # grayed planet
        self.grayedearth = pygame.image.load("Game/Assets/Earth_Black.png")
        self.grayedearth.set_alpha(200)
        self.grayedice = pygame.image.load("Game/Assets/Ice_Black.png")
        self.grayedice.set_alpha(200)

        self.music = MusicHandler("MainMenu")

        self.clicked = False

    def draw(self, surface):
        if self.config["The End"] == 0:
            surface.blit(self.fond, (0,0))
        else :
            surface.blit(self.winfond, (0,0))

    #### PLANETS


    def lavaplanet(self, surface):
        if 133 <= self.mousepos[0] <= 169 and 72 <= self.mousepos[1] <= 108:
            surface.blit(self.lavahover, (133, 72))
            if self.mouseaction[0] and not self.clicked:
                if lv.main() == 1:
                    self.config["greenPlanet"] = 1
                    with open("Game/config.json", 'w') as f:
                        dump(self.config, f)
    
    def greenplanet(self, surface): #260 143
        if self.config["greenPlanet"] == 0:
            surface.blit(self.grayedearth, (205,111))
            return
        if 205 <= self.mousepos[0] <= 261 and 111 <= self.mousepos[1] <= 160:
            surface.blit(self.earthhover, (205, 111))
            if self.mouseaction[0] and not self.clicked:
                if fr.main() == 1:
                    self.config["grayPlanet"] = 1
                    with open("Game/config.json", 'w') as f:
                        dump(self.config, f)
    
    def grayplanet(self, surface):
        if self.config["grayPlanet"] == 0:
            surface.blit(self.grayedice, (307,50))
            return
        if 307 <= self.mousepos[0] <= 375 and 50 <= self.mousepos[1] <= 123:
            surface.blit(self.icehover, (307, 51))
            if self.mouseaction[0] and not self.clicked:
                if ice.main() == 1:
                    self.config["The End"] = 1
                    with open("Game/config.json", 'w') as f:
                        dump(self.config, f)
     

    #### HANDLERS


    def mousehandler(self, screen_size):
        self.mouseaction = pygame.mouse.get_pressed()
        self.mousepos = scale_mouse_pos(screen_size)

    def clickedhandler(self):
        if self.mouseaction[0]:
            self.clicked = True
        else:
            self.clicked = False
    

    #### UPDATE

    def update(self, display):
        self.draw(display)

        self.mousehandler(pygame.display.get_window_size())

        self.lavaplanet(display)
        self.greenplanet(display)
        self.grayplanet(display)

        self.clickedhandler()
        self.music.play()