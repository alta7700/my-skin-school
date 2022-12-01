from django.urls import path

from tickets.views import *

urlpatterns = [
    path('', add_ticket)
]
