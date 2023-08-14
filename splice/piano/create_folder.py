import os

MOODS = ['Happy',
    'Relaxed',
    'Inspired','Sad',
    'Stressed',
    'Frustrated']

# Specify the path where you want to create the folders
base_path = "splice\\piano\\"  # Replace with the desired folder path

# Create folders for each mood
for mood in MOODS:
    folder_path = os.path.join(base_path, mood)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder created: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")
