# coding: utf-8

from __future__ import unicode_literals


import re


from .common import InfoExtractor


class OnlineAnidubIE(InfoExtractor):
    _VALID_URL = r'http://online\.anidub\.com/anime_tv/full/([,\w\d]+)-[-_\d\w]+\.html'
    _TITLE_PATTERN = r'<title>([\s\d\w/«»-]+) \['
    _SERIES_PATTERN = r'<option([\s\n\r]+selected="selected")?[\s\n\r]+value=["\'](http://online.anidub.com/[^"\']+)["\']>([^<]+)</option>'

    def _real_extract(self, url):
        anime_id = self._search_regex(self._VALID_URL, url, 'anime id', flags=re.UNICODE)

        anime_page = self._download_webpage(url, anime_id)
        anime_title = self._html_search_regex(self._TITLE_PATTERN, anime_page, 'anime title', flags=re.UNICODE)

        series_matches = re.findall(self._SERIES_PATTERN, anime_page)
        series_data = [(m[1], m[2]) for m in series_matches]

        entries = self.__entries(series_data, anime_title)
        return self.playlist_result(entries, anime_id, anime_title)

    def __entries(self, data, anime_title):
        for original_url, title in data:
            arg = re.findall(r"http://online\.anidub\.com/player/([^|]+)|\d+", original_url)[0]
            vk_url = "https://vk.com/" + arg

            yield self.url_result(vk_url, None, None, title)
