import time
import threading
import pygame
import os

left_open = False
right_open = False

def print_cats():
    os.system("cls" if os.name == "nt" else "clear")
    if left_open and right_open:
        with open("cats/open_open.txt", "r") as f:
            print(f.read())
    elif left_open:
        with open("cats/open_closed.txt", "r") as f:
            print(f.read())
    elif right_open:
        with open("cats/closed_open.txt", "r") as f:
            print(f.read())
    else:
        with open("cats/closed_closed.txt", "r") as f:
            print(f.read())

def open_left(delay):
    global left_open
    time.sleep(delay)
    left_open = True
    print_cats()

def close_left(delay):
    global left_open
    time.sleep(delay)
    left_open = False
    print_cats()

def open_right(delay):
    global right_open
    time.sleep(delay)
    right_open = True
    print_cats()

def close_right(delay):
    global right_open
    time.sleep(delay)
    right_open = False
    print_cats()

# Define the action to be performed
def perform_action(x, m):
    print(f"Action performed at {time.time()} for delay: {x} seconds, measure {m}")

# Define a function to wait and perform the action
def schedule_action(delay, measure):
    time.sleep(delay)
    perform_action(delay, measure)

def schedule_beats(primary_beat_times, secondary_beat_times, midi_fpath):
    pygame.mixer.init()
    pygame.mixer.music.load(midi_fpath)
    for x in range(len(primary_beat_times) - 1):
        # threading.Thread(target=schedule_action, args=(primary_beat_times[x][1], primary_beat_times[x][0],)).start()
        threading.Thread(target=open_left, args=(primary_beat_times[x][1],)).start()
        close_time = primary_beat_times[x][1] + (primary_beat_times[x + 1][1] - primary_beat_times[x][1]) / 2
        threading.Thread(target=close_left, args=(close_time,)).start()

    threading.Thread(target=open_left, args=(primary_beat_times[-1][1],)).start()
    threading.Thread(target=close_left, args=(primary_beat_times[-1][1] + 0.2,)).start()

    if secondary_beat_times:
        for x in range(len(secondary_beat_times) - 1):
            threading.Thread(target=open_right, args=(secondary_beat_times[x][1],)).start()
            close_time = secondary_beat_times[x][1] + (secondary_beat_times[x + 1][1] - secondary_beat_times[x][1]) / 2
            threading.Thread(target=close_right, args=(close_time,)).start()

        threading.Thread(target=open_right, args=(secondary_beat_times[-1][1],)).start()
        threading.Thread(target=close_right, args=(secondary_beat_times[-1][1] + 0.2,)).start()

    pygame.mixer.music.play(-1)

    print("All actions scheduled.")
