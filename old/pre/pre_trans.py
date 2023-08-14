import mido
from mido import Message, MidiFile, MidiTrack

# Define the mappings from alphabet letters to pitches
mapping = {'a': 36, 'b': 38, 'c': 40, 'd': 42, 'e': 44, 'f': 45, 'g': 47,
           'h': 48, 'i': 50, 'j': 52, 'k': 53, 'l': 55, 'm': 57, 'n': 59,
           'o': 60, 'p': 62, 'q': 64, 'r': 65, 's': 67, 't': 69, 'u': 71,
           'v': 72, 'w': 74, 'x': 76, 'y': 77, 'z': 79}

def text_to_pitch(text):
    # Convert the text to lower case
    text = text.lower()

    # Initialize the list of pitches
    pitches = []

    # Iterate over each character in the text
    for char in text:
        # If the character is in the mapping, add its corresponding pitch to the list
        if char in mapping:
            pitches.append(mapping[char])
    
    return pitches

def rhythm_based_on_word_length(word):
    return len(word) % 4 + 1

def pattern_based_on_word_length(text):
    words = text.split()
    track = MidiTrack()
    for word in words:
        rhythm = rhythm_based_on_word_length(word)
        pitches = text_to_pitch(word)
        for pitch in pitches:
            track.append(Message('note_on', note=pitch, velocity=64, time=rhythm * 480))
            track.append(Message('note_off', note=pitch, velocity=64, time=rhythm * 480))
    return track

# usage
mid = MidiFile()
text = 'hello world'
track = pattern_based_on_word_length(text)
mid.tracks.append(track)
mid.save('hello_world.mid')
