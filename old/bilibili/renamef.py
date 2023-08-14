import os
from pypinyin import lazy_pinyin
import re

# Folder path where the files are located
folder_path = 'bilibili\\all_audios\\'

# List all files in the folder
files = os.listdir(folder_path)

# Regular expression to match the pattern xxxxxxxxxxxx《中文》xxxxxxxx.mp3
pattern = re.compile(r'(.*)《(.*?)》(.*).mp3')

for file_name in files:
    # Apply the regular expression to each file name
    match = pattern.match(file_name)
    
    if match:
        # Extract parts of the filename
        prefix = match.group(1)
        chinese_part = match.group(2)
        suffix = match.group(3)
        
        # Convert Chinese characters to Pinyin
        pinyin_part = ''.join(lazy_pinyin(chinese_part))
        
        # Create the new file name
        new_file_name = f'{pinyin_part}.mp3'
        
        # Rename the file
        old_path = os.path.join(folder_path, file_name)
        new_path = os.path.join(folder_path, new_file_name)
        os.rename(old_path, new_path)
        
        print(f'Renamed: {file_name} -> {new_file_name}')
