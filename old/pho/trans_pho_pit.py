import nltk
import random
# nltk.download('cmudict')
from nltk.corpus import cmudict
from music21 import note, chord, stream, midi,instrument
from phonetics import nysiis,dmetaphone,metaphone
from midi2audio import FluidSynth
import subprocess
# Initialize the CMU Pronouncing Dictionary
d = cmudict.dict()

# Define a mapping from phonetic sounds to pitches
mapping = {
    'AA': 'C4', 'AE': 'C#4', 'AH': 'D4', 'AO': 'D#4', 'AW': 'E4',
    'AY': 'F4', 'B': 'F#4', 'CH': 'G4', 'D': 'G#4', 'DH': 'A4',
    'EH': 'A#4', 'ER': 'B4', 'EY': 'C5', 'F': 'C#5', 'G': 'D5',
    'HH': 'D#5', 'IH': 'E5', 'IY': 'F5', 'JH': 'F#5', 'K': 'G5',
    'L': 'G#5', 'M': 'A5', 'N': 'A#5', 'NG': 'B5', 'OW': 'C6',
    'OY': 'C#6', 'P': 'D6', 'R': 'D#6', 'S': 'E6', 'SH': 'F6',
    'T': 'F#6', 'TH': 'G6', 'UH': 'G#6', 'UW': 'A6', 'V': 'A#6',
    'W': 'B6', 'Y': 'C7', 'Z': 'C#7', 'ZH': 'D7', 'H': 'C4'
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

# # Create a new violin instrument
# violin = instrument.Violin()

# # Add the violin to the stream
# s.insert(0, violin)

# words = [dmetaphone(w) for w in words]

# For each word and chosen triad...
for word, triad in zip(words, chosen_triads):
    # Convert the word to phonetic transcription
    
    transcription = [phoneme for phoneme in d[word.lower()][0]]
    # transcription= metaphone(word)
    # transcription= list(metaphone(word))
    print(word,transcription)
    # Convert the phonetic transcription to pitches
    word_pitches = [mapping[phoneme.rstrip('012')] for phoneme in transcription if phoneme.rstrip('012') in mapping]

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
# print(s.show('text'))

# Play the stream
# sp = midi.realtime.StreamPlayer(s)
# while 1:
#     sp.play()


# Save to a MIDI file
s.write('midi', fp='output.mid')

# Initialize FluidSynth with a SoundFont
# You'll need to replace 'path/to/piano.sf2' with the path to an actual SoundFont file
fs = FluidSynth(r'SoundFont\YDP-GrandPiano-SF2-20160804\YDP-GrandPiano-20160804.sf2')

# Play the MIDI file with FluidSynth
fs.midi_to_audio('output.mid', 'output.wav')
