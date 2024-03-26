import argparse
import os
import subprocess

import dotenv

from modules.fetch import get_playlist_items
from modules.filter import filter_videos

dotenv.load_dotenv()

KEY = os.getenv("YT_API_KEY")
if not KEY:
    raise ValueError("YT_API_KEY not found in .env or environment variables")

url = "https://youtube.googleapis.com/youtube/v3/playlistItems?playlistId=&part=contentDetails&maxResults=50&key="

music_dir = os.getenv("OUTPUT_DIR", "~/Music/")
yt_dlp_exe = os.getenv("YT_DLP_EXE", "yt-dlp")

playlist_id = os.getenv("PLAYLIST_ID", "PLSQmKW3jS_HRPnGo1cv9W6IH7Z_-3oAn_")

bypass_already_downloaded = os.getenv("BYPASS_ALREADY_DOWNLOADED",
                                      "false").lower() == "true"

parser = argparse.ArgumentParser()

parser.add_argument("--playlist_id", help="Playlist ID", default=playlist_id)
parser.add_argument("output_dir", help="Output directory", default="~/Music/")
parser.add_argument("--yt_dlp_exe", help="yt-dlp executable", default="yt-dlp")
parser.add_argument("--no-check-downloaded",
                    help="Bypass already downloaded videos",
                    action="store_true")

args = parser.parse_args()

playlist_id = args.playlist_id
music_dir = args.output_dir
yt_dlp_exe = args.yt_dlp_exe
bypass_already_downloaded = args.no_check_downloaded

video_ids = get_playlist_items(playlist_id, KEY)
if not video_ids:
    raise ValueError("No video ids found")

with open("ids.txt", "a") as f:  # create file if it doesn't exist
    pass

with open("ids.txt", "r") as f:
    ids = f.read().splitlines()

if bypass_already_downloaded or len(ids) != len(video_ids):
    # new or removed videos
    need_to_download = filter_videos(video_ids, music_dir)
    if bypass_already_downloaded:
        need_to_download = video_ids

    if len(need_to_download) == 0:
        print("No new videos found")

    # Download
    for index, id in enumerate(need_to_download):
        print(f"Downloading {index + 1}/{len(need_to_download)}")

        subprocess.run([
            yt_dlp_exe,
            "-x",
            "--audio-format",
            "mp3",
            "--format",
            "ba",
            f"https://www.youtube.com/watch?v={id}",
            "--embed-metadata",
            "--embed-thumbnail",
            "--ppa",
            "EmbedThumbnail+ffmpeg_o:-c:v png -vf pad='iw:max(iw\\,ih):(ow-iw)/2:(oh-ih)/2:color=0x000000',scale='max(iw\\,ih):max(iw\\,ih)'",
            "-o",
            f"{music_dir}%(title)s [%(id)s].%(ext)s",
        ])

    with open("ids.txt", "w") as f:  # save new ids
        f.write("\n".join(video_ids))

    # subprocess.run(["sudo", "reboot"])
