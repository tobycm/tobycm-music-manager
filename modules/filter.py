import os
from os import listdir
from os.path import isfile, join


def filter_videos(
    videos_ids: list[str],
    music_dir: str = "~/Music/toby-my-music/",
) -> list[str]:
    onlyfiles = [
        file for file in listdir(music_dir) if isfile(join(music_dir, file))
    ]

    for file in onlyfiles:
        for id in videos_ids:
            if id in file:
                break
        else:
            print("Deleting " + file)
            os.remove(join(music_dir, file))

    onlyfiles = [
        file for file in listdir(music_dir) if isfile(join(music_dir, file))
    ]

    need_to_download: list[str] = []
    for id in videos_ids:
        for file in onlyfiles:
            if id in file:
                break
        else:
            need_to_download.append(id)

    return need_to_download
