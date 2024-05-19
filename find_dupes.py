import argparse
import os
from os import listdir
from os.path import isfile, join

import dotenv

from modules.fetch import get_playlist_items

dotenv.load_dotenv()

output_dir = os.getenv("OUTPUT_DIR", "~/Music/")

KEY = os.getenv("YT_API_KEY")
if not KEY:
    raise ValueError("YT_API_KEY not found in .env or environment variables")

url = "https://youtube.googleapis.com/youtube/v3/playlistItems?playlistId=&part=contentDetails&maxResults=50&key="

playlist_id = os.getenv("PLAYLIST_ID", "PLSQmKW3jS_HRPnGo1cv9W6IH7Z_-3oAn_")

delete_dupes = os.getenv("DELETE_DUPES", "false").lower() == "true"

parser = argparse.ArgumentParser()

parser.add_argument("--playlist-id", help="Playlist ID", default=playlist_id)
parser.add_argument("output_dir",
                    help="Output directory",
                    nargs="?",
                    default=output_dir)
parser.add_argument("--delete",
                    help="Delete duplicate files",
                    action="store_true")

args = parser.parse_args()

playlist_id = args.playlist_id
output_dir = args.output_dir
delete_dupes = args.delete

playlist_video_ids = get_playlist_items(playlist_id, KEY)
if not playlist_video_ids:
    raise ValueError("No video ids found in playlist")

onlyfiles: list[str] = [
    file for file in listdir(output_dir) if isfile(join(output_dir, file))
]

dupes: list[str] = []

for id in playlist_video_ids:
    last_file: str | None = None

    for file in onlyfiles:
        if id not in file:
            continue

        if last_file:
            dupes.append(last_file)
            dupes.append(file)
            break

        last_file = file

if not dupes:
    print("No duplicates found")
    exit()

if delete_dupes:
    print("Deleting duplicates")

    for dupe in dupes:
        os.remove(join(output_dir, dupe))
        print("Deleted " + dupe)

    exit()

print("Duplicate(s): ")
for dupe in dupes:
    print(dupe)
