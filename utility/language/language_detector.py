from langdetect import detect
import edge_tts

# Map of languages to their best child-friendly female TTS voices
VOICE_MAPPING = {
    'en': 'en-US-JennyMultilingualNeural',  # Cheerful, child-friendly English voice
    'hi': 'hi-IN-SweetyNeural',             # Hindi voice
    'es': 'es-MX-DaliaNeural',              # Spanish voice
    'fr': 'fr-FR-DeniseNeural',             # French voice
    'de': 'de-DE-KatjaNeural',              # German voice
    'it': 'it-IT-ElsaNeural',               # Italian voice
    'ja': 'ja-JP-NanamiNeural',             # Japanese voice
    'ko': 'ko-KR-SunHiNeural',              # Korean voice
    'zh': 'zh-CN-XiaoxiaoNeural',           # Chinese voice
    'ar': 'ar-AE-FatimaNeural',             # Arabic voice
}

def detect_language_and_voice(text):
    """Detect language and return appropriate voice"""
    try:
        lang = detect(text)
        if lang in VOICE_MAPPING:
            return lang, VOICE_MAPPING[lang]
        return 'en', VOICE_MAPPING['en']  # Default to English
    except:
        return 'en', VOICE_MAPPING['en']  # Default to English if detection fails

async def list_available_voices():
    """List all available voices for reference"""
    voices = await edge_tts.list_voices()
    return [voice for voice in voices if voice['ShortName'] in VOICE_MAPPING.values()]