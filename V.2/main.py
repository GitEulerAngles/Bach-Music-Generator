from math import floor
from random import randrange

import scamp

scamp.engraving_settings.lilypond_search_paths
print(scamp.engraving_settings.lilypond_dir)

s = scamp.Session()
s.tempo = 120

cello = s.new_part("cello")

current_note = 0
key = 0
octave = 3
position_in_scale = 0
minor_scale = [0,2,4,5,7,9,11]
harmonic_minor_scale = [0,2,4,5,8,9,11]
chordProgression = []
chords = [[0,4,9],[2,5,11],[0,4,7],[2,5,9],
          [4,7,11],[0,5,9],[2,7,11]]
scale = chords[0]

def go_to_note(note):
    global position_in_scale, octave, scale
    scale_length = len(scale)
    new_note = 0
    position_in_scale += note
    if position_in_scale < 0:
        position_in_scale = position_in_scale%scale_length
        octave -= 1
    elif position_in_scale >= scale_length:
        octave += 1
        position_in_scale = position_in_scale%scale_length
    new_note = scale[(position_in_scale)%scale_length]+(octave*12)+key
    return new_note

def sequences(iteration, interval):
    global current_note
    n = -1 - interval
    if iteration < 0:
        n = -2 - interval
    for i in range(abs(iteration)):
        for j in range(n, 3 + interval, 3 + (interval*2)):
            current_note = go_to_note(j)
            cello.play_note(current_note, 1.0, .5)

def patterns(iteration, interval, notes):
    global current_note
    note_length = []
    for i in range(abs(notes)):
        note_length.append(randrange(1, 3, 1))
    for i in range(abs(iteration)):
        for j in range(abs(notes)):
            current_note = go_to_note(interval)
            cello.play_note(current_note,1.0,1)
        if i != (iteration-1):
            current_note = go_to_note(-(interval*notes)+interval)

def generateProgression(amount_of_chords):
    dominant = [1,3,4,6]
    tonic = [0,2,5]

    progression = []

    for i in range(int(amount_of_chords/2)):
        progression.append(tonic[randrange(0,3,1)])
    for i in range(int(amount_of_chords/2)):
        progression.append(dominant[randrange(0,4,1)])
    
    return progression

measure = 0
chordProgression = generateProgression(4)

s.start_transcribing()

def generateMelody():
    global scale, measure
    fun = randrange(0,3,1)
    if fun <= 1:
        n = randrange(-1,2,2)
        if current_note > 50:
            n = -1
        elif current_note < 40:
            n = 1
        scale = chords[measure%4]
        patterns(1,n,4)
    elif fun == 2:
        n = randrange(-1,2,2)
        if current_note > 50:
            n = -1
        elif current_note < 40:
            n = 1
        r = randrange(0,2,1)
        s = randrange(0,2,1)
        if s == 0:
            scale = harmonic_minor_scale
        elif s == 1:
            scale = minor_scale
        if r == 0:
            patterns(1,n,4)
        elif r == 1:
            sequences(4,n)
    measure += 1

for i in range(32):
    generateMelody()

performance = s.stop_transcribing()
performance.to_score().show()
