from music21 import note, chord, stream, midi, duration, instrument
import random

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
rhythm_values = [0.25, 0.5, 1.0, 1.5, 2.0]

# Create a music21 stream
s = stream.Stream()

# For each word and chosen triad...
for word, triad in zip(words, chosen_triads):
    # Convert the word to list of letters
    letters = list(word.lower())
    
    # Convert the phonetic transcription to pitches
    word_pitches = [pitch_mapping[l] for l in letters]
    
    # Determine a rhythm pattern based on the number of letters in the word
    word_length = len(word)
    rhythm_pattern = [rhythm_values[i % len(rhythm_values)] for i in range(word_length)]

    # Create a new chord from the pitches of the chosen triad
    new_triad = chord.Chord(triad.pitches)
    
    # Set the duration of the chord to the total rhythm pattern duration
    new_triad.duration = duration.Duration(sum(rhythm_pattern))
    
    # Add the chord to the stream
    s.append(new_triad)

    # For each pitch and rhythm in the word...
    for p, r in zip(word_pitches, rhythm_pattern):
        # Create a note from the pitch
        n = note.Note(p)

        # Set the duration of the note based on the rhythm pattern
        n.duration = duration.Duration(r)

        # Add the note to the stream
        s.append(n)

    # Add a rest to the stream
    s.append(note.Rest(quarterLength=0.25))

# Play the stream
sp = midi.realtime.StreamPlayer(s)
while 1:
    sp.play()
