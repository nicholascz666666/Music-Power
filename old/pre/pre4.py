from music21 import note, chord, stream, midi, duration, instrument
import random
from midi2audio import FluidSynth
import pygame.midi
# Define a predefined mapping from letter to pitches
pitch_mapping = {
    'a': 'C2', 'b': 'D2', 'c': 'E2', 'd': 'F2', 'e': 'G2',
    'f': 'A2', 'g': 'B2', 'h': 'C3', 'i': 'D3', 'j': 'E3',
    'k': 'F3', 'l': 'G3', 'm': 'A3', 'n': 'B3', 'o': 'C4',
    'p': 'D4', 'q': 'E4', 'r': 'F4', 's': 'G4', 't': 'A4',
    'u': 'B4', 'v': 'C5', 'w': 'D5', 'x': 'E5', 'y': 'F5', 'z': 'G5'
}

# Define the 12 pitches in an octave
pitches = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Define the four types of triads
types = ['major', 'minor', 'diminished', 'augmented']

# Create a list to hold the triads
triads = []

# For each pitch and type, create a triad and add it to the list
for p in pitches:
    for t in types:
        triads.append(chord.Chord([p + '4', p + '5', p + '6'], quarterLength=1.0).closedPosition(forceOctave=4))

# Input text
text = "hello beautiful world"

# Split the text into words
words = text.split()
chosen_triads = random.sample(triads, len(words))

# Let's create a list of possible rhythms (expressed in quarterLengths)
rhythm_mapping = {
    1: [[1.0]],
    2: [[1.5, 1.0],[1.0, 1.5]],
    3: [[1.5,  1.0, 1.0], [1.0, 1.0, 1.5]],
    4: [[1.0, 1.5,  1.0, 1.0], [1.5,  1.0, 1.0, 1.0], [1.0, 1.0, 1.5, 1.0]],
    5: [[1.0, 1.0, 1.5,  1.0, 1.0], [1.5, 1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.5,  1.0],[1.0, 1.0, 1.0, 1.0, 1.5]],
    9: [[1, 0.5, 0.5, 1, 0.5, 0.5, 0.5,1, 0.5]]
    # 1: [[1.0]],
    # 2: [[1.0, 0.5, 1.0]],
    # 3: [[1.0, 0.5, 1.0, 1.0], [1.0, 1.0, 0.5, 1.0]],
    # 4: [[1.0, 1.0, 0.5, 1.0, 1.0], [1.0, 0.5, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 0.5, 1.0]],
    # 5: [[1.0, 1.0, 1.0, 0.5, 1.0, 1.0], [1.0, 0.5,1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0, 0.5, 1.0],[1.0, 1.0, 0.5, 1.0, 1.0, 1.0]]
    # 1: [[1.0]],
    # 2: [[1.5, 0.5, 1.0],[1.0, 0.5, 1.5]],
    # 3: [[1.5, 0.5, 1.0, 1.0], [1.0, 1.0, 0.5, 1.5]],
    # 4: [[1.0, 1.5, 0.5, 1.0, 1.0], [1.5, 0.5, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 0.5, 1.5]],
    # 5: [[1.0, 1.0, 1.5, 0.5, 1.0, 1.0], [1.5, 0.5,1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0, 0.5, 1.5],[1.0, 1.5, 0.5, 1.0, 1.0, 1.0]]
    # 1: [[1.5]],
    # 2: [[1.5, 1.0, 1.5]],
    # 3: [[1.5, 1.0, 1.5, 1.5], [1.5, 1.5, 1.0, 1.5]],
    # 4: [[1.5, 1.5, 1.0, 1.5, 1.5], [1.5, 1.0, 1.5, 1.5, 1.5], [1.5, 1.5, 1.5, 1.0, 1.5]],
    # 5: [[1.5, 1.5, 1.5, 1.0, 1.5, 1.5], [1.5, 1.0, 1.5, 1.5, 1.5, 1.5], [1.5, 1.5, 1.5, 1.5, 1.0, 1.5], [1.5, 1.5, 1.0, 1.5, 1.5, 1.5]]
    # 1: [[1.25]],
    # 2: [[1.25, 0.75, 1.25]],
    # 3: [[1.25, 0.75, 1.25, 1.25], [1.25, 1.25, 0.75, 1.25]],
    # 4: [[1.25, 1.25, 0.75, 1.25, 1.25], [1.25, 0.75, 1.25, 1.25, 1.25], [1.25, 1.25, 1.25, 0.75, 1.25]],
    # 5: [[1.25, 1.25, 1.25, 0.75, 1.25, 1.25], [1.25, 0.75, 1.25, 1.25, 1.25, 1.25], [1.25, 1.25, 1.25, 1.25, 0.75, 1.25],[1.25, 1.25, 0.75, 1.25, 1.25, 1.25]]
    # Add more patterns for different word lengths as needed...
}

