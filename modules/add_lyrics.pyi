import yt_dlp


class AddLyricsPP(yt_dlp.postprocessor.PostProcessor):

    def __init__(self, downloader=None):
        ...

    def run(self, info):
        ...
