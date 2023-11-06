from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return (
            super().get_queryset()
            .filter(
                pub_date__lte=timezone.now(),
                is_published=True,
                category__is_published=True
            )
        )
