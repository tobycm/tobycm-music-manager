import eyed3
import webvtt
import yt_dlp


class NoSubtitles(Exception):
    pass


class AddLyricsPP(yt_dlp.postprocessor.PostProcessor):
    nsub_path: str

    def __init__(self, nsub_path: str = "bin/nsub", downloader=None):
        super().__init__(downloader)
        self.nsub_path = nsub_path

    def run(self, info: dict):
        self.to_screen("Trying to find subtitles from the video")

        filepath: str = info.get("filepath")

        try:
            # ew wtf is this formatting
            subtitles: dict[str,
                            dict[str,
                                 str]] | None = info.get("requested_subtitles")
            if subtitles is None:
                raise NoSubtitles

            subtitle_file: str | None = next(iter(
                subtitles.values())).get("filepath")

            if subtitle_file is None:
                raise NoSubtitles

            self.to_screen(f"Found subtitle file: {subtitle_file}")
        except (NoSubtitles, StopIteration):
            self.to_screen("No subtitles found")
            return [], info
        except Exception as e:
            self.to_screen(f"Error while getting subtitles. Error {e}")
            return [], info

        lrc = "[offset: +0]\n"

        vtt = webvtt.read(subtitle_file)
        captions = vtt.captions

        for treatment in SpecialTreatments.get_treatment(info.get("id")):
            captions = treatment(captions)

        for caption in webvtt.read(subtitle_file):
            caption.text = caption.text.replace("\n", "")
            lrc += f"[{caption.start}]{caption.text}\n"

        mp3 = eyed3.load(filepath)
        if mp3 is None:
            raise yt_dlp.utils.PostProcessingError("Failed to load file")

        if mp3.tag is None:
            mp3.initTag()

        assert mp3.tag is not None

        mp3.tag.lyrics.set(lrc)

        mp3.tag.save()

        self.to_screen("Subtitles added!")

        return [subtitle_file], info


class SpecialTreatments:
    deduplicate_ids = ["6bnaBnd4kyU"]

    @staticmethod
    def deduplicate(captions: list) -> list:
        texts = []
        new_captions = []
        for caption in captions:
            if caption.text in texts:
                continue

            new_captions.append(caption)
            texts.append(caption.text)

        return new_captions

    @staticmethod
    def get_treatment(video_id: str) -> list:
        if video_id in SpecialTreatments.deduplicate_ids:
            return [SpecialTreatments.deduplicate]

        return []
