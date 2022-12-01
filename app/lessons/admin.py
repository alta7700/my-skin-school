import os

from django.contrib import admin

from lessons.models import School, Lesson, Content
from main.admin import ModelAdmin, default_site
from school import settings


class ContentInlineAdmin(admin.TabularInline):
    model = Content
    extra = 1
    fields = ('provider', 'text')


class SchoolProxyAdmin(ModelAdmin):
    list_display = ('title', 'position')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('position',)
    list_display_links = ('title',)
    fieldsets = (
        (None, {'fields': ('position', 'title', 'slug', 'description', 'cover')}),
        (None, {'fields': ('school',), 'classes': ('hidden',)})
    )
    add_fieldsets = (
        (None, {'fields': ('position', 'title', 'slug', 'description', 'cover')}),
    )

    inlines = (ContentInlineAdmin, )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(school=self.model.base)

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial['school'] = self.model.base.id
        return initial


def refresh_urls():
    from django.urls.base import clear_url_caches
    from importlib import reload, import_module
    reload(import_module(settings.ROOT_URLCONF))
    clear_url_caches()


def add_school_to_lessons_admin(obj: School):
    meta = type('Meta', (object,), {
        'proxy': True, 'verbose_name': f'Урок {obj.title}', 'verbose_name_plural': obj.title
    })
    proxy_model_dict = {'Meta': meta, 'base': obj, '__module__': 'main'}
    SchoolProxyModel = type(obj.slug.replace("-", "_"), (Lesson,), proxy_model_dict)
    default_site.register(SchoolProxyModel, SchoolProxyAdmin)


@admin.register(School)
class SchoolsAdmin(ModelAdmin):
    list_display = ('title', 'position')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('position',)
    list_display_links = ('title',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            add_school_to_lessons_admin(obj)
            refresh_urls()


if not os.environ.get('MIGRATION_ALERT'):
    for school in School.objects.all():
        add_school_to_lessons_admin(school)
    refresh_urls()
