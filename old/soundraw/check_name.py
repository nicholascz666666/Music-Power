import os
import re

def is_valid_filename(filename):
    return re.match(r'^[a-zA-Z0-9_]+\s*\(\d+\)\.[a-zA-Z0-9]+$', filename)

def rename_file(old_name):
    name, ext = os.path.splitext(old_name)
    new_name = re.sub(r'\s*\((\d+)\)', r'_\1', name)
    new_name = re.sub(r'\s+', r'_', new_name)  # Replace any remaining spaces with underscores
    new_name = new_name + ext
    return new_name

def rename_files_recursively(folder_path):
    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            old_file_path = os.path.join(dirpath, filename)
            if is_valid_filename(filename):
                new_filename = rename_file(filename)
                new_file_path = os.path.join(dirpath, new_filename)
                os.rename(old_file_path, new_file_path)
                print(f'Renamed: {old_file_path} => {new_file_path}')

if __name__ == "__main__":
    folder_path = "soundraw/"  # Replace this with the actual folder path
    rename_files_recursively(folder_path)
