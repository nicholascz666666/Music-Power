import requests
import random

from PIL import Image
from io import BytesIO

def get_images_from_pexels(query, aspect_ratios=[(4, 3), (3, 2), (16, 9), (16, 10)], max_results=4):
    PEXELS_API_URL = "https://api.pexels.com/v1/search"
    HEADERS = {
        "Authorization": "4hewugLQRyU9zGWLVF73z03LCUXU4rys2CZ6cWcWgFv9NZffMGdR5q5I"
    }
    PARAMS = {
        "query": query,
        "per_page": 30 # Fetch 30 images
    }
    response = requests.get(PEXELS_API_URL, headers=HEADERS, params=PARAMS)
    if response.status_code == 200:
        json_response = response.json()
        photos = json_response["photos"]
        selected_photos = []
        for photo in photos:
            width = photo["width"]
            height = photo["height"]
            # Check if the aspect ratio matches any of the given ratios
            if any(width / height == ar[0] / ar[1] for ar in aspect_ratios):
                selected_photos.append(photo)

        # Make sure there are enough photos to sample
        if len(selected_photos) >= max_results:
            chosen_photos = random.sample(selected_photos, max_results)
        else:
            print(f"Warning: Only found {len(selected_photos)} images with the required aspect ratio(s).")
            chosen_photos = selected_photos

        # Download and save the images
        saved_images = []
        for i, photo in enumerate(chosen_photos):
            url = photo["src"]["medium"]
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            path = f"splice\\tmp_image\\temp_image_{i}.jpg"
            img.save(path)
            saved_images.append(path)
        
        return saved_images
    else:
        print(f"Failed to fetch images from Pexels. Error Code: {response.status_code}")
        return None

# print(get_images_from_pexels("night"))