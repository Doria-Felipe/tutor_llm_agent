def merge_transcript_chunks(chunks, max_chars=900, min_chars=300):
    merged = []
    buf_text, buf_start, buf_end = [], None, None

    for chunk in chunks:
        t = chunk["text"].strip()
        if not t:
            continue
        if buf_start is None:
            buf_start = chunk["start"]

        candidate = (" ".join(buf_text + [t])).strip()

        if len(candidate) < max_chars:
            buf_text.append(t)
            buf_end = chunk["end"]
        else:
            if buf_text:
                merged.append({"text": " ".join(buf_text).strip(),
                               "start": buf_start, "end": buf_end})
            buf_text = [t]
            buf_start = chunk["start"]
            buf_end = chunk["end"]

    if buf_text:
        merged.append({"text": " ".join(buf_text).strip(),
                       "start": buf_start, "end": buf_end})

    return [m for m in merged if len(m["text"]) >= min_chars]