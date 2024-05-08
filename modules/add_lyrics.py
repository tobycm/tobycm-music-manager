import subprocess

import eyed3
import yt_dlp


class AddLyricsPP(yt_dlp.postprocessor.PostProcessor):
    nsub_path: str

    def __init__(self, nsub_path: str = "bin/nsub", downloader=None):
        super().__init__(downloader)
        self.nsub_path = nsub_path

    def run(self, info):
        filepath = info.get("filepath")

        try:
            subtitles = info.get("requested_subtitles")
            subtitle_file = subtitles[next(iter(subtitles))].get("filepath")
            print(f"Found subtitle file: {subtitle_file}")
        except Exception as e:
            print("No subtitles found")
            return [], info

        lrc_subtitle_file = subtitle_file.split(".")
        lrc_subtitle_file[-1] = "lrc"
        lrc_subtitle_file = ".".join(lrc_subtitle_file)

        subprocess.run([
            self.nsub_path, "-f", "srt", "-t", "lrc",
            subtitle_file.replace("\\", "/"),
            lrc_subtitle_file.replace("\\", "/")
        ])

        mp3 = eyed3.load(filepath)
        if mp3 is None:
            raise yt_dlp.utils.PostProcessingError("Failed to load file")

        if mp3.tag is None:
            mp3.initTag()

        assert mp3.tag is not None

        with open(lrc_subtitle_file, "r") as f:
            mp3.tag.lyrics.set(f.read())

        mp3.tag.save()

        srt_subtitle_file = subtitle_file.split(".")
        srt_subtitle_file[-1] = "srt"
        srt_subtitle_file = ".".join(srt_subtitle_file)

        subprocess.run([
            self.nsub_path, "-f", "vtt", "-t", "srt",
            subtitle_file.replace("\\", "/"),
            srt_subtitle_file.replace("\\", "/")
        ])

        return [subtitle_file, lrc_subtitle_file], info
