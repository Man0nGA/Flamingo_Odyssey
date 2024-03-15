import pygame, json
from mainmenu import MainMenu
from pygame.locals import *

def main():

    with open("Game/config.json", "r") as f:
        config = json.load(f)

    #Music
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()

    x_screen_size = pygame.display.Info().current_w
    y_screen_size = pygame.display.Info().current_h

    screen = pygame.display.set_mode((x_screen_size, y_screen_size))
    #screen = pygame.display.set_mode((x_screen_size, y_screen_size))
    pygame.display.set_caption('The game')

    display = pygame.Surface((380, 220))
    mainmenu = MainMenu()

    clock = pygame.time.Clock()

    while True:
        display.fill((0, 0, 0))

        mainmenu.update(display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                pass
            if event.type == KEYUP:
                pass
            if event.type == KEYDOWN:
                if event.key in [K_k]:
                    return
            
        screen.blit(pygame.transform.scale(display, pygame.display.get_window_size()), (0,0))
        pygame.display.update()
        clock.tick(70)

main()
