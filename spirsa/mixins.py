from django.contrib import admin
from django.db import models
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import TemplateView
from django.utils.text import slugify


class AutoSlugAdminMixin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.slug == '':
            obj.slug = slugify(obj.title)
        obj.save()


class MetaViewMixin(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = {
            'meta_url': '{}://{}'.format(
                self.request.scheme, get_current_site(self.request)
            ),
            'meta_title': '',
            'meta_description': '',
            'meta_image_alt': '',
        }
        context.update(data)
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
        max_length=50, blank=True,
        help_text='Leave empty to create from the title'
    )

    class Meta:
        abstract = True


class TimeStampModelMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
