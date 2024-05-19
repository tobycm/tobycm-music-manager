import argparse
import os
from os import listdir
from os.path import isfile, join

import dotenv
import eyed3
import yt_dlp

from modules.add_lyrics import AddLyricsPP

dotenv.load_dotenv()

output_dir = os.getenv("OUTPUT_DIR", "~/Music/")

parser = argparse.ArgumentParser()
parser.add_argument("output_dir",
                    help="Output directory",
                    nargs="?",
                    default=output_dir)

args = parser.parse_args()

output_dir = args.output_dir

ytdlp_opts = {
    'ignoreerrors':
    True,
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
    'postprocessor_args': {
        'embedthumbnail+ffmpeg_o': [
            '-c:v', 'png', '-vf',
            'pad=iw:max(iw\\,ih):(ow-iw)/2:(oh-ih)/2:color=0x000000,scale=max(iw\\,ih):max(iw\\,ih)'
        ]
    },
    'subtitleslangs': ['en', 'vi', 'jp'],
    'subtitlesformat':
    'vtt',
    'writesubtitles':
    True
}


def filter_mp3(music_dir: str = "~/Music/toby-my-music/", ) -> list[str]:
    onlyfiles = [
        file for file in listdir(music_dir) if isfile(join(music_dir, file))
    ]

    need_to_download: list[str] = []

    for file in onlyfiles:
        if not file.endswith(".mp3"):
            continue

        mp3 = eyed3.load(join(music_dir, file))
        if mp3 is None:
            continue

        if mp3.tag is None:
            continue

        if mp3.tag.lyrics is None:
            continue

        if len(mp3.tag.lyrics) == 0:
            continue

        need_to_download.append(file.split(" [")[-1].split("]")[0])

    return need_to_download


video_ids = filter_mp3(output_dir)

with yt_dlp.YoutubeDL(ytdlp_opts) as ydl:
    ydl.add_post_processor(AddLyricsPP())
    ydl.download(video_ids)
