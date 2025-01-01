import os
import tempfile
import requests
import base64
from urllib.parse import quote

def download_pollinations_image(prompt, output_path):
    """Generate and download image using getimg.ai API"""
    api_key = os.environ.get('GETIMP_API_KEY')
    api_url = "https://api.getimg.ai/v1/stable-diffusion-xl/text-to-image"
    
    headers = {
        "authorization": f"Bearer {api_key}",
        "content-type": "application/json",
        "accept": "application/json",
    }
    
    payload = {
        "prompt": prompt,
        "response_format": "b64",
        "style": "photorealism",
        "width": 1280,
        "height": 720,
        "output_format": "jpeg",
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=300)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Extract base64 image data from response
        image_data = response.json().get('image')
        if image_data:
            # Decode base64 and save to file
            with open(output_path, 'wb') as f:
                f.write(base64.b64decode(image_data))
            return True
        else:
            print("No image data in response")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Error generating image: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
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