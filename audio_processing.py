import os
import random
from pydub import AudioSegment
# import pygame
# import tempfile
# import wave
# import shutil
# import sounddevice as sd
# import numpy as np
import time
from pydub.silence import detect_nonsilent
PATH=r"splice\\piano\\"



def get_audio_files(categories, selected_files):
    def get_pitch(file_name):
        return file_name.split("_")[-1][0]

    def is_within_gap(pitch1, pitch2, gap=2):
        pitch_order = 'CDEFGAB'
        diff = abs(pitch_order.index(pitch1) - pitch_order.index(pitch2))
        return diff <= gap

    category_names = [category[0] for category in categories]
    chosen_files = []
    num_files_to_choose = [2, 2] if len(category_names) > 1 else [4]

    for i, category in enumerate(category_names):
        paths = PATH + category
        all_files = [os.path.join(paths, f) for f in os.listdir(paths) if os.path.isfile(os.path.join(paths, f))]

        if selected_files:
            current_pitch = get_pitch(selected_files[-1])
            filtered_files = [f for f in all_files if is_within_gap(current_pitch, get_pitch(f))]
            chosen_files.extend(random.sample(filtered_files, min(num_files_to_choose[i], len(filtered_files))))
        else:
            chosen_files.extend(random.sample(all_files, min(num_files_to_choose[i], len(all_files))))

    return chosen_files

# def get_audio_files(categories,selected_files):
#     category_names = [category[0] for category in categories]
#     chosen_files = []
#     num_files_to_choose = [2, 1] if len(category_names) > 1 else [3]

#     for i, category in enumerate(category_names):
#         paths = PATH + category
#         all_files = [os.path.join(paths, f) for f in os.listdir(paths) if os.path.isfile(os.path.join(paths, f))]
#         chosen_files.extend(random.sample(all_files, min(num_files_to_choose[i], len(all_files))))  # Ensure not to sample more files than available

#     return chosen_files


def merge_selected_files(input_files):
    combined = AudioSegment.empty()

    # Iterate through input_files and process each one
    for infile_path in input_files:
        print(f"Processing file: {infile_path}")

        # Load the audio file
        audio = AudioSegment.from_wav(infile_path)

        # Detect non-silent parts
        non_silence = detect_nonsilent(audio, min_silence_len=2000, silence_thresh=-50)

        # Find the end of the last non-silent part (in milliseconds)
        end_time = non_silence[-1][1]

        # Subtract 2000 milliseconds (1 seconds) from the end time
        new_end_time = end_time 

        # Trim the audio file to the new end time
        trimmed_audio = audio[:new_end_time]

        # Concatenate the trimmed audio
        combined += trimmed_audio

    # Save the merged audio to the target file
    combined.export("splice//output//output.wav", format="wav")




# def merge_selected_files(input_files):
#     combined = AudioSegment.empty()

#     # Iterate through input_files and read each one
#     for infile_path in input_files:
#         print(f"Processing file: {infile_path}")
#         sound = AudioSegment.from_wav(infile_path)

#         # Exclude the last 2 seconds from each file
#         frames_to_exclude = 2 * 1000  # 2 seconds in milliseconds
#         sound = sound[:-frames_to_exclude]

#         # Concatenate the sound
#         combined += sound

#     # Create a temporary file
#     temp_output = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
#     combined.export(temp_output.name, format="wav")

#     return temp_output.name


# def merge_selected_files(selected_files_global):
#     # Code to merge selected files
#     return merge_audio_files(selected_files_global)



# def merge_audio_files(input_files):
#     output_file = r"userselection//output//output.wav"
#     # Open the output file
#     with wave.open(output_file, 'wb') as outfile:
#         # Iterate through input_files and read each one
#         for infile_path in input_files:
#             with wave.open(infile_path, 'rb') as infile:
#                 # If this is the first file, set all output parameters
#                 if outfile.getnframes() == 0:
#                     outfile.setparams(infile.getparams())
#                 # Read frames from infile and write to outfile
#                 outfile.writeframes(infile.readframes(infile.getnframes()))

# def merge_audio_files(input_files):
#     # Create a temporary file
#     temp_output = tempfile.NamedTemporaryFile(delete=False)
#     temp_output.close()

#     # Open the first input file to get its parameters
#     with wave.open(input_files[0], 'rb') as infile:
#         params = infile.getparams()

#     # Open the output file and set its parameters
#     with wave.open(temp_output.name, 'wb') as outfile:
#         outfile.setparams(params)

#         # Iterate through input_files and read each one
#         for infile_path in input_files:
#             with wave.open(infile_path, 'rb') as infile:
#                 # Calculate the number of frames to exclude (2 seconds)
#                 frames_to_exclude = 2 * infile.getframerate()

#                 # Read frames from infile, up to 2 seconds before the end, and write to outfile
#                 frames_to_read = infile.getnframes() - frames_to_exclude
#                 frames = infile.readframes(frames_to_read)
#                 outfile.writeframes(frames)
#     # Move the temporary file to the desired output path
#     shutil.move(temp_output.name, "userselection/output/output.wav")
#     return temp_output.name
# def merge_audio_files(input_files):
#     output_file = r"userselection//output//output.wav"
#     # Open the output file
#     with wave.open(output_file, 'wb') as outfile:
#         params_set = False
#         # Iterate through input_files and read each one
#         for infile_path in input_files:
#             with wave.open(infile_path, 'rb') as infile:
#                 # If this is the first file, set all output parameters
#                 if not params_set:
#                     outfile.setparams(infile.getparams())
#                     params_set = True

#                 # Calculate the number of frames to exclude (2 seconds)
#                 frames_to_exclude = 2 * infile.getframerate()

#                 # Read frames from infile, up to 2 seconds before the end, and write to outfile
#                 frames_to_read = infile.getnframes() - frames_to_exclude
#                 frames = infile.readframes(frames_to_read)
#                 outfile.writeframes(frames)
#     return output_file

# print(merge_selected_files(["soundraw\Angry\Trap__BPM70_1.wav","soundraw\Angry\Trap__BPM200.wav"]))

# # Load two wav files
# sound1 = AudioSegment.from_wav("soundraw\Angry\Trap__BPM70_1.wav")
# sound2 = AudioSegment.from_wav("soundraw\Angry\Trap__BPM200.wav")

# # Apply some effect to one of the files (optional)
# sound2 = sound2 # Increase the volume of the second sound
# sound1 = sound1 -10  # Increase the volume of the second sound
# # Merge the two wav files
# combined_sound = sound1.overlay(sound2)

# # Convert to raw audio data
# raw_audio_data = np.array(combined_sound.get_array_of_samples())

# # Play the combined sound
# sd.play(raw_audio_data, samplerate=combined_sound.frame_rate)

# # Wait for playback to finish
# sd.wait()