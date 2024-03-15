import pygame, json
from tile_map import TileMap
from Player import Player
from Music import MusicHandler
from pygame.locals import*

def main():

    with open("Game/config.json", "r") as f:
        config = json.load(f)

    # Music
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()

    x_screen_size = pygame.display.Info().current_w
    y_screen_size = pygame.display.Info().current_h

    screen = pygame.display.set_mode((x_screen_size, y_screen_size))
    pygame.display.set_caption('The game')

    display = pygame.Surface((380, 220))

    Map = TileMap(10, "Game/Tiles/","Game/Images/")
    Map.load_map("Game/Saves/Ice.json")

    Music = MusicHandler("Ice")

    plr = Player(display, Map.basecamerapos.copy(),0.2,9.81,2.0,187.0,19.0)

    clock = pygame.time.Clock()

    while True:
        display.fill((0, 0, 0))
        
        Map.draw_map(display, plr.pos) # Map.draw_map always before plr.update 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key in [K_r]:
                    plr.isOverLimit(Map, display, screen, 1)
                if event.key in [K_k]:
                    return

        plr.update(display, Map, screen)
        Music.play()

        screen.blit(pygame.transform.scale(display, pygame.display.get_window_size()), (0,0))
        pygame.display.update()
        clock.tick(50)

        if plr.win==True:
            return 1