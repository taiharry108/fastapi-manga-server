
from typing import Dict
from .downloader import Downloader


class DownloaderFactory(object):
    downloaders: Dict[str, Downloader] = {}

    @classmethod
    def get_downloader(cls, name: str) -> Downloader:
        if not name in cls.downloaders:
            cls.downloaders[name] = Downloader()

        return cls.downloaders[name]