# Function to get a combination of patterns that matches a specific length
def get_combination(n):
    if n in rhythm_mapping:  # if the length is already in the mapping, return a random pattern of that length
        return random.choice(rhythm_mapping[n])
    else:  # if not, try to combine smaller patterns
        keys = list(rhythm_mapping.keys())
        random.shuffle(keys)  # shuffle the keys to get random combinations
        for key in keys:
            if key < n:  # if the key is smaller than the target length...
                remainder = n - key  # calculate the remainder
                remainder_combination = get_combination(remainder)  # recursively try to find a combination for the remainder
                if remainder_combination:  # if a combination for the remainder is found...
                    return random.choice(rhythm_mapping[key]) + remainder_combination  # combine it with the current key and return the combination
    return None  # if no combination is found, return None

# Create a music21 stream
s = stream.Stream()

# For each word and chosen triad...
for word, triad in zip(words, chosen_triads):
    # Convert the word to list of letters
    letters = list(word.lower())
    
    # Convert the phonetic transcription to pitches
    word_pitches = [pitch_mapping[l] for l in letters]

    # Print the pitches for the word
    print(f"Pitches for '{word}': {word_pitches}")
    
    # Determine a rhythm pattern based on the number of letters in the word
    word_length = len(word)
    rhythm_pattern = get_combination(word_length)
    if not rhythm_pattern:  # if no combination is found, default to all quarter notes
        rhythm_pattern = [1.0]*word_length

    # Create a new chord from the pitches of the chosen triad
    new_triad = chord.Chord(triad.pitches)
    
    # Set the duration of the chord to the total rhythm pattern duration
    new_triad.duration = duration.Duration(1.5)
    
    # Add the chord to the stream
    s.append(new_triad)

    # For each pitch and rhythm in the word...
    for p, r in zip(word_pitches, rhythm_pattern):
        if r == 0:  # if the rhythm value is 0, add a rest instead of a note
            s.append(note.Rest(quarterLength=r))
        else:
            # Create a note from the pitch
            n = note.Note(p)

            # Set the duration of the note based on the rhythm pattern
            n.duration = duration.Duration(r)

            # Add the note to the stream
            s.append(n)
    # Add a rest to the stream
    s.append(note.Rest(quarterLength=0.5))

# Save the stream as a MIDI file
s.write('midi', fp='output44.mid')

# # Initialize the pygame.midi module
# pygame.midi.init()

# # Open a MIDI output device
# output_device = pygame.midi.Output(0)
# output_device.set_instrument(0)

# # Load the MIDI file
# midi_file = pygame.midi.MidiFile()
# midi_file.open('output.mid')

# # Play each MIDI event
# for i in range(midi_file.length()):
#     event = midi_file.read(1)[0][0]
#     output_device.write(event)

# # Close the MIDI output device
# output_device.close()

# # Quit the pygame.midi module
# pygame.midi.quit()
# Initialize FluidSynth with a SoundFont
# You'll need to replace 'path/to/piano.sf2' with the path to an actual SoundFont file
fs = FluidSynth(r'pho\SoundFont\YDP-GrandPiano-SF2-20160804\YDP-GrandPiano-20160804.sf2')

# Play the MIDI file with FluidSynth
fs.midi_to_audio('output44.mid', 'output44.wav')