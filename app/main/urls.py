from django.urls import path, include


urlpatterns = [
    path('tickets/', include('tickets.urls')),
    path('', include('lessons.urls')),
]
