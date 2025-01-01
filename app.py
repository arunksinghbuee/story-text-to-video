from openai import OpenAI
import os
import edge_tts
import asyncio
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.video_search_query_generator import getVideoSearchQueriesTimed
from utility.image.background_image_generator import generate_images_for_segments
from utility.render.render_engine import get_output_media

def review_search_terms(search_terms):
    """Interactive review and update of search terms"""
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
    
    return updated_terms

def main():
    # Read input script
    with open("text-file.txt", "r+", encoding='utf-8') as file:
        script = file.read()

    SAMPLE_FILE_NAME = "audio_tts.wav"
    print("script: {}".format(script))

    # Generate audio with fallback
    voice = "en-US-AriaNeural"
    try:
        asyncio.run(generate_audio(script, SAMPLE_FILE_NAME, voice))
    except Exception as e:
        print(f"Error generating audio: {str(e)}")
        voice = "hi-IN-MadhurNeural"
        print(f"Trying fallback voice: {voice}")
        asyncio.run(generate_audio(script, SAMPLE_FILE_NAME, voice))

    # Generate captions and search terms
    timed_captions = generate_timed_captions(SAMPLE_FILE_NAME)
    print("timed_captions", timed_captions)

    search_terms = getVideoSearchQueriesTimed(script, timed_captions)
    print("\nInitial search terms:", search_terms)

    if search_terms is not None:
        # Review and update search terms
        search_terms = review_search_terms(search_terms)
        print("\nFinal search terms:", search_terms)

        # Generate images and video
        image_segments = generate_images_for_segments(search_terms)
        if image_segments:
            video_path = get_output_media(SAMPLE_FILE_NAME, timed_captions, image_segments)
            print(f"Video generated successfully: {video_path}")
        else:
            print("Failed to generate images")
    else:
        print("No search terms generated")

if __name__ == "__main__":
    main()
