from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet as DefaultQuerySet
from django.db.models.manager import BaseManager


class QuerySet(DefaultQuerySet):

    def get_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except ObjectDoesNotExist:
            pass


Manager = BaseManager.from_queryset(QuerySet, class_name='Manager')

