from django.apps import apps
from django.contrib import admin
from django.db import models
from django.utils.text import slugify

from spirsa.utils import (
    clean_meta_description,
    get_site_url
)


class AutoSlugAdminMixin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.slug == '':
            obj.slug = slugify(getattr(obj, 'title', None) or getattr(obj, 'name'), '')
        obj.save()


class MetaViewMixin():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'base_url': '{}'.format(get_site_url(self.request)),
            'meta_type': 'website',
        })

        MetaInformation = apps.get_model('spirsa', 'MetaInformation')
        info = MetaInformation.objects.last()
        if info:
            context.update({
                'meta_title_base': info.meta_title,
                'meta_description': clean_meta_description(info.meta_description),
                'meta_keywords': info.meta_keywords,
                'meta_image': info.meta_image if info.meta_image else None,
                'meta_image_title': info.meta_image_title,
            })
        return context


class PublishedQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published=True)


class PublishedModelMixin(models.Model):
    published = models.BooleanField(default=True)

    objects = PublishedQuerySet.as_manager()

    class Meta:
        abstract = True


class SlugModelMixin(models.Model):
    slug = models.SlugField(
        max_length=50, blank=True, unique=True,
        help_text='Leave empty to use title or name'
    )

    class Meta:
        abstract = True


class TimeStampModelMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SrcsetModelMixin(models.Model):
    image_timestamp = models.FloatField(default=0.0)
    srcsets = models.JSONField(blank=True, null=True)
    cls_dimension = models.OneToOneField(
        'art.CLSDimension', on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.cls_dimension:
            CLSDimension = apps.get_model('art', 'CLSDimension')
            self.cls_dimension = CLSDimension()
            self.cls_dimension.save()
        if not self.image:
            self.image_timestamp = 0
            self.srcsets = None
