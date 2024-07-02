# import numpy as np
# from scipy import signal    
import pygame
import math
import threading
import sys


def run_game():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.mixer.init()
    pygame.mixer.music.load("Gravity Falls.wav")
    FPS = 100

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    ud = False
    lr = True

    #create game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Endless Scroll")

    #load image
    bg = pygame.image.load("bg_lr.png").convert()
    bg_width = bg.get_width()
    bg_rect = bg.get_rect()

    #define game variables
    scroll = 0
    tiles = math.ceil(SCREEN_WIDTH  / bg_width) + 1

    #game loop
    pygame.mixer.music.play(-1)
    run = True
    while run:

        clock.tick(FPS)

        #draw scrolling background
        for i in range(0, tiles):
            screen.blit(bg, (i * bg_width + scroll, 0))
            bg_rect.x = i * bg_width + scroll
            # pygame.draw.rect(screen, (255, 0, 0), bg_rect, 1)

        #scroll background
        scroll -= 5

        #reset scroll
        if abs(scroll) > bg_width:
            scroll = 0

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                if not ud and (keys[pygame.K_UP] or keys[pygame.K_DOWN]):
                    ud = True
                    lr = False
                    bg = pygame.transform.rotate(bg, 90)
                    bg_width = bg.get_width()
                    bg_rect = bg.get_rect()
                    tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1
                if not lr and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
                    lr = True
                    ud = False
                    bg = pygame.transform.rotate(bg, -90)
                    bg_width = bg.get_width()
                    bg_rect = bg.get_rect()
                    tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1

        pygame.display.update()

    pygame.mixer.stop()
    pygame.mixer.quit()
    pygame.quit()

def main():
    game_thread = threading.Thread(target=run_game)

    game_thread.start()

    game_thread.join()

if __name__ == "__main__":
    main()