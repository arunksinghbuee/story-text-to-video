import os
from elevenlabs import ElevenLabs
import asyncio
import aiofiles
import io

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
        
        # Get language code from voice string (e.g., 'en-AU-WilliamNeural' -> 'en')
        lang_code = voice.split('-')[0].lower()
        
        # Get appropriate voice ID
        voice_id = VOICE_MAPPING.get(lang_code, VOICE_MAPPING['en'])
        
        # Convert text to speech
        audio_stream = client.text_to_speech.convert(
            voice_id=voice_id,
            output_format="wav",  # Changed to WAV format
            text=text,
            model_id="eleven_multilingual_v2",
        )
        
        # Convert generator to bytes
        audio_bytes = b''
        for chunk in audio_stream:
            if isinstance(chunk, (bytes, bytearray)):
                audio_bytes += chunk
            else:
                audio_bytes += bytes(chunk)
        
        # Save audio to file
        async with aiofiles.open(output_filename, 'wb') as f:
            await f.write(audio_bytes)
        
        return True
        
    except Exception as e:
        print(f"Error generating audio: {str(e)}")
        # Print more detailed error information
        import traceback
        print(f"Detailed error: {traceback.format_exc()}")
        return False





