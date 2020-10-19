from django.db import models

from spirsa.mixins import TimeStampModelMixin


class MetaInformation(TimeStampModelMixin):
    meta_title = models.CharField(max_length=100)
    meta_description = models.TextField(max_length=500)
    meta_keywords = models.TextField(
        max_length=200, help_text='Separate each keyword group with a comma.'
    )
    meta_image = models.ImageField(
        upload_to='%Y/%m/', blank=True, null=True,
        help_text='1200x630 or larger with simiar aspect ratio.'
    )
    meta_image_title = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Meta information'
        verbose_name_plural = 'Meta information'

    def __str__(self):
        return self.meta_title
