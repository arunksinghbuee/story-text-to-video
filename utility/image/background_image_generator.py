import os
import tempfile
import requests
from urllib.parse import quote

def download_pollinations_image(prompt, output_path):
    """Download image from pollinations.ai"""
    encoded_prompt = quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"Error downloading image: {e}")
    return False

def generate_images_for_segments(search_terms):
    """Generate images for each time segment"""
    image_segments = []
    temp_dir = tempfile.mkdtemp()
    
    for segment in search_terms:
        time_range, prompts = segment
        start_time, end_time = time_range
        
        image_path = os.path.join(temp_dir, f"segment_{len(image_segments)}.jpg")
        success = False
        
        for prompt in prompts:
            if download_pollinations_image(prompt, image_path):
                image_segments.append({
                    'start_time': start_time,
                    'end_time': end_time,
                    'image_path': image_path
                })
                success = True
                break
        
        if not success:
            print(f"Failed to generate image for segment {start_time}-{end_time}")
    
    return image_segments