from functools import cache
import xml.etree.ElementTree as ET
import os
import inquirer

notes_to_beat = {
    "whole": 4,
    "half": 2,
    "quarter": 1,
    "eighth": 0.5,
    "16th": 0.25,
    "32nd": 0.125,
    "64th": 0.0625,
    "128th": 0.03125,
    "256th": 0.03125 / 2,
    "512th": (0.03125 / 2) / 2,
}

@cache
def get_tempo(element):
    try:
        return (
            element.find("direction-type")
            .find("metronome")
            .find("per-minute")
            .text
        )
    except AttributeError:
        try:
            return element.find("sound").get("tempo")
        except AttributeError:
            return None

@cache
def get_divisions(element):
    try:
        return element.find("divisions").text
    except AttributeError:
        return None

def parse_musicxml(file):
    tree = ET.parse(file)
    measures = tree.find("part").findall("measure")
    note_delays_seconds = []
    last_second = 0
    tempo = None
    sbp = None # Second per beat, how long a beat lasts in seconds, used to calculate note delays
    divisions = None # Number of divisions per beat, used to calculate note delays in absence of note type

    for n, m in enumerate(measures):
        items = m.iterfind("*")  # Used to find all notes
        for item in items:
            
            # We only want to look at the primary notes, so we ignore the backup notes
            if item.tag == "note":
                # Notes marked as a chord are played as part of the same beat as the previous note at the same time, so we ignore them 
                is_chord = item.find("chord") is not None
                if is_chord: continue

                # Note delay seconds indicates the time in seconds after the beginning of the song that the note should be played
                # If a note is a rest note OR if it is the end of a tied note, we ignore it because it won't be played
                if (item.find("tie") is None or item.find("tie").get("type") != "stop") and item.find("rest") is None: note_delays_seconds.append((n + 1, last_second))

                # Calculate next beat time

                # If the note is dotted, we'll need to add an additional half of its length
                dotted = True if item.find("dot") is not None else False

                try: 
                    type = item.find("type").text  # Type of note (whole, half, etc)
                    num_beats = notes_to_beat[type] + (notes_to_beat[type] / 2 if dotted else 0)
                except AttributeError:
                    duration = item.find("duration").text  # If the type of note is not specified, we use the duration
                    num_beats = (int(duration) / divisions) * (1.5 if dotted else 1)
                
                # Update next beat time
                last_second += num_beats * sbp
            elif item.tag == "direction":
                tempo = int(get_tempo(item)) if get_tempo(item) else tempo
                if tempo: sbp = 60 / tempo
            elif item.tag == "attributes":
                divisions = int(get_divisions(item)) if get_divisions(item) else divisions
            elif item.tag == "backup":
                break
    return note_delays_seconds


def main():
    song_dirs = os.listdir("songs")
    song_choices = [inquirer.List("song", 
                                 message="Pick a song", 
                                 choices=[song for song in song_dirs if 
                                          len(list(filter(lambda x: x.endswith(".musicxml"), os.listdir(f"songs/{song}")))) and 
                                          len(list(filter(lambda x: x.endswith(".mid"), os.listdir(f"songs/{song}"))))]
                                )]
    ans = inquirer.prompt(song_choices)
    # note_times = parse_musicxml("songs/Death by Glamour/Death_by_Glamour_piano.musicxml")
    # print(note_times)


if __name__ == "__main__":
    main()
