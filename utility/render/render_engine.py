from moviepy.editor import AudioFileClip, CompositeVideoClip, ImageClip, TextClip
from PIL import Image

def get_output_media(audio_file, captions, image_segments):
    """Generate video with images, captions and audio"""
    try:
        # Load the audio file
        audio = AudioFileClip(audio_file)
        
        # Create video clips from images
        clips = []
        for segment in image_segments:
            try:
                # Use PIL to resize the image first
                with Image.open(segment['image_path']) as pil_image:
                    pil_image = pil_image.resize((1920, 1080), Image.Resampling.LANCZOS)
                    pil_image.save(segment['image_path'])
                
                # Create image clip
                img_clip = ImageClip(segment['image_path'])
                duration = segment['end_time'] - segment['start_time']
                img_clip = img_clip.set_duration(duration).set_start(segment['start_time'])
                clips.append(img_clip)
            except Exception as e:
                print(f"Error processing image segment: {e}")
                continue
        
        if not clips:
            raise Exception("No valid image clips were created")
        
        # Create caption clips
        caption_clips = []
        for caption in captions:
            try:
                time_range, text = caption
                start_time, end_time = time_range
                
                text_clip = (TextClip(str(text), fontsize=40, color='white', font='Arial')
                            .set_position('bottom')
                            .set_duration(end_time - start_time)
                            .set_start(start_time))
                caption_clips.append(text_clip)
            except Exception as e:
                print(f"Error creating caption clip: {e}")
                continue
        
        # Combine all clips and add audio
        final_clip = CompositeVideoClip(clips + caption_clips)
        final_clip = final_clip.set_audio(audio)
        
        # Write output file
        output_path = "output.mp4"
        final_clip.write_videofile(output_path, fps=24)
        
        return output_path
    
    finally:
        # Clean up
        try:
            final_clip.close()
            audio.close()
        except:
            pass
