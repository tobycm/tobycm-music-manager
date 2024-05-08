import os
from os import listdir
from os.path import isfile, join


def filter_videos(videos_ids: list[str],
                  music_dir: str = "/home/pi/toby-my-music/") -> list[str]:
    onlyfiles = [
        file for file in listdir(music_dir) if isfile(join(music_dir, file))
    ]

    for file in onlyfiles:
        downloaded = False
        for id in videos_ids:
            if id not in file:
                continue
            if "mp3" in file:
                downloaded = True
                break
            mp3_file = file.split(".")
            if mp3_file[-1] != "srt":
                break
            mp3_file.pop()
            mp3_file[-1] = "mp3"
            mp3_file = ".".join(mp3_file)

            if mp3_file in onlyfiles:
                downloaded = True
                break
        if not downloaded:
            print("Deleting " + file)
            os.remove(join(music_dir, file))

    onlyfiles = [
        file for file in listdir(music_dir) if isfile(join(music_dir, file))
    ]

    need_to_download: list[str] = []
    for id in videos_ids:
        downloaded = False
        for file in onlyfiles:
            if id not in file:
                continue
            if "mp3" in file:
                downloaded = True
                break
            mp3_file = file.split(".")
            if mp3_file[-1] != "srt":
                break
            mp3_file.pop()
            mp3_file[-1] = "mp3"
            mp3_file = ".".join(mp3_file)

            if mp3_file in onlyfiles:
                downloaded = True
                break
        if not downloaded:
            need_to_download.append(id)

    return need_to_download
