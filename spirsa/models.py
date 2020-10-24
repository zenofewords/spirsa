from django.db import models

from spirsa.constants import (
    PROFILE_VARIATION_SETS,
    PROFILE_WIDTH,
)
from spirsa.mixins import TimeStampModelMixin
from spirsa.utils import create_image_variations


class AbountContactInformation(TimeStampModelMixin):
    image = models.ImageField(
        upload_to='spirsa/%Y/%m/', blank=True, null=True,
        help_text='Use a jpeg or png image (700x700 or larger).'
    )
    image_title = models.CharField(max_length=100, blank=True, null=True)
    image_timestamp = models.FloatField(default=0.0)
    srcsets = models.JSONField(blank=True, null=True)
    contact_email = models.EmailField(max_length=100, blank=True)

    top_section_title = models.CharField(max_length=100, blank=True)
    top_section_text = models.TextField(max_length=1500, blank=True)
    bottom_section_title = models.CharField(max_length=100, blank=True)
    bottom_section_text = models.TextField(max_length=500, blank=True)

    class Meta:
        verbose_name = 'About and contact page information'
        verbose_name_plural = 'About and contact page information'

    def __str__(self):
        return 'About and contact page information'

    def save(self, *args, **kwargs):
        super().save(args, kwargs)

        if self.image:
            create_image_variations(self, PROFILE_WIDTH, PROFILE_VARIATION_SETS)


class MetaInformation(TimeStampModelMixin):
    meta_title = models.CharField(max_length=100)
    meta_description = models.TextField(max_length=500)
    meta_keywords = models.TextField(
        max_length=200, help_text='Separate each keyword group with a comma.'
    )
    meta_image = models.ImageField(
        upload_to='spirsa/%Y/%m/', blank=True, null=True,
        help_text='Use a jpeg or png image (1200x630 or larger).'
    )
    meta_image_title = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Meta information'
        verbose_name_plural = 'Meta information'

    def __str__(self):
        return self.meta_title
