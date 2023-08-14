import os

folder_path = 'icons\\NEG\\'  # Replace with your folder path
files = sorted(os.listdir(folder_path))

count = 31
for file in files:
    extension = os.path.splitext(file)[1]
    if extension:  # Check if the file has an extension
        new_name = str(count) + extension
        src = os.path.join(folder_path, file)
        dst = os.path.join(folder_path, new_name)
        os.rename(src, dst)
        count += 1
