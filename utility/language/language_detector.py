from langdetect import detect
import edge_tts

# Map of languages to their best child-friendly female TTS voices
VOICE_MAPPING = {
    'en': 'en-US-JennyMultilingualNeural',  # Cheerful, child-friendly English voice
    'hi': 'hi-IN-MadhurNeural',             # Hindi voice
    'es': 'es-MX-DaliaNeural',              # Spanish voice
    'fr': 'fr-FR-DeniseNeural',             # French voice
    'de': 'de-DE-KatjaNeural',              # German voice
    'it': 'it-IT-ElsaNeural',               # Italian voice
    'ja': 'ja-JP-NanamiNeural',             # Japanese voice
    'ko': 'ko-KR-SunHiNeural',              # Korean voice
    'zh': 'zh-CN-XiaoxiaoNeural',           # Chinese voice
    'ar': 'ar-AE-FatimaNeural',             # Arabic voice
}

async def detect_language_and_voice(text):
    """Detect language and return appropriate voice"""
    try:
        lang = detect(text)
        # Get all available voices
        available_voices = await edge_tts.list_voices()
        available_voice_names = [voice['ShortName'] for voice in available_voices]
        
        if lang in VOICE_MAPPING:
            # Check if preferred voice is available
            if VOICE_MAPPING[lang] in available_voice_names:
                return lang, VOICE_MAPPING[lang]
            
            # If not, find another voice for the same language
            lang_code = lang if lang != 'hi' else 'hi-IN'
            alternative_voices = [
                voice['ShortName'] for voice in available_voices 
                if voice['Locale'].startswith(lang_code) and voice['Gender'] == 'Female'
            ]
            
            if alternative_voices:
                return lang, alternative_voices[0]
        
        # Default to English if no suitable voice found
        return 'en', VOICE_MAPPING['en']
    except Exception as e:
        print(f"Error in language detection: {e}")
        return 'en', VOICE_MAPPING['en']

async def list_available_voices():
    """List all available voices for reference"""
    voices = await edge_tts.list_voices()
    return [voice for voice in voices if voice['Gender'] == 'Female']