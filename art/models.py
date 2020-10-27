from django.db import models
from django.urls import reverse

from spirsa.constants import (
    SMALL_VARIATION_SETS,
    SMALL_WIDTH,
)
from spirsa.mixins import (
    PublishedModelMixin,
    PublishedQuerySet,
    SlugModelMixin,
    TimeStampModelMixin,
)
from spirsa.utils import create_image_variations


class ArtworkManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('cls_dimension')

    def digital(self):
        return self.get_queryset().filter(is_traditional=False)

    def traditional(self):
        return self.get_queryset().filter(is_traditional=True)


class Artwork(PublishedModelMixin, SlugModelMixin, TimeStampModelMixin):
    title = models.CharField(max_length=50, unique=True)
    short_description = models.TextField(max_length=500, blank=True)
    is_traditional = models.BooleanField(default=False)
    image = models.ImageField(upload_to='artwork/%Y/%m/', blank=True, null=True)
    image_timestamp = models.IntegerField(default=0)
    srcsets = models.JSONField(blank=True, null=True)
    ordering = models.IntegerField(
        default=0, help_text='Higher number equals higher position. Leave 0 for default.'
    )
    keywords = models.ManyToManyField('art.Keyword', blank=True)
    cls_dimension = models.OneToOneField(
        'art.CLSDimension', on_delete=models.CASCADE, blank=True, null=True
    )

    objects = ArtworkManager.from_queryset(PublishedQuerySet)()

    class Meta:
        verbose_name = 'Artwork'
        verbose_name_plural = 'Artworks'
        ordering = ('-ordering', '-created_at', )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.cls_dimension:
            self.cls_dimension = CLSDimension()
            self.cls_dimension.save()
        if not self.image:
            self.image_timestamp = 0
            self.srcsets = None
        super().save(args, kwargs)

        if self.image:
            create_image_variations(self)

    def get_absolute_url(self):
        return reverse('art:artwork-detail', kwargs={'slug': self.slug})


class ArtworkDetail(PublishedModelMixin, TimeStampModelMixin):
    image = models.ImageField(upload_to='artwork/detail/%Y/%m/', blank=True, null=True)
    image_title = models.CharField(max_length=100, blank=True)
    image_timestamp = models.IntegerField(default=0)
    srcsets = models.JSONField(blank=True, null=True)
    ordering = models.IntegerField(
        default=0, help_text='Higher number equals higher position. Leave 0 for default.'
    )
    artwork = models.ForeignKey(
        'art.Artwork', on_delete=models.CASCADE, related_name='details'
    )

    class Meta:
        verbose_name = 'Artwork detail'
        verbose_name_plural = 'Artwork details'
        ordering = ('-ordering', '-created_at', )

    def __str__(self):
        return '{}, {}'.format(self.artwork.title, self.image_title)

    def save(self, *args, **kwargs):
        if not self.image:
            self.image_timestamp = 0
            self.srcsets = None
        super().save(args, kwargs)

        if self.image:
            create_image_variations(self, SMALL_WIDTH, SMALL_VARIATION_SETS)


class Keyword(PublishedModelMixin, SlugModelMixin):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Keyword'
        verbose_name_plural = 'Keywords'
        ordering = ('name', )

    def __str__(self):
        return self.name


class CLSDimension(models.Model):
    list_height = models.IntegerField(blank=True, null=True)
    list_width = models.IntegerField(blank=True, null=True)
    detail_height = models.IntegerField(blank=True, null=True)
    detail_width = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'CLS dimension'
        verbose_name_plural = 'CLS dimensions'

    def __str__(self):
        return 'list width: {} height: {}, detail width: {}, height: {}'.format(
            self.list_width, self.list_height, self.detail_width, self.detail_height
        )
