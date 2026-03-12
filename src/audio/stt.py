from faster_whisper import WhisperModel
import tempfile
import soundfile as sf

# Load model once
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


def transcribe(audio_bytes):

    """
    Convert microphone audio into text
    """

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:

        f.write(audio_bytes)
        temp_path = f.name

    segments, _ = model.transcribe(
        temp_path,
        language="de"
    )

    text = " ".join([segment.text for segment in segments])

    return text.strip()