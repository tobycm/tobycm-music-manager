import eyed3
import webvtt
import yt_dlp


class NoSubtitles(Exception):
    pass


class AddLyricsPP(yt_dlp.postprocessor.PostProcessor):

    def __init__(self, downloader=None):
        super().__init__(downloader)

    def run(self, info: dict):
        self.to_screen("Trying to find subtitles from the video")

        subs: list[tuple[str, str]] = []  # list[(lang, filepath)]

        try:
            # ew wtf is this formatting
            subtitles: dict[str,
                            dict[str,
                                 str]] | None = info.get("requested_subtitles")
            if subtitles is None:
                raise NoSubtitles

            en_sub = subtitles.get("en")
            vi_sub = subtitles.get("vi")

            if not en_sub and not vi_sub:
                raise NoSubtitles

            if en_sub:
                subs.append(("eng", en_sub.get("filepath")))
            if vi_sub:
                subs.append(("vie", vi_sub.get("filepath")))

            self.to_screen(f"Found subtitle files: {[sub[1] for sub in subs]}")
        except (NoSubtitles, StopIteration):
            self.to_screen("No subtitles found")
            return [], info
        except Exception as e:
            self.to_screen(f"Error while getting subtitles. Error {e}")
            return [], info

        # Load the mp3 file
        mp3 = eyed3.load(info.get("filepath"))
        if mp3 is None:
            raise yt_dlp.utils.PostProcessingError("Failed to load file")

        if mp3.tag is None:
            mp3.initTag()

        assert mp3.tag is not None

        def add_lyrics(lang: str, sub_file: str, no_header: bool = False):
            # transform vtt to lrc
            lrc = ""
            if not no_header:
                lrc = "[offset: +00:00.00]\n\n"

            vtt = webvtt.read(sub_file)
            captions = vtt.captions

            for treatment in SpecialTreatments.get_treatment(info.get("id")):
                captions = treatment(captions)

            for caption in captions:
                caption.text = caption.text.replace("\n", "")
                start = ":".join(caption.start.split(":")[1:]).split(".")
                lrc += f"[{f'{start[0]}.{start[1][:2]}'}]{caption.text}\n"

            mp3.tag.lyrics.set(lrc, lang=lang.encode("ascii"))

        no_header = False
        for lang, sub_file in subs:
            add_lyrics(lang, sub_file, no_header=no_header)
            no_header = True

        mp3.tag.save()

        self.to_screen("Subtitles added!")

        return [sub[1] for sub in subs], info


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
