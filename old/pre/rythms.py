import mido
from mido import MidiFile, MidiTrack, Message
from midi2audio import FluidSynth
# Define some parameters
tempo = mido.bpm2tempo(120)
ticks_per_beat = 480
pitches = [60, 62, 64, 65, 67, 69, 71, 72] # These are MIDI pitches, where 60 is middle C
durations = [1, 0.5, 0.5, 1, 0.5, 0.5, 1, 0.5] # These are durations in beats

# Create a new MIDI file and a track
mid = MidiFile(ticks_per_beat=ticks_per_beat)
track = MidiTrack()
mid.tracks.append(track)

# Add tempo meta message
track.append(mido.MetaMessage('set_tempo', tempo=tempo))

# Create notes
for pitch, duration in zip(pitches, durations):
    ticks = int(duration * ticks_per_beat)
    track.append(Message('note_on', note=pitch, velocity=64, time=0))
    track.append(Message('note_off', note=pitch, velocity=64, time=ticks))

# Save the MIDI file
mid.save('rhythm_example.mid')
fs = FluidSynth(r'pho\SoundFont\YDP-GrandPiano-SF2-20160804\YDP-GrandPiano-20160804.sf2')

# Play the MIDI file with FluidSynth
fs.midi_to_audio('rhythm_example.mid', 'rhythm_example.wav')