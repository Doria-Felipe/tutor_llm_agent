def is_subtitles_disabled(e: Exception) -> bool:
    return "subtitles are disabled" in str(e).lower()

def is_no_transcript(e: Exception) -> bool:
    return "no transcripts were found" in str(e).lower()

def is_ip_block_error(e: Exception) -> bool:
    msg = str(e).lower()
    return any(x in msg for x in [
        "blocking requests from your ip",
        "requestblocked",
        "ipblocked",
        "too many requests",
        "toomanyrequests"
    ])