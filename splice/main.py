# from ui2 import main_input, select_files,music_ready_page,magic_starts_page
# from category_assignment import assign_categories
# from audio_processing import get_audio_files, merge_selected_files
# import threading

# # Start the application
# user_words = main_input()

# # Process each word and gather the selected files
# selected_files = []
# selected_icons = []
# for word in user_words.split():
#     sentiment_score, categories = assign_categories(word)
#     audio_files = get_audio_files(categories,selected_files)
#     selected_file = select_files(word, audio_files,sentiment_score,selected_icons)
#     selected_files.append(selected_file)

# merge_selected_files(selected_files)
# magic_starts_page(len(selected_files))
# music_ready_page("splice\output\output.wav")

from ui2 import main_input, select_files, music_ready_page, magic_starts_page
from category_assignment import assign_categories
from audio_processing import get_audio_files, merge_selected_files
import threading
import time
import sys

def main():
    # Start the application
    user_words = main_input()

    # Process each word and gather the selected files
    selected_files = []
    selected_icons = []
    for word in user_words.split():
        sentiment_score, categories = assign_categories(word)
        audio_files = get_audio_files(categories, selected_files)
        selected_file = select_files(word, audio_files, sentiment_score, selected_icons)
        selected_files.append(selected_file)

    if None in selected_files:
        sys.exit()

    # Number of files
    num_files = len(selected_files)

    # Create a thread to handle the merging of selected files
    merge_thread = threading.Thread(target=merge_selected_files, args=(selected_files,))

    # Start the merging thread
    merge_thread.start()

    # Display the magic starts page with a progress bar
    magic_starts_page(num_files)

    # Wait for the merge thread to finish
    merge_thread.join()

    # Proceed to the music ready page
    music_ready_page("splice\output\output.wav")

if __name__ == "__main__":
    main()

