from math import floor
from random import randrange

import scamp

scamp.engraving_settings.lilypond_search_paths
print(scamp.engraving_settings.lilypond_dir)

s = scamp.Session()
s.tempo = 120

cello = s.new_part("cello")

current_note = 48
position_in_scale = 0
minor_scale = [2,2,1,2,2,2,1]
harmonic_minor_scale = [2,2,1,3,1,2,1]
scale = minor_scale

def go_to_note(note):
    global position_in_scale
    new_note = 0
    for i in range(abs(note)):
        if note < 0:
            new_note -= scale[(position_in_scale-i-1)%7]
        else:
            new_note += scale[(position_in_scale+i)%7]
    position_in_scale += note
    return new_note

def sequences(iteration, interval):
    global current_note
    n = -1 - interval
    if iteration < 0:
        n = -2 - interval
    for i in range(abs(iteration)):
        count = 0
        for j in range(n, 3 + interval, 3 + (interval*2)):
            current_note += go_to_note(j)
            cello.play_note(current_note,1.0,.25)
            count += 1

def patterns(iteration, interval, notes):
    global current_note
    note_length = []
    for i in range(abs(notes)):
        note_length.append(randrange(1, 3, 1))
    for i in range(abs(iteration)):
        count = 0
        for j in range(abs(notes)):
            current_note += go_to_note(interval)
            cello.play_note(current_note,1.0,.25)
            count += 1
        if i != (iteration-1):
            current_note += go_to_note(-(interval*notes)+interval)

s.start_transcribing()
for i in range(1):
    r = randrange(-1,2,2)
    if current_note < 48:
        r = 1
    elif current_note > 60:
        r = -1
    sequences(2*r,randrange(0,3,1))
    patterns(2, r, randrange(3,5,1))
current_note-=(current_note%12)-7
position_in_scale = 0
current_note+=go_to_note(-1)
for i in range(8):
    r = randrange(-1,2,2)
    if current_note < 48:
        r = 1
    elif current_note > 60:
        r = -1
    sequences(2*r,randrange(0,3,1))
    patterns(2, r, randrange(3,5,1))


performance = s.stop_transcribing()
performance.to_score().show()
