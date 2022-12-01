from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin, GroupAdmin

from main.admin import ModelAdminMixin, default_site
from users.forms import MyUserCreationForm
from users.models import User, Group


dates = ('last_login', 'date_joined')
fio = ('last_name', 'first_name', 'fathers_name')


@admin.register(User)
class UserAdmin(DefaultUserAdmin, ModelAdminMixin):
    readonly_fields = dates
    add_fieldsets = (
        ('Логины', {'fields': User.LOGIN_FIELDS, 'classes': ('wide',)}),
        ('Пароли', {'fields': ('password1', 'password2'), 'classes': ('wide',)})
    )
    fieldsets = (
        ('Логины', {'fields': (*User.LOGIN_FIELDS, 'password')}),
        ('Личная информация', {'fields': fio}),
        ('Права', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
        ('Важные даты', {'fields': dates}),
    )
    add_form = MyUserCreationForm

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        return *self.readonly_fields, 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or obj is None or request.user.id == obj.id


default_site.register(Group, GroupAdmin)
