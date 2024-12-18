from openai import OpenAI
import os
import edge_tts
import json
import asyncio
import whisper_timestamped as whisper
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.background_video_generator import generate_video_url
from utility.render.render_engine import get_output_media
from utility.video.video_search_query_generator import getVideoSearchQueriesTimed, merge_empty_intervals
import argparse
from google.colab import files
import io

if __name__ == "__main__":
    print("Enter story language (en/hi)")
    LANGUAGE = input();

    print("Please select a file to upload...")
    uploaded = files.upload()
        
    # Process the uploaded file
    for filename, content in uploaded.items():
        print(f"\nReading file: {filename}")        
        # Convert bytes to string and read content
        scriptText = io.StringIO(content.decode('utf-8')).read()
        print(scriptText)

    SAMPLE_FILE_NAME = "audio_tts.wav"
    VIDEO_SERVER = "pexel"

    print("script: {}".format(scriptText))

    if LANGUAGE == "hi":
        voice = "hi-IN-SwaraNeural"
    else:
        voice = "en-AU-WilliamNeural"
    asyncio.run(generate_audio(scriptText, SAMPLE_FILE_NAME, voice))

    timed_captions = generate_timed_captions(SAMPLE_FILE_NAME)
    print(timed_captions)

    search_terms = getVideoSearchQueriesTimed(scriptText, timed_captions)
    print(search_terms)

    background_video_urls = None
    if search_terms is not None:
        background_video_urls = generate_video_url(search_terms, VIDEO_SERVER)
        print(background_video_urls)
    else:
        print("No background video")

    background_video_urls = merge_empty_intervals(background_video_urls)

    if background_video_urls is not None:
        video = get_output_media(SAMPLE_FILE_NAME, timed_captions, background_video_urls, VIDEO_SERVER)
        print(video)
    else:
        print("No video")
