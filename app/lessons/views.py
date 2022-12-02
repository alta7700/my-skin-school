from django.db.models import Count
from django.views.generic import DetailView, ListView

from main.views import BaseContextMixin
from lessons.models import School, Lesson


class SchoolListView(BaseContextMixin, ListView):

    title = 'Школа здоровья'
    context_object_name = 'schools'
    queryset = School.objects.all().annotate(lessons_count=Count('lessons')).order_by('position')

    def get_navbar_history(self, **kwargs) -> dict[str, str]:
        return {'Школы здоровья': '#'}


class SchoolDetailView(BaseContextMixin, DetailView):

    context_object_name = 'school'
    school_exist: bool
    object: School
    template_name = 'lessons/school_detail.html'

    queryset = School.objects.prefetch_related('lessons')

    def get_object(self, queryset=None):
        return self.queryset.get_or_none(slug=self.kwargs['slug'])

    def get_navbar_history(self, **kwargs) -> dict[str, str]:
        if self.object:
            return {'Школы здоровья': '/', self.object.title: '#'}  # self.object.get_absolute_url()}
        return {'Школы здоровья': '/'}

    def get_title(self) -> str:
        return self.object.title if self.object else 'Ничего не нашёл:('


class LessonDetailView(BaseContextMixin, DetailView):

    context_object_name = 'lesson'
    school_exist: bool
    object: Lesson
    template_name = 'lessons/lesson_detail.html'

    queryset = Lesson.objects.select_related('school').prefetch_related('contents')

    def get_title(self) -> str:
        return str(self.object) if self.object else 'Ничего не нашёл:('

    def get_object(self, queryset=None):
        return self.queryset.get_or_none(school__slug=self.kwargs['slug'], position=self.kwargs['position'])

    def get_navbar_history(self, **kwargs) -> dict[str, str]:
        if self.object:
            return {
                'Школы здоровья': '/',
                self.object.school.title: self.object.school.get_absolute_url(),
                f'Урок {self.object.position}': '#',  # self.object.get_absolute_url()
            }
        return {'Школы здоровья': '/'}
