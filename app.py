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

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Generate a video from a topic.")
    # parser.add_argument("language", type=str, help="Language of the topic Ex: en/hi")
    # parser.add_argument("scriptText", type=str, help="The topic for the video")

    # args = parser.parse_args()
    # script = args.scriptText
    # LANGUAGE = args.language

    file = open("text-file.txt", "r+", encoding='utf-8')
    script = file.read()
    file.close()

    # # Clean Hindi text
    # def clean_hindi_text(text):
    #     # Remove special characters but keep Hindi characters and basic punctuation
    #     import re
    #     # Keep Hindi characters (0900-097F), numbers, basic punctuation
    #     cleaned = re.sub(r'[^।-॥\u0900-\u097F\s.,!?0-9]', '', text)
    #     # Remove extra whitespace
    #     cleaned = ' '.join(cleaned.split())
    #     return cleaned

    # script = clean_hindi_text(script)

    SAMPLE_FILE_NAME = "audio_tts.wav"
    VIDEO_SERVER = "pexel"

    print("script: {}".format(script))

    voice = "en-AU-WilliamNeural"

    # if LANGUAGE == "hi":
    #     voice = "hi-IN-SwaraNeural"
    # else:
    #     voice = "en-AU-WilliamNeural"
    asyncio.run(generate_audio(script, SAMPLE_FILE_NAME, voice))

    # timed_captions = generate_timed_captions(SAMPLE_FILE_NAME)
    # print(timed_captions)

    # search_terms = getVideoSearchQueriesTimed(scriptText, timed_captions)
    # print(search_terms)

    # background_video_urls = None
    # if search_terms is not None:
    #     background_video_urls = generate_video_url(search_terms, VIDEO_SERVER)
    #     print(background_video_urls)
    # else:
    #     print("No background video")

    # background_video_urls = merge_empty_intervals(background_video_urls)

    # if background_video_urls is not None:
    #     video = get_output_media(SAMPLE_FILE_NAME, timed_captions, background_video_urls, VIDEO_SERVER)
    #     print(video)
    # else:
    #     print("No video")
