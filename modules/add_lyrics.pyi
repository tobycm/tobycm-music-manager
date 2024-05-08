import yt_dlp


class AddLyricsPP(yt_dlp.postprocessor.PostProcessor):
    nsub_path: str

    def __init__(self, nsub_path: str = "bin/nsub", downloader=None):
        ...

    def run(self, info):
        ...
