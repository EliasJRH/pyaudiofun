from functools import cache
import xml.etree.ElementTree as ET
import os
import inquirer
import argparse, sys
from visualizer import schedule_beats

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
    
def calculate_time_modification(element):
    try:
        return (int(element.find("time-modification").find("normal-notes").text) / 
                int(element.find("time-modification").find("actual-notes").text))
    except AttributeError:
        return 1

def parse_musicxml(file):
    tree = ET.parse(file)
    measures = tree.find("part").findall("measure")
    primary_note_delays_seconds = []
    secondary_note_delays_seconds = []
    last_primary_second = 0
    last_secondary_second = 0
    tempo = None
    sbp = None # Second per beat, how long a beat lasts in seconds, used to calculate note delays
    divisions = None # Number of divisions per beat, used to calculate note delays in absence of note type
    tempo_changed = False
    changed_tempo_item = None
    time_modifier = 1

    for measure_num, measure in enumerate(measures):
        recording_backup_notes = False # backup notes occur once per measure at most, so the flag is reset per measure
        items = list(measure.iterfind("*"))  # Used to find all notes
        tempo_changes = []
        item_num = 0
        while item_num < len(items):
            item = items[item_num]
            if item.tag == "note":
                # x_pos is recorded to find out when tempo changes occur
                x_pos = item.get("default-x")

                # Notes marked as a chord are played as part of the same note as the previous note at the same time, so we ignore the
                # completely
                is_chord = item.find("chord") is not None
                if is_chord:
                    item_num += 1 # Continue will go to start of while loop without incrementing item_num, have to increment here
                    continue

                # In order to match tempos for the secondary notes, we need to record when the tempo changes during the primary notes
                # This is purely because of the fact that musicxml files only record tempo changes on the primary set of notes which makes
                # sense given that this a codefied representation of the sheet music
                # The tempo_changed flag is used because we can only determine the x_pos at which the tempo change occurs after the next
                # note is encountered
                if tempo_changed: 
                    tempo_changes.append({"x_pos": x_pos, "tempo_item": changed_tempo_item})
                    tempo_changed = False

                # Note delay seconds indicates the time in seconds after the beginning of the song that the note should be played
                # If a note is a rest note OR if it is the end of a tied note, we don't record it's beat time because it won't 
                # played however, we still add the time it takes to the play that note to the overall time+
                if (item.find("tie") is None or item.find("tie").get("type") != "stop") and item.find("rest") is None: 
                    if recording_backup_notes: secondary_note_delays_seconds.append((measure_num+1, last_secondary_second))
                    else: primary_note_delays_seconds.append((measure_num + 1, last_primary_second))

                # Calculate next beat time for next note

                # If the note is dotted, we'll need to add an additional half of its length
                dotted = True if item.find("dot") is not None else False

                time_modifier = calculate_time_modification(item)

                try: 
                    type = item.find("type").text  # Type of note (whole, half, etc)
                    num_beats = (notes_to_beat[type] + (notes_to_beat[type] / 2 if dotted else 0)) * time_modifier
                except AttributeError:
                    duration = item.find("duration").text  # If the type of note is not specified, we use the duration
                    num_beats = ((int(duration) / divisions) * (1.5 if dotted else 1)) * time_modifier
                
                # Update next beat time for the next note
                if recording_backup_notes: last_secondary_second += num_beats * sbp
                else: last_primary_second += num_beats * sbp
            elif item.tag == "direction":
                # If the direction tag contains a new tempo, we change the tempo and seconds per beat
                tempo = int(get_tempo(item)) if get_tempo(item) else tempo
                if tempo:
                    sbp = 60 / tempo
                    tempo_changed = True
                    changed_tempo_item = item
            elif item.tag == "attributes":
                # Obtains divisions for when note type is omitted
                divisions = int(get_divisions(item)) if get_divisions(item) else divisions
            elif item.tag == "backup":
                if not recording_backup_notes: 
                    recording_backup_notes = True
                    cur_ind = item_num + 1
                    while cur_ind < len(items) and len(tempo_changes) > 0:
                        next_item = items[cur_ind]
                        if next_item.tag == "note" and not next_item.get("chord"):
                            if float(next_item.get("default-x")) == float(tempo_changes[0]["x_pos"]): 
                                items.insert(cur_ind, tempo_changes.pop(0)["tempo_item"])
                            elif float(next_item.get("default-x")) > float(tempo_changes[0]["x_pos"]):
                                item.insert(cur_ind-1, tempo_changes.pop(0)["tempo_item"])
                        cur_ind += 1
                else: break
            item_num += 1

    song_length = max(primary_note_delays_seconds[-1][1], secondary_note_delays_seconds[-1][1]) + (sbp * 4)
    return (primary_note_delays_seconds, secondary_note_delays_seconds, song_length)

def parse_cmd_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--debug", help="Run in debug mode", default=False, action="store_true")
    args = arg_parser.parse_args()
    return args

def main():
    args = parse_cmd_args()

    song_dirs = sorted(os.listdir("songs"))
    # Only display song directories that contain a musicxml file and a midi file
    # I'm going to assume that they'll always be valid, otherwise ¯\_(ツ)_/¯
    song_choices = [inquirer.List("song", 
                                 message="Pick a song", 
                                 choices=[song for song in song_dirs if 
                                          len(list(filter(lambda x: x.endswith(".musicxml"), os.listdir(f"songs/{song}")))) and 
                                          len(list(filter(lambda x: x.endswith(".mid"), os.listdir(f"songs/{song}"))))]
                                )]
    ans = inquirer.prompt(song_choices)

    # I'm also assuming that there's exactly one of each type of file
    musicxml_fname = [f for f in os.listdir(f"songs/{ans["song"]}") if f.endswith(".musicxml")][0]
    musicxml_fpath = f"songs/{ans["song"]}/{musicxml_fname}"
    midi_fname = [f for f in os.listdir(f"songs/{ans["song"]}") if f.endswith(".mid")][0]
    midi_fpath = f"songs/{ans["song"]}/{midi_fname}"

    primary_beat_times, secondary_beat_times, song_length = parse_musicxml(musicxml_fpath)
    schedule_beats(primary_beat_times, secondary_beat_times, midi_fpath, song_length, args.debug)


if __name__ == "__main__":
    main()
