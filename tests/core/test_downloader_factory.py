from core.downloader import Downloader
from core.downloader_factory import DownloaderFactory


class TestDownloaderFactory:
    def test_get_downloader(self):
        downloader = DownloaderFactory.get_downloader('test')
        assert isinstance(downloader, Downloader)

    def test_get_downloaders_with_same_name(self):
        downloader1 = DownloaderFactory.get_downloader('test')
        downloader2 = DownloaderFactory.get_downloader('test')
        assert downloader1 == downloader2
