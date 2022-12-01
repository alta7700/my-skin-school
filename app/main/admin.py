from django.contrib import admin
from django.contrib.admin import AdminSite
from django.template.loader import select_template
from django.contrib.auth.models import Group


default_site: AdminSite = admin.site
default_site.disable_action('delete_selected')
default_site.index_template = 'main/admin/index.html'
default_site.app_index_template = 'main/admin/app_index.html'

default_site.site_title = "Моя-кожа.рф"
default_site.site_header = "Администрирование Моя-кожа.рф"
default_site.index_title = "Администрирование"


default_site.unregister(Group)


class ModelAdminMixin:
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        for attr in ('change_form', 'change_list'):
            setattr(self, f'{attr}_template', select_template((
                f'{self.opts.app_label}/admin/{self.opts.model_name}/{attr}.html',
                f'{self.opts.app_label}/admin/{attr}.html',
                f'main/admin/{attr}.html'
            )).template.name)

    @staticmethod
    def get_custom_object_tools_list(context: dict) -> list[dict]:
        if not (ot := context.get('custom_object_tools_items')):
            context['custom_object_tools_items'] = ot = []
        return ot

    def get_list_display_links(self, request, list_display):
        return self.list_display_links or list_display


class ModelAdmin(ModelAdminMixin, admin.ModelAdmin):
    pass
