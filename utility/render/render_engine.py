import time
import os
import tempfile
import zipfile
import platform
import subprocess
from moviepy.editor import (AudioFileClip, CompositeVideoClip, CompositeAudioClip, ImageClip,
                            TextClip, VideoFileClip)
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
import requests
from PIL import Image

def download_file(url, filename):
    with open(filename, 'wb') as f:
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        f.write(response.content)

def search_program(program_name):
    try: 
        search_cmd = "where" if platform.system() == "Windows" else "which"
        return subprocess.check_output([search_cmd, program_name]).decode().strip()
    except subprocess.CalledProcessError:
        return None

def get_program_path(program_name):
    program_path = search_program(program_name)
    return program_path

def get_output_media(audio_file, captions, image_segments, mode="images"):
    # Load the audio file
    audio = AudioFileClip(audio_file)
    
    # Create video clips from images
    clips = []
    for segment in image_segments:
        start_time = segment['start_time']
        end_time = segment['end_time']
        duration = end_time - start_time
        
        try:
            # Create image clip
            img_clip = ImageClip(segment['image_path'])
            # Set duration and start time
            img_clip = img_clip.set_duration(duration)
            img_clip = img_clip.set_start(start_time)
            
            # Use PIL to resize the image first
            pil_image = Image.open(segment['image_path'])
            pil_image = pil_image.resize((1920, 1080), Image.Resampling.LANCZOS)
            pil_image.save(segment['image_path'])
            
            # Create new clip from resized image
            img_clip = ImageClip(segment['image_path'])
            img_clip = img_clip.set_duration(duration)
            img_clip = img_clip.set_start(start_time)
            
            clips.append(img_clip)
        except Exception as e:
            print(f"Error processing image segment: {e}")
            continue
    
    if not clips:
        raise Exception("No valid image clips were created")
    
    # Create caption clips
    caption_clips = []
    for caption in captions:
        text_clip = TextClip(caption['text'], fontsize=40, color='white', font='Arial')
        text_clip = text_clip.set_position('bottom').set_duration(caption['end'] - caption['start'])
        text_clip = text_clip.set_start(caption['start'])
        caption_clips.append(text_clip)
    
    # Combine all clips
    final_clip = CompositeVideoClip(clips + caption_clips)
    
    # Add audio
    final_clip = final_clip.set_audio(audio)
    
    # Write output file
    output_path = "output.mp4"
    final_clip.write_videofile(output_path, fps=24)
    
    # Clean up
    final_clip.close()
    audio.close()
    
    return output_path
