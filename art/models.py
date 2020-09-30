from django.db import models

from spirsa.mixins import (
    PublishedModelMixin,
    SlugModelMixin,
    TimeStampModelMixin,
)
from spirsa.utils import create_image_variations


class Artwork(PublishedModelMixin, SlugModelMixin, TimeStampModelMixin):
    title = models.CharField(max_length=50)
    short_description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='artwork/%Y/%m/', blank=True, null=True)
    image_timestamp = models.FloatField(default=0.0)
    srcsets = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = 'Artwork'
        verbose_name_plural = 'Artworks'
        ordering = ('created_at', )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(args, kwargs)

        if self.image:
            create_image_variations(self)
