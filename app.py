from openai import OpenAI
import os
import edge_tts
import json
import asyncio
import whisper_timestamped as whisper
import requests
from PIL import Image
from io import BytesIO
import tempfile
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.video_search_query_generator import getVideoSearchQueriesTimed, merge_empty_intervals
from utility.render.render_engine import get_output_media

def download_pollinations_image(prompt, output_path):
    """Download image from pollinations.ai"""
    # Encode the prompt for URL
    encoded_prompt = requests.utils.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Save the image
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
    
    for i, segment in enumerate(search_terms):
        start_time, end_time, prompt = segment
        image_path = os.path.join(temp_dir, f"segment_{i}.jpg")
        
        if download_pollinations_image(prompt, image_path):
            image_segments.append({
                'start_time': start_time,
                'end_time': end_time,
                'image_path': image_path
            })
    
    return image_segments

if __name__ == "__main__":
    file = open("text-file.txt", "r+", encoding='utf-8')
    script = file.read()
    file.close()

    SAMPLE_FILE_NAME = "audio_tts.wav"

    print("script: {}".format(script))

    # Clean Hindi text
    def clean_hindi_text(text):
        import re
        cleaned = re.sub(r'[^।-॥\u0900-\u097F\s.,!?0-9]', '', text)
        cleaned = ' '.join(cleaned.split())
        return cleaned

    #script = clean_hindi_text(script)
    voice = "en-US-AriaNeural"

    try:
        communicate = edge_tts.Communicate(text=script, voice=voice)
        asyncio.run(generate_audio(script, SAMPLE_FILE_NAME, voice))
    except Exception as e:
        print(f"Error generating audio: {str(e)}")
        voice = "hi-IN-MadhurNeural"
        print(f"Trying fallback voice: {voice}")
        asyncio.run(generate_audio(script, SAMPLE_FILE_NAME, voice))

    timed_captions = generate_timed_captions(SAMPLE_FILE_NAME)
    print("timed_captions", timed_captions)

    search_terms = getVideoSearchQueriesTimed(script, timed_captions)
    print("search_terms", search_terms)

    if search_terms is not None:
        # Generate images instead of downloading videos
        image_segments = generate_images_for_segments(search_terms)
        if image_segments:
            # Modify get_output_media to handle images instead of videos
            video = get_output_media(SAMPLE_FILE_NAME, timed_captions, image_segments, "images")
            print("Video generated successfully")
        else:
            print("Failed to generate images")
    else:
        print("No search terms generated")
