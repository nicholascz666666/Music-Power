from ui import get_user_input, select_files
from category_assignment import assign_categories
from web_scraper import login_website, scrape_website
from audio_processing import download_audio_files, merge_audio_files

# Login to the website
session = login_website('https://soundraw.io/users/sign_in')

# Get user input
user_input = get_user_input()

# Assign categories
categories = assign_categories(user_input)

# Scrape website for audio files
audio_files_urls = []
for category in categories:
    url = f'https://soundraw.io/edit_music?length=15&tempo=low,normal,high&mood={category}'
    audio_files_urls += scrape_website(url,session)

# Download audio files
audio_files = download_audio_files(audio_files_urls)

# Allow user to select and merge audio files
selected_files = select_files(audio_files)
merged_file = merge_audio_files(selected_files)

# Save the merged audio file
merged_file.export("final_audio.mp3", format="mp3")
