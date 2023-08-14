from ui import main_input, select_files,music_ready_page,magic_starts_page
from category_assignment import assign_categories
from audio_processing import get_audio_files, merge_selected_files

# Start the application
user_words = main_input()

# Process each word and gather the selected files
selected_files = []
for word in user_words.split():
    categories = assign_categories(word)
    audio_files = get_audio_files(categories)
    selected_file = select_files(word, audio_files)
    selected_files.append(selected_file)

# Merge the selected files and play the music
merge_selected_files(selected_files)
magic_starts_page()
music_ready_page("userselection//output//output.wav")
