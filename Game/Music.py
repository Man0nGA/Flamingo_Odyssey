from random import shuffle
from os import listdir
import pygame

class MusicHandler():

    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, music=None):
        if music != None:
            self.musiclist = [f"Game/Music/{music}/"+i for i in listdir(f"Game/Music/{music}/")]
            shuffle(self.musiclist)
            if len(listdir(f"Game/Music/{music}/"))>0:
                self.lastmusic = self.musiclist[-1]
                self.currentmusic = -1
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.fadeout(1000)
        self.death_sound = pygame.mixer.Sound("Game/Sound/mort.mp3")
        self.tirer = pygame.mixer.Sound("Game/Sound/tirage_de_la_fleche.mp3")
        self.mur = pygame.mixer.Sound("Game/Sound/colision_avec_le_mur.wav")
        self.mur_lent = pygame.mixer.Sound("Game/Sound/colision_mur_lent.mp3")
        self.lache = pygame.mixer.Sound("Game/Sound/lache_de_la_fleche.mp3")
        self.respawn = pygame.mixer.Sound("Game/Sound/reaparition.mp3")
        self.sol = pygame.mixer.Sound("Game/Sound/colision_sol.mp3")
        self.win = pygame.mixer.Sound("Game/Sound/Victoire.wav")
        self.sound_volume()
        self.music_volume = pygame.mixer.music.set_volume(0.03)

    def sound_volume(self):
        self.death_sound.set_volume(99999)
        self.tirer.set_volume(9999)

    def play(self):
        if not pygame.mixer.music.get_busy(): # no music playing ?
            
            if len(self.musiclist) == 0:
                return

            if len(self.musiclist) == 1:
                pass

            elif self.currentmusic >= len(self.musiclist)-1:
                self.currentmusic = 0
                
                # randomize music list order
                shuffle(self.musiclist) 
                while self.musiclist[0] == self.lastmusic: 
                    shuffle(self.musiclist)

                # set music to be played
                self.lastmusic = self.musiclist[0]

            else:
                # set music to be played
                self.currentmusic += 1
                self.lastmusic = self.musiclist[self.currentmusic]

            # play music
            pygame.mixer.music.load(self.lastmusic)
            pygame.mixer.music.play()