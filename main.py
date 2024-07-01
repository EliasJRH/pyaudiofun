import wave
# import numpy as np
# from scipy import signal    
import pygame
import math
from playsound import playsound

def main():
    pygame.init()
    playsound("Gravity Falls.wav")

    clock = pygame.time.Clock()
    FPS = 100

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800

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
            if event.type == pygame.QUIT: run = False

        pygame.display.update()

    pygame.quit()




if __name__ == "__main__":
    main()

# wave_obj = wave.open("Gravity Falls.wav", "rb")
# samples_per_sec = wave_obj.getframerate()
# samples = wave_obj.getnframes()
# length = samples/samples_per_sec
# print(f"{samples}/{samples_per_sec}={length}")
# print(samples_per_sec * 0.1)
# signalwave = wave_obj.readframes(samples)
# signal_array = np.frombuffer(signalwave, dtype=np.int16)
# times = np.linspace(0, samples/samples_per_sec, num=samples)
# print(times)
# print([1,2,3])
# peaks_indices = signal.find_peaks(signal_array)
# print(peaks_indices[0])
# peak_times = []
# for i in list(peaks_indices[0][0:20]):
#     peak_times.append(times[i])

# print(peak_times)