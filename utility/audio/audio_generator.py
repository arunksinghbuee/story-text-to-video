import os
from elevenlabs import ElevenLabs
import asyncio

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
        audio = client.text_to_speech.convert(
            voice_id=voice_id,
            output_format="mp3_44100_128",
            text=text,
            model_id="eleven_multilingual_v2",
        )
        
        # Save audio to file
        with open(output_filename, 'wb') as f:
            f.write(audio)
        
        return True
        
    except Exception as e:
        print(f"Error generating audio: {str(e)}")
        return False





