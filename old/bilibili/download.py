import os
import youtube_dl

# Paths and URLs
url_file_path = 'bilibili\\all_audio.txt'  # Path to the text file with URLs
target_folder = 'bilibili\\all_audios\\'  # Path to the target download folder

# # Create target folder if not exists
# if not os.path.exists(target_folder):
#     os.makedirs(target_folder)

# # Define options for youtube_dl
# ydl_opts = {
#     'format': 'best',  # Download the best available quality
#     'outtmpl': os.path.join(target_folder, '%(id)s.%(ext)s'),  # Output template
# }

# # Read URLs from file and download videos
# with open(url_file_path, 'r') as url_file:
#     for url in url_file:
#         url = url.strip()  # Remove leading/trailing whitespace
#         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#             info_dict = ydl.extract_info(url, download=False)
#             video_id = info_dict.get('id', None)
#             video_title = info_dict.get('title', '')

#             # Check if the title contains "C"
#             if 'C' in video_title:
#                 video_path = os.path.join(target_folder, f'{video_id}.mp4')

#                 if not os.path.exists(video_path):
#                     ydl.download([url])
#                     print(f'Downloaded: {url}')
#                 else:
#                     print(f'Skipped (already downloaded): {url}')
#             else:
#                 print(f'Skipped (title does not include "C"): {url}')

# Read URLs from file
with open(url_file_path, 'r') as file:
    urls = [line.strip() for line in file]

# Options for youtube-dl
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(target_folder, '%(title)s.%(ext)s'),  # Save file as <title>.<extension>
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '640',
    }],
}

for url in urls:
    try:
        # Get the title of the video
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
            # Check if the file already exists
            if os.path.exists(target_folder+video_title + '.mp3'):
                print(f"The file {video_title}.mp3 already exists, skipping...")
                continue

            # Download the audio
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
    except Exception as e:
        print(f"Error downloading {url}: {e}, skipping to the next one...")
        continue

