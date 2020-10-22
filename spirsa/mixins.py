from django.apps import apps
from django.contrib import admin
from django.db import models
from django.views.generic import TemplateView
from django.utils.text import slugify

from spirsa.utils import get_site_url


class AutoSlugAdminMixin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.slug == '':
            obj.slug = slugify(getattr(obj, 'title', None) or getattr(obj, 'name'), '')
        obj.save()


class MetaViewMixin(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'meta_url': get_site_url(self.request),
        })

        MetaInformation = apps.get_model('spirsa', 'MetaInformation')
        info = MetaInformation.objects.last()
        if info:
            context.update({
                'meta_title': info.meta_title,
                'meta_description': info.meta_description,
                'meta_keywords': info.meta_keywords,
                'meta_image': info.meta_image,
                'meta_image_title': info.meta_image_title,
            })
        return context


class PublishedQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)


class PublishedModelMixin(models.Model):
    is_published = models.BooleanField(default=False)

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
