from datetime import datetime
from functools import cached_property
from random import choices
from string import hexdigits
from typing import TypeVar

from django.db import models
from django.urls import reverse

from main.managers import Manager
from lessons.content_providers import BaseContentProvider, providers_map, content_types_map, VIDEO, AUDIO, TEXT


T = TypeVar('T')


def upload_to(instance, filename: str):
    base = instance._meta.model_name
    random_name = "".join(choices(hexdigits, k=10))
    ext = filename.rpartition(".")[2] or "png"
    return datetime.now().strftime(f'{base}/%Y/%m/%d/{random_name}.{ext}')


class School(models.Model):
    id: int
    position: int = models.SmallIntegerField('Позиция', unique=True)
    title: str = models.CharField('Название', unique=True, max_length=40)
    slug: str = models.SlugField('Синоним', unique=True, max_length=50)
    cover = models.ImageField(
        'Обложка', max_length=300, width_field='cower_w', height_field='cower_h', default='',
        upload_to=upload_to, blank=True
    )
    cower_w: int = models.PositiveSmallIntegerField('Ширина обложки', editable=False, default=0)
    cower_h: int = models.PositiveSmallIntegerField('Высота обложки', editable=False, default=0)

    objects = Manager()

    class Meta:
        db_table = 'schools'
        verbose_name = '_Школа'
        verbose_name_plural = '_Школы'
        ordering = ('position', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('school_lessons', kwargs={'slug': self.slug})


class Lesson(models.Model):
    id: int
    school: School = models.ForeignKey(verbose_name='Школа', to=School, on_delete=models.RESTRICT,
                                       related_name='lessons')
    position: int = models.PositiveSmallIntegerField('Номер урока')
    title: str = models.CharField('Название', max_length=80)
    slug: str = models.SlugField('Синоним', unique=True, max_length=90)
    description: str = models.CharField('Описание', max_length=300)

    cover = models.ImageField(
        'Обложка', max_length=300, width_field='cower_w', height_field='cower_h', default='',
        upload_to=upload_to, blank=True
    )
    cower_w: int = models.PositiveSmallIntegerField('Ширина обложки', editable=False, default=0)
    cower_h: int = models.PositiveSmallIntegerField('Высота обложки', editable=False, default=0)

    objects = Manager()

    class Meta:
        db_table = 'lessons'
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('position',)
        unique_together = (('position', 'school'), )

    def __str__(self):
        return f'{self.school}. Урок {self.position}. {self.title}'

    def get_absolute_url(self):
        return reverse('lesson', kwargs={'slug': self.school.slug, 'position': self.position})

    def get_available_content_types(self):
        types = set()
        for content in self.contents.all():
            types.add(content.type)
        return [(t, *content_types_map[t]) for t in sorted(types)]

    def get_content(self, content_type: int) -> list["Content"]:
        return [content for content in self.contents.all() if content.type == content_type]

    @staticmethod
    def sort_by_priority(data: T) -> T:
        return sorted(data, key=lambda x: x.get_priority())

    @cached_property
    def videos(self) -> list["Content"]:
        return self.sort_by_priority(self.get_content(VIDEO))

    def main_video(self):
        return self.videos[0] if self.videos else None

    @cached_property
    def audios(self) -> list["Content"]:
        return self.sort_by_priority(self.get_content(AUDIO))

    def main_audio(self):
        return self.audios[0] if self.audios else None

    @cached_property
    def texts(self) -> list["Content"]:
        return self.sort_by_priority(self.get_content(TEXT))

    def main_text(self):
        return self.texts[0] if self.texts else None


class Content(models.Model):
    id: int
    lesson: Lesson = models.ForeignKey(verbose_name='Урок', to=Lesson, on_delete=models.CASCADE,
                                       related_name='contents')
    provider: str = models.CharField('Тип', max_length=10, choices=BaseContentProvider.get_choices())
    text: str = models.TextField('Текст')

    class Meta:
        db_table = 'lesson_content'
        verbose_name = 'Контент урока'
        verbose_name_plural = 'Контент уроков'
        ordering = ('provider', )
        unique_together = (('lesson', 'provider'),)

    _renderer = None

    def get_renderer(self) -> BaseContentProvider:
        if not self._renderer:
            self._renderer = providers_map[self.provider](self)
        return self._renderer

    def render(self):
        return self.get_renderer().render()

    def render_link(self):
        return self.get_renderer().render_link()

    @property
    def type(self) -> int:
        return int(self.provider.split(',')[0])

    @property
    def provider_id(self) -> int:
        return int(self.provider.split(',')[1])

    @property
    def group_block_id(self) -> str:
        return self.get_renderer().group_block_id

    def get_priority(self) -> int:
        return self.get_renderer().priority

    def clean(self):
        self.get_renderer().modify_data()
