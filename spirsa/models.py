from django.db import models

from spirsa.constants import (
    SMALL_VARIATION_SETS,
    SMALL_WIDTH,
)
from spirsa.mixins import (
    SrcsetModelMixin,
    TimeStampModelMixin,
)
from spirsa.utils import (
    create_image_variations,
    get_contact_image_path,
)


class AboutContactInformation(SrcsetModelMixin, TimeStampModelMixin):
    title = models.CharField(verbose_name='image title', max_length=100, blank=True)
    image = models.ImageField(
        upload_to=get_contact_image_path, blank=True, null=True,
        help_text='Use a jpeg or png image (760x760 or larger).'
    )
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
        super(SrcsetModelMixin, self).save(args, kwargs)
        super().save(args, kwargs)

        if self.image:
            create_image_variations(self, SMALL_WIDTH, SMALL_VARIATION_SETS)


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
