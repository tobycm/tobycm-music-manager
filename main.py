import argparse
import os
import sys
import time
from pprint import pprint

import dotenv
import yt_dlp

from modules.add_lyrics import AddLyricsPP
from modules.fetch import get_playlist_items
from modules.filter import filter_videos

dotenv.load_dotenv()

output_dir = os.getenv("OUTPUT_DIR", "~/Music/")

KEY = os.getenv("YT_API_KEY")
if not KEY:
    raise ValueError("YT_API_KEY not found in .env or environment variables")

url = "https://youtube.googleapis.com/youtube/v3/playlistItems?playlistId=&part=contentDetails&maxResults=50&key="

playlist_id = os.getenv("PLAYLIST_ID", "PLSQmKW3jS_HRPnGo1cv9W6IH7Z_-3oAn_")

bypass_already_downloaded = os.getenv("BYPASS_ALREADY_DOWNLOADED",
                                      "false").lower() == "true"

no_subtitle = os.getenv("NO_SUBTITLE", "false").lower() == "true"

parser = argparse.ArgumentParser()

parser.add_argument("--playlist-id", help="Playlist ID", default=playlist_id)
parser.add_argument("output_dir",
                    help="Output directory",
                    nargs="?",
                    default=output_dir)
parser.add_argument("--no-check-downloaded",
                    help="Bypass already downloaded videos",
                    action="store_true")
parser.add_argument("--no-subtitle",
                    help="Don't download subtitles",
                    action="store_true")

args, unknown_args = parser.parse_known_args()

playlist_id = args.playlist_id

output_dir = args.output_dir

if not os.path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)
if not os.path.isdir(output_dir):
    raise ValueError(f"{output_dir} is not a directory")

bypass_already_downloaded = args.no_check_downloaded
no_subtitle = args.no_subtitle

extra_args = yt_dlp.parse_options(unknown_args)

ytdlp_opts = extra_args.ydl_opts

# pprint(ytdlp_opts)

toby_opts = {
    'ignoreerrors':
    True,
    "concurrent_fragments":
    2,
    'format':
    'ba',
    'outtmpl': {
        'default': f'{output_dir}/%(title)s [%(id)s].%(ext)s',
        'pl_thumbnail': ''
    },
    'writethumbnail':
    True,
    'final_ext':
    'mp3',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '5',
        'nopostoverwrites': False
    }, {
        'key': 'FFmpegMetadata',
        'add_chapters': True,
        'add_metadata': True,
        'add_infojson': 'if_exists'
    }, {
        'key': 'EmbedThumbnail',
        'already_have_thumbnail': False
    }],
    # 'postprocessor_args': {
    #     'embedthumbnail+ffmpeg_o': [
    #         '-c:v', 'png', '-vf',
    #         'pad=iw:max(iw\\,ih):(ow-iw)/2:(oh-ih)/2:color=0x000000,scale=max(iw\\,ih):max(iw\\,ih)'
    #     ]
    # }
}

if not no_subtitle:
    ytdlp_opts.update({
        'subtitleslangs': ['en', 'vi', 'jp'],
        'subtitlesformat': 'vtt',
        'writesubtitles': True
    })

for k, v in toby_opts.items():
    ytdlp_opts[k] = v

# pprint(ytdlp_opts)

playlist_video_ids = get_playlist_items(playlist_id, KEY)
if not playlist_video_ids:
    raise ValueError("No video ids found in playlist")

if not os.path.exists(".cache"):
    os.mkdir(".cache")

with open(".cache/playlist_video_ids.txt",
          "a") as f:  # create file if it doesn't exist
    pass

cached_video_ids = []

with open(".cache/playlist_video_ids.txt", "r") as f:
    try:
        timestamp = int(f.readline().strip("Timestamp: "))
    except ValueError:
        timestamp = 0
    if time.time() - timestamp > 86400:  # 1 day
        print("1 day passed since last fetch, cache invalidated")
    else:
        cached_video_ids = f.read().splitlines()

pprint(ytdlp_opts)

if (len(cached_video_ids)
        == len(playlist_video_ids)) and not bypass_already_downloaded:
    print("No new videos to download")
    exit(0)

need_to_download = playlist_video_ids
# new or removed videos
if not bypass_already_downloaded:
    need_to_download = filter_videos(playlist_video_ids, output_dir)

print(f"Found {len(need_to_download)} new videos to download")

if len(need_to_download) == 0:
    print("No new videos to download")
    exit(0)

# Download
print(f"Downloading {len(need_to_download)} songs...")

need_to_download = need_to_download[::-1]

with yt_dlp.YoutubeDL(ytdlp_opts) as ydl:
    if not no_subtitle:
        ydl.add_post_processor(AddLyricsPP())
    ydl.download(need_to_download)

with open(".cache/playlist_video_ids.txt", "w") as f:  # save new ids
    f.write(f"Timestamp: {int(time.time())}\n")
    f.write("\n".join(playlist_video_ids))

# subprocess.run(["sudo", "reboot"])
