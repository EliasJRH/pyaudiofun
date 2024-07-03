# import numpy as np
# from scipy import signal
from functools import cache
import pygame
import math
import threading
import sys
import xml.etree.ElementTree as ET
import time

notes_to_beat = {
    "whole": 4,
    "half": 2,
    "quarter": 1,
    "eighth": 0.5,
    "16th": 0.25,
}


@cache
def find_tempo(element):
    try:
        return (
            element.find("direction")
            .find("direction-type")
            .find("metronome")
            .find("per-minute")
            .text
        )
    except AttributeError:
        return None



def parse_musicxml(file):
    tree = ET.parse(file)
    measures = tree.find("part").findall("measure")
    note_delays_seconds = []
    last_second = 0

    for n, m in enumerate(measures):
        last_x = 0  # Used to distinguish notes from each other
        items = m.iterfind("*")  # Used to find all notes
        tempo = int(find_tempo(m)) if find_tempo(m) else (tempo if tempo else 0)
        spb = 60 / tempo  # How many seconds each beat should last
        for item in items:
            
            # We only want to look at the primary notes, so we ignore the backup notes
            if item.tag == "note":
                # If a note is on the other side of a tie, we ignore it because it's not a new beat
                # if item.find("tie") is not None and item.find("tie").get("type") == "stop": continue
                
                # Some notes are stacked, so we only look at it if it's positioned differently
                x_pos = float(item.get("default-x"))
                if x_pos != last_x:
                    # Note delay seconds indicates the time in seconds after the beginning of the song that the note should be played
                    # If a note is a rest note OR if it is the end of a tied note, we ignore it because it won't be played
                    if (item.find("tie") is None or item.find("tie").get("type") != "stop") and item.find("rest") is None: note_delays_seconds.append((n + 1, last_second))

                    # Calculate next beat time

                    type = item.find("type").text  # Type of note (whole, half, etc)
                    last_x = x_pos
                    
                    # If the note is dotted, we'll need to add an additional half of its length
                    dotted = True if item.find("dot") is not None else False
                    
                    # Update next beat time
                    num_beats = notes_to_beat[type] + (notes_to_beat[type] / 2 if dotted else 0)
                    last_second += num_beats * spb
            elif item.tag == "backup":
                break
    return note_delays_seconds


def print_beat_changes(note_times):
    last_second = 0
    for i in note_times:
        print(i - last_second)
        last_second = i
        time.sleep(i - last_second)
        print(i)


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

    # create game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Endless Scroll")

    # load image
    bg = pygame.image.load("bg_lr.png").convert()
    bg_width = bg.get_width()
    bg_rect = bg.get_rect()

    # define game variables
    scroll = 0
    tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1

    # game loop
    pygame.mixer.music.play(-1)
    run = True
    while run:

        clock.tick(FPS)
        pygame.time.get_ticks()
        # draw scrolling background
        for i in range(0, tiles):
            screen.blit(bg, (i * bg_width + scroll, 0))
            bg_rect.x = i * bg_width + scroll
            # pygame.draw.rect(screen, (255, 0, 0), bg_rect, 1)

        # scroll background
        scroll -= 5

        # reset scroll
        if abs(scroll) > bg_width:
            scroll = 0

        # event handler
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
    # note_times = parse_musicxml(
    #     "songs/Gravity Falls/Gravity_Falls_Opening_-_Intermediate_Piano_Solo.musicxml"
    # )
    note_times = parse_musicxml(
        "songs/Phinease and Ferb/Phineas_and_ferb_theme_–_Bowling_for_Soup_Phineas_and_Ferb_-_Theme_song.musicxml"
    )
    print(note_times)
    # game_thread = threading.Thread(target=run_game)
    # beat_thread = threading.Thread(target=print_beat_changes, args=(note_times,))

    # game_thread.start()
    # beat_thread.start()

    # game_thread.join()
    # beat_thread.join()


if __name__ == "__main__":
    main()
