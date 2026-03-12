from gtts import gTTS # type: ignore
from pathlib import Path
import hashlib

# Cache folder
CACHE_DIR = Path("data/audio_cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def speak(text: str, lang: str = "de") -> str:
    """
    Generate (or reuse cached) speech audio for a text string.

    Args:
        text (str): text to convert
        lang (str): language code

    Returns:
        str: path to audio file
    """

    # Create deterministic filename from text
    text_hash = hashlib.md5(text.encode("utf-8")).hexdigest()
    file_path = CACHE_DIR / f"{text_hash}.mp3"

    # If audio already exists, reuse it
    if file_path.exists():
        return str(file_path)

    # Generate audio
    tts = gTTS(text=text, lang=lang)
    tts.save(file_path)

    return str(file_path)