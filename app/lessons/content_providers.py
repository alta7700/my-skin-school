from typing import Any, TYPE_CHECKING, TypeVar, Type
from urllib import parse

from django.forms.renderers import get_default_renderer
from django.utils.functional import classproperty
from django.utils.safestring import mark_safe

from lessons.html_parser import IframeParser, VKScriptParser


if TYPE_CHECKING:
    from lessons.models import Content

CP = TypeVar('CP')

VIDEO = 1
AUDIO = 2
TEXT = 3


class BaseContentProvider:
    renderer = get_default_renderer()

    template_prefix: str = 'lessons/content/'
    _template_name: str = None
    content_type: int = None
    content_type_ru: str = None
    content_type_en: str = None
    provider_id: int = None
    provider_name: str = None
    provider_priority: int = None

    instance: "Content"

    def __init__(self, content_instance: "Content"):
        self.instance = content_instance

    def __repr__(self) -> str:
        return f'{self.content_type_ru} {self.provider_name}'

    @classproperty
    def group_block_id(cls) -> str:
        return f'lesson-{cls.content_type_en}-block'

    @classproperty
    def priority(cls) -> int:
        return cls.provider_priority or cls.provider_id

    @classproperty
    def provider_icon(cls) -> str:
        return f'/static/images/{cls.provider_name}.svg'

    @classproperty
    def template_name(self) -> str:
        return f'{self.template_prefix}{self._template_name or self.content_type_en}.html'

    def get_context(self) -> dict[str, Any]:
        return {}

    def render(self) -> str:
        context = self.get_context()
        return mark_safe(self.renderer.render(self.template_name, context))

    def render_link(self) -> str:
        return mark_safe(
            f'<a href="{self.get_remote_url()}" target="_blank"><img src="{self.provider_icon}" alt="{self.provider_name}"></a>'
        )

    def get_remote_url(self) -> str:
        return self.instance.text

    @classmethod
    def get_all_providers(cls: Type[CP]) -> list[Type[CP]]:
        subclasses = []
        if cls.provider_id:
            subclasses.append(cls)
        for sc in cls.__subclasses__():
            subclasses.extend(sc.get_all_providers())
        return sorted(subclasses, key=lambda x: (x.content_type, x.priority))

    @classmethod
    def get_choice_id(cls) -> str:
        return f'{cls.content_type},{cls.provider_id}'

    @classmethod
    def get_title(cls) -> str:
        return f'{cls.content_type_ru.capitalize()} {cls.provider_name}'.strip()

    @classmethod
    def get_choices(cls) -> tuple[tuple[str, str]]:
        choices = []
        for pr in cls.get_all_providers():
            choices.append((pr.get_choice_id(), pr.get_title()))
        return tuple(choices)

    @classmethod
    def get_providers_map(cls) -> tuple[dict[str, Type[CP]], dict[int, tuple[str, str]]]:
        pr_map, ct_map = {}, {}
        for pr in cls.get_all_providers():
            pr_map[pr.get_choice_id()] = pr
            ct_map[pr.content_type] = pr.content_type_ru.upper(), pr.group_block_id
        return pr_map, ct_map

    def modify_data(self):
        """modifying self.instance.text"""
        pass


class BaseVideoContentProvider(BaseContentProvider):
    content_type = VIDEO
    content_type_ru = 'видео'
    content_type_en = 'video'
    video_src_pattern = None
    remote_url_pattern = None

    def get_context(self) -> dict[str, Any]:
        return {'video_src': self.video_src_pattern.format(self.instance.text)}

    def get_remote_url(self) -> str:
        return self.remote_url_pattern.format(self.instance.text)

    def modify_data(self):
        parser = IframeParser()
        parser.feed(self.instance.text)
        if parser.valid_iframe():
            self.finish_modify_data(parser)

    def finish_modify_data(self, parser: IframeParser):
        raise NotImplementedError


class BaseAudioContentProvider(BaseContentProvider):
    content_type: int = AUDIO
    content_type_ru = 'аудио'
    content_type_en = 'audio'


class BaseTextContentProvider(BaseContentProvider):
    content_type: int = TEXT
    content_type_ru = 'текст'
    content_type_en = 'text'


class VKVideoContentProvider(BaseVideoContentProvider):
    provider_id = 1
    provider_name = 'VK'
    video_src_pattern = 'https://vk.com/video_ext.php?{}'
    remote_url_pattern = 'https://vk.com/video{}'

    def get_remote_url(self) -> str:
        data = self.get_query_data()
        return self.remote_url_pattern.format(f'{data.get("oid")}_{data.get("id")}')

    def get_query_data(self) -> dict[str, str]:
        return {key: value for key, value in parse.parse_qsl(self.instance.text)}

    def finish_modify_data(self, parser: IframeParser):
        self.instance.text = parser.get_src().query


class YouTubeVideoContentProvider(BaseVideoContentProvider):
    provider_id = 2
    provider_name = 'YouTube'
    video_src_pattern = 'https://www.youtube.com/embed/{}'
    remote_url_pattern = 'https://www.youtube.com/watch?v={}'

    def finish_modify_data(self, parser: IframeParser):
        self.instance.text = parser.get_src().path.rpartition('/')[2]


class RuTubeVideoContentProvider(BaseVideoContentProvider):
    provider_id = 3
    provider_name = 'RuTube'
    video_src_pattern = 'https://rutube.ru/play/embed/{}'
    remote_url_pattern = 'https://rutube.ru/video/{}/'

    def finish_modify_data(self, parser: IframeParser):
        self.instance.text = parser.get_src().path.rpartition('/')[2]


class VKAudioContentProvider(BaseAudioContentProvider):
    provider_id = 1
    provider_name = 'VK'
    _template_name = 'audio-vk'
    remote_url_pattern = 'https://vk.com/podcast{}'
    # provider_priority = 3

    @property
    def audio_id(self) -> str:
        return self.instance.text.split(',')[0]

    @property
    def audio_hash(self) -> str:
        return self.instance.text.split(',')[1]

    def get_context(self) -> dict[str, Any]:
        return {'audio_id': self.audio_id, 'audio_hash': self.audio_hash}

    def get_remote_url(self) -> str:
        return self.remote_url_pattern.format(self.audio_id)

    def modify_data(self):
        parser = VKScriptParser()
        parser.feed(self.instance.text)
        data = parser.get_parsed_data()
        if data:
            self.instance.text = data


class YandexAudioContentProvider(BaseAudioContentProvider):
    provider_id = 2
    provider_name = 'Yandex'
    _template_name = 'audio-yandex'
    audio_src_pattern = 'https://music.yandex.ru/iframe/#track/{}/{}'
    remote_url_pattern = 'https://music.yandex.ru/album/{}/track/{}'

    @property
    def album_id(self):
        return self.instance.text.split(',')[0]

    @property
    def track_id(self):
        return self.instance.text.split(',')[1]

    def get_context(self) -> dict[str, Any]:
        return {'audio_src': self.audio_src_pattern.format(self.track_id, self.album_id)}

    def get_remote_url(self) -> str:
        return self.remote_url_pattern.format(self.album_id, self.track_id)

    def modify_data(self):
        parser = IframeParser()
        parser.feed(self.instance.text)
        if parser.valid_iframe():
            album_id, track_id, *_ = parser.get_src().fragment.split('/')[::-1]
            self.instance.text = f'{album_id},{track_id}'


class SimpleTextContentProvider(BaseTextContentProvider):
    provider_id = 1
    provider_name = ''

    def get_context(self) -> dict[str, Any]:
        return {'text': self.instance.text}


providers_map, content_types_map = BaseContentProvider.get_providers_map()
