import subprocess, json, pandas as pd

def get_playlist_entries(playlist_url: str):
    cmd = ["yt-dlp", "--flat-playlist", "--dump-single-json", playlist_url]
    out = subprocess.check_output(cmd, text=True)
    data = json.loads(out)
    return [{"id": e["id"],
             "title": e.get("title",""),
             "url": f"https://www.youtube.com/watch?v={e['id']}"} 
            for e in data.get("entries", [])]

def get_playlist_entries_from_csv(path: str):
    df = pd.read_csv(path)
    return [{"id": row["id"], 
             "title": row.get("title",""), 
             "url": row.get("url", f"https://www.youtube.com/watch?v={row['id']}")}
            for _, row in df.iterrows()]