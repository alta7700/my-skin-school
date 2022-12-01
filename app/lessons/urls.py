from django.urls import path

from .views import *


urlpatterns = [
    path('', SchoolListView.as_view(), name='school_list'),
    path('<slug:slug>', SchoolDetailView.as_view(), name='school_lessons'),
    path('<slug:slug>/<int:position>', LessonDetailView.as_view(), name='lesson'),
]
