# Constants for Russian LEO navigation satellites
import os
import requests
import urllib


def fetch_rover_photos(rover_name, sol, camera, api_key):
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/photos"
    params = {
        'sol': sol,
        'camera': camera,
        'api_key': api_key
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching rover photos: {e}")
        return None


def save_rover_images(photo_data, save_folder):
    try:
        photos = photo_data.get('photos', [])
        if not photos:
            print("No photos found.")
            return
        
        for photo in photos:
            img_src = photo['img_src']
            img_name = os.path.basename(img_src)
            img_path = os.path.join(save_folder, img_name)
            
            # Download the image
            urllib.request.urlretrieve(img_src, img_path)
            print(f"Image saved: {img_name}")
    except KeyError as e:
        print(f"Error accessing photo data: {e}")


