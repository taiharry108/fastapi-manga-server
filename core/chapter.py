class Chapter(object):
    def __init__(self, title: str, page_url: str):
        self._title = title
        self._page_url = page_url

    def get_title(self):
        return self._title

    def get_page_url(self):
        return self._page_url

    title = property(get_title)
    page_url = property(get_page_url)
