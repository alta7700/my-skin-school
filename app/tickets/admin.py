from django.contrib import admin

from main.admin import ModelAdmin
from tickets.models import Ticket


@admin.register(Ticket)
class TicketAdmin(ModelAdmin):
    list_display = ('first_name', 'theme', 'processed')
    readonly_fields = ('first_name', 'email', 'phone', 'theme', 'message',)
    list_filter = ('processed',)
    ordering = ('processed', )
