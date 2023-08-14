from music21 import note, chord, stream, midi, duration, instrument
import random
from midi2audio import FluidSynth
import pygame.midi
import nltk
nltk.download('punkt')
from nltk import sent_tokenize
from textblob import TextBlob

# Define the pitch mapping from 'C2' to 'G5'
all_pitches = ['C',  'D','E', 'F', 'G',  'A',  'B']
all_octaves = [2, 3, 4, 5]
all_notes = [p + str(o) for o in all_octaves for p in all_pitches]
index_mapping = {note: i for i, note in enumerate(all_notes)}  # store the index of each note for easy lookup
# Get the index range of valid notes ('C2' to 'G5')
start_index = index_mapping['C2']
end_index = index_mapping['G5']

# Define the 12 pitches in an octave
pitches =['C',  'D',  'E', 'F', 'G',  'A',  'B']

# Define the four types of triads
types = ['major', 'minor', 'diminished', 'augmented']

# Create a list to hold the triads
triads = []

# For each pitch and type, create a triad and add it to the list
for p in pitches:
    for t in types:
        triads.append(chord.Chord([p + '4', p + '5', p + '6'], quarterLength=1.0).closedPosition(forceOctave=4))

# Input text
text = "I am so happy with my new phone. but the weather is terrible outside."
# text = '''The sun rose on a beautiful morning, painting the sky with vibrant hues. Birds chirped joyfully, 
# celebrating the new day, while the flowers bloomed, spreading their sweet fragrance. In a quaint little village, 
# the townspeople gathered to celebrate a long-awaited event - the annual harvest festival. Laughter and cheer filled the 
# air as families and friends reunited, sharing stories and memories. Meanwhile, not far away, a young man named Jack felt a heavy
#  weight on his heart. He had recently lost his job, leaving him feeling defeated and uncertain about the future. 
#  As the festivities continued, he couldn't shake off the sense of failure that consumed him. However, amidst the revelry, 
#  a chance encounter with an old friend brought hope back into Jack's life. They shared tales of perseverance and resilience, inspiring
#    him to believe in himself again. While the day was filled with both highs and lows, the underlying message of the day 
#    resonated deeply with everyone - that life's journey is a mix of positive and negative sentiments, 
#    and it is in unity and support that we find strength to overcome challenges.'''

# Split the text into words
words = text.split()
chosen_triads = [random.choice(triads) for _ in words]


# Let's create a list of possible rhythms (expressed in quarterLengths)
rhythm_mapping = {
    1: [[1.0]],
    2: [[1.0, 0.5, 1.0],[1.0, 0.5, 0.5], [0.5, 0.5, 0.5]],
    3: [[1.5, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.5]],
    4: [[1.5, 1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.5, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0, 1.0]],
    5: [[1.5, 1.0, 1.0, 1.0, 1.5, 1.0], [1.5, 1.0,1.0, 1.5, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0, 1.5, 1.5],[1.5, 1.0, 1.5, 1.5, 1.5, 1.5]]#,
    # 9: [[1, 0.5, 0.5, 1, 0.5, 0.5, 0.5,1, 0.5]]
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

# Use NLTK's sent_tokenize to split the text into sentences
sentences = sent_tokenize(text)

for sentence in sentences:
    # Use TextBlob to determine the sentiment of each sentence
    sentiment = TextBlob(sentence).sentiment.polarity
    print(f"Sentence: {sentence}")
    print(f"Sentiment: {sentiment}")

    # Split the sentence into words
    words = sentence.split()
    chosen_triads = [random.choice(triads) for _ in words]

    # Initialize a variable to store the first pitch of the previous word
    prev_first_pitch_index = None
    # For each word and chosen triad...
    for word, triad in zip(words, chosen_triads):
        if sentiment > 0:  # positive sentiment
            # Get the index range of valid notes ('C4' to 'B5')
            start_index = index_mapping['C4']
            end_index = index_mapping['B5']
        else:  # negative sentiment
            # Get the index range of valid notes ('C2' to 'B3')
            start_index = index_mapping['C2']
            end_index = index_mapping['B3']
        if prev_first_pitch_index is None:  # if this is the first word...
            # Select the first pitch randomly from the list
            first_pitch_index = random.randint(start_index, end_index)
        else:  # if this is not the first word...
            # Determine the range of valid first pitches (within 3 gaps from the first pitch of the previous word)
            first_pitch_min_index = max(start_index, prev_first_pitch_index - 3)
            first_pitch_max_index = min(end_index, prev_first_pitch_index + 3)

            # Select the first pitch randomly from the valid range
            first_pitch_index = random.randint(first_pitch_min_index, first_pitch_max_index)

        first_pitch = all_notes[first_pitch_index]

        # Determine the range of valid chords for the word
        chord_min_index = max(start_index, first_pitch_index - 3)
        chord_max_index = min(end_index, first_pitch_index + 3)
        
        # Select a chord randomly from the valid range
        valid_chords = [chord for chord in triads if chord_min_index <= index_mapping[chord.root().nameWithOctave] <= chord_max_index]
        triad = random.choice(valid_chords) if valid_chords else random.choice(triads)  # if no valid chords are found, default to any random chord

        # Initialize the word_pitches list with the first pitch
        word_pitches = [first_pitch]

            # For the rest of the letters in the word...
        for _ in range(1, len(word)):
            # Determine the range of valid next pitches (within 2 gaps from the previous pitch)
            prev_pitch_index = index_mapping[word_pitches[-1]]
            next_pitch_min_index = max(start_index, prev_pitch_index - 2)
            next_pitch_max_index = min(end_index, prev_pitch_index + 2)

            while True:  # loop until a valid next pitch is selected
                # Select the next pitch randomly from the valid range
                next_pitch_index = random.randint(next_pitch_min_index, next_pitch_max_index)
                next_pitch = all_notes[next_pitch_index]

                # Check if the last two pitches in the word_pitches list are the same as the next pitch
                if len(word_pitches) >= 2 and word_pitches[-1] == word_pitches[-2] == next_pitch:
                    continue  # if they are the same, continue to select a new next pitch
                else:
                    break  # if they are not the same, break the loop to keep the selected next pitch

            # Add the next pitch to the word_pitches list
            word_pitches.append(next_pitch)

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
        s.append(note.Rest(quarterLength=0.75))



# Save the stream as a MIDI file
s.write('midi', fp='pre6.mid')
fs = FluidSynth(r'pho\SoundFont\YDP-GrandPiano-SF2-20160804\YDP-GrandPiano-20160804.sf2')

# Play the MIDI file with FluidSynth
fs.midi_to_audio('pre6.mid', 'pre6.wav')