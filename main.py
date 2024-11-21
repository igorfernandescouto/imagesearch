import os
import requests
from PIL import Image, UnidentifiedImageError
import cv2
import numpy as np
from io import BytesIO

# chave de API do Bing Search
BING_SEARCH_API_KEY = 'f386fd97dbd54d7d89dba680de8a151b'
BING_SEARCH_URL = "https://api.bing.microsoft.com/v7.0/images/search"

def search_images(query, count=10, offset=0):
    headers = {"Ocp-Apim-Subscription-Key": BING_SEARCH_API_KEY}
    params = {
        "q": query,
        "count": count,
        "offset": offset,
        "safeSearch": "Off"  # Desativa o SafeSearch
    }
    response = requests.get(BING_SEARCH_URL, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    return [img["contentUrl"] for img in search_results["value"]]

def load_images_from_urls(urls):
    images = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/"
    }
    for url in urls:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            images.append((url, img))
        except (requests.RequestException, UnidentifiedImageError):
            continue
    return images

def filter_images(query, min_width, min_height, desired_count):
    urls = search_images(query, count=desired_count)
    images = load_images_from_urls(urls)
    filtered_images = []
    for url, img in images:
        if (min_width == "x" or img.width >= int(min_width)) and (min_height == "x" or img.height >= int(min_height)):
            filtered_images.append((url, img))
        if len(filtered_images) >= desired_count:
            break
    return filtered_images

def save_images(images, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    for url, img in images:
        img_name = os.path.join(folder, os.path.basename(url))
        img.save(img_name)

if __name__ == "__main__":
    query = "volante"
    min_width = "x"  # Use "x" para qualquer largura
    min_height = "x"  # Use "x" para qualquer altura
    desired_count = 10  # Número desejado de imagens válidas
    selected_images = filter_images(query, min_width, min_height, desired_count)
    save_images(selected_images, 'imagens')
    print("Selected images saved in 'imagens' folder.")