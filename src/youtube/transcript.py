import random, time
from youtube_transcript_api import YouTubeTranscriptApi
from .exceptions import is_ip_block_error

api = YouTubeTranscriptApi()

def fetch_with_backoff(video_id: str, languages=("de",), max_retries=6):
    delay = 20.0
    for attempt in range(max_retries):
        try:
            return api.fetch(video_id, languages=list(languages))
        except Exception as e:
            if not is_ip_block_error(e):
                raise
            sleep_s = delay + random.uniform(0, 1.5)
            print(f"[BLOCKED] {video_id} — sleeping {sleep_s:.1f}s (attempt {attempt+1}/{max_retries})")
            time.sleep(sleep_s)
            delay *= 2
    raise RuntimeError(f"Still blocked after {max_retries} retries for {video_id}")