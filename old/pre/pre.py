from music21 import note, chord, stream, midi,instrument
import random


# Define a predefine mapping from letter to pitches
pitch_mapping = {
    'a': 'C2', 'b': 'D2', 'c': 'E2', 'd': 'F2', 'e': 'G2',
    'f': 'A2', 'g': 'B2', 'h': 'C3', 'i': 'D3', 'j': 'E3',
    'k': 'F3', 'l': 'G3', 'm': 'A3', 'n': 'B3', 'o': 'C4',
    'p': 'D4', 'q': 'E4', 'r': 'F4', 's': 'G4', 't': 'A4',
    'u': 'B4', 'v': 'C5', 'w': 'D5', 'x': 'E5', 'y': 'F5','z': 'G5'
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
# Create a music21 stream
s = stream.Stream()


# For each word and chosen triad...
for word, triad in zip(words, chosen_triads):
    # Convert the word to list of letters
    letters = list(word.lower())
    print(letters)
    # Convert the phonetic transcription to pitches
    word_pitches = [pitch_mapping[l] for l in letters]

    # Create a new chord from the pitches of the chosen triad
    new_triad = chord.Chord(triad.pitches)
    # Set the duration of the chord to the number of pitches in the word
    new_triad.duration.quarterLength = 2#len(word_pitches)
    # Add the chord to the stream
    s.append(new_triad)
    # For each pitch in the word...
    for p in word_pitches:
        print(p)
        # Create a note from the pitch
        n = note.Note(p)

        # Set the duration of the note to 1/3 of a quarter note
        n.duration.quarterLength = 1

        # Add the note to the stream
        s.append(n)

    # Add a rest to the stream
    s.append(note.Rest(quarterLength=0.5))

# Play the stream
sp = midi.realtime.StreamPlayer(s)
while 1:
    sp.play()