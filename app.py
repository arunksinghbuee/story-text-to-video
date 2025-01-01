from openai import OpenAI
import os
import edge_tts
import asyncio
import whisper_timestamped as whisper
import requests
from PIL import Image
import tempfile
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.video_search_query_generator import getVideoSearchQueriesTimed
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
    
    for segment in search_terms:
        time_range, prompts = segment  # Unpack the correct format
        start_time, end_time = time_range
        
        # Try each prompt in the list until one works
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
    print("\nInitial search terms:", search_terms)

    # Interactive review and update of search terms
    if search_terms is not None:
        print("\nReview and update search terms. Enter 'done' when finished.")
        updated_terms = []
        
        for i, segment in enumerate(search_terms):
            time_range, prompts = segment
            start_time, end_time = time_range
            
            print(f"\nSegment {i+1} ({start_time}-{end_time}):")
            print(f"Current prompts: {prompts}")
            
            user_input = input("Enter new prompts (comma-separated) or press Enter to keep current: ")
            
            if user_input.strip().lower() == 'done':
                break
            elif user_input.strip():
                new_prompts = [p.strip() for p in user_input.split(',')]
                updated_terms.append([[start_time, end_time], new_prompts])
            else:
                updated_terms.append(segment)

        search_terms = updated_terms
        print("\nFinal search terms:", search_terms)

        # Generate images with updated search terms
        image_segments = generate_images_for_segments(search_terms)
        if image_segments:
            video = get_output_media(SAMPLE_FILE_NAME, timed_captions, image_segments, "images")
            print("Video generated successfully")
        else:
            print("Failed to generate images")
    else:
        print("No search terms generated")
