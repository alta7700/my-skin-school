from urllib import parse
from html.parser import HTMLParser


class IframeParser(HTMLParser):
    _iframe: dict[str, str]

    def __init__(self, *, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        self._iframe = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'iframe':
            for attr in attrs:
                self._iframe[attr[0]] = attr[1]

    def valid_iframe(self):
        return bool(self._iframe)

    def get_src(self):
        return parse.urlparse(self._iframe['src'])


class VKScriptParser(HTMLParser):
    _data = dict[str, str]
    _start_trigger = 'VK.Widgets.Podcast('
    _end_trigger = ')'

    def __init__(self, *, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        self._data = {}

    def handle_data(self, data: str) -> None:
        data = data.strip()
        if data:
            start_index = data.find(self._start_trigger)
            if start_index != -1:
                start_index += len(self._start_trigger)
                data = data[start_index:]
                end_index = data.find(self._end_trigger)
                if end_index != -1:
                    data = data[:end_index].replace('"', '').replace("'", '')
                    *_, track_id, track_hash = map(lambda x: x.strip(), data.split(','))
                    self._data.update({'track_id': track_id, 'track_hash': track_hash})

    def get_parsed_data(self) -> str | None:
        if (_id := self._data.get('track_id')) and (_hash := self._data.get('track_hash')):
            return f'{_id},{_hash}'
