import os
from elevenlabs import ElevenLabs
import asyncio
import aiofiles
import io
from pydub import AudioSegment

# Voice IDs mapping for different languages
VOICE_MAPPING = {
    'en': 'JBFqnCBsd6RMkjVDRZzb',  # English voice
    'hi': 'cgSgspJ2msm6clMCkdW9',  # Hindi voice
}

async def generate_audio(text, output_filename, voice="en-AU-WilliamNeural"):
    """Generate audio using ElevenLabs API"""
    try:
        # Initialize ElevenLabs client
        client = ElevenLabs(api_key=os.environ.get('ELEVENLABS_API_KEY'))
        
        # Get language code from voice string
        lang_code = voice.split('-')[0].lower()
        
        # Get appropriate voice ID
        voice_id = VOICE_MAPPING.get(lang_code, VOICE_MAPPING['en'])
        
        # Convert text to speech with a supported format
        audio_stream = client.text_to_speech.convert(
            voice_id=voice_id,
            output_format="mp3_44100_128",  # Using supported format
            text=text,
            model_id="eleven_multilingual_v2",
        )
        
        # Save MP3 temporarily
        temp_mp3 = "temp_audio.mp3"
        audio_bytes = b''
        for chunk in audio_stream:
            if isinstance(chunk, (bytes, bytearray)):
                audio_bytes += chunk
            else:
                audio_bytes += bytes(chunk)
        
        with open(temp_mp3, 'wb') as f:
            f.write(audio_bytes)
        
        # Convert to WAV with correct parameters
        audio = AudioSegment.from_mp3(temp_mp3)
        audio = audio.set_frame_rate(16000).set_channels(1)
        audio.export(output_filename, format="wav")
        
        # Clean up temp file
        os.remove(temp_mp3)
        
        return True
        
    except Exception as e:
        print(f"Error generating audio: {str(e)}")
        import traceback
        print(f"Detailed error: {traceback.format_exc()}")
        return False





