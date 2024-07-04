import time
import threading
import pygame


# Define the action to be performed
def perform_action(x):
    print(f"Action performed at {time.time()} for delay: {x} seconds")

# Define a function to wait and perform the action
def schedule_action(delay):
    time.sleep(delay)
    perform_action(delay)

def schedule_beats(beat_timing_list, midi_fpath):
# Schedule each action
    pygame.mixer.init()
    pygame.mixer.music.load(midi_fpath)
    for delay in beat_timing_list:
        threading.Thread(target=schedule_action, args=(delay[1],)).start()

    pygame.mixer.music.play(-1)

    print("All actions scheduled.")
