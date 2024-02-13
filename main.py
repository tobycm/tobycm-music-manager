import os
import subprocess

import dotenv

from modules.fetch import get_playlist_items
from modules.filter import filter_videos

dotenv.load_dotenv()

KEY = os.getenv("YT_API_KEY")
if not KEY:
    raise ValueError("YT_API_KEY not found in .env")

url = "https://youtube.googleapis.com/youtube/v3/playlistItems?playlistId=&part=contentDetails&maxResults=50&key="

music_dir = "D:/RandomStuff/ytdl-stuff/toby-my-music/"
yt_dlp_exe = "yt-dlp"

video_ids = get_playlist_items("PLSQmKW3jS_HRPnGo1cv9W6IH7Z_-3oAn_", KEY)
if not video_ids:
    raise ValueError("No video ids found")

with open("ids.txt", "a") as f:  # create file if it doesn't exist
    pass

with open("ids.txt", "r") as f:
    ids = f.read().splitlines()

if len(ids) != len(video_ids):
    # new or removed videos
    need_to_download = filter_videos(video_ids, music_dir)

    # Download
    for id in need_to_download:
        subprocess.run([
            yt_dlp_exe,
            "-x",
            "--audio-format",
            "mp3",
            "--format",
            "ba",
            f"https://www.youtube.com/watch?v={id}",
            "-o",
            f"{music_dir}%(title)s [%(id)s].%(ext)s",
        ])

    with open("ids.txt", "w") as f:  # save new ids
        f.write("\n".join(video_ids))

    # subprocess.run(["sudo", "reboot"])
