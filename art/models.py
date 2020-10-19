from django.db import models

from spirsa.mixins import (
    PublishedModelMixin,
    PublishedQuerySet,
    SlugModelMixin,
    TimeStampModelMixin,
)
from spirsa.utils import create_image_variations


class ArtworkManager(models.Manager):
    def digital(self):
        return super().get_queryset().filter(is_traditional=False)

    def traditional(self):
        return super().get_queryset().filter(is_traditional=True)


class Artwork(PublishedModelMixin, SlugModelMixin, TimeStampModelMixin):
    title = models.CharField(max_length=50)
    short_description = models.TextField(max_length=500)
    is_traditional = models.BooleanField(default=False)
    image = models.ImageField(upload_to='artwork/%Y/%m/', blank=True, null=True)
    image_timestamp = models.FloatField(default=0.0)
    srcsets = models.JSONField(blank=True, null=True)
    ordering = models.IntegerField(
        default=0, help_text='Higher number equals higher position. Leave 0 for default.'
    )
    keywords = models.ManyToManyField('art.Keyword', blank=True)

    objects = ArtworkManager.from_queryset(PublishedQuerySet)()

    class Meta:
        verbose_name = 'Artwork'
        verbose_name_plural = 'Artworks'
        ordering = ('-ordering', '-created_at', )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(args, kwargs)

        if self.image:
            create_image_variations(self)


class Keyword(PublishedModelMixin, SlugModelMixin):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Keyword'
        verbose_name_plural = 'Keywords'
        ordering = ('name', )

    def __str__(self):
        return self.name
