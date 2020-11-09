from django.db import models
from django.urls import reverse

from spirsa.constants import (
    THUMBNAIL_WIDTH,
    THUMBNAIL_VARIATION_SETS,
)
from spirsa.mixins import (
    PublishedModelMixin,
    PublishedQuerySet,
    SlugModelMixin,
    SrcsetModelMixin,
    TimeStampModelMixin,
)
from spirsa.utils import (
    create_image_variations,
    get_artwork_image_path,
    get_artwork_thumbnail_path,
)


class ArtworkManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('cls_dimension')

    def digital(self):
        return self.get_queryset().filter(is_traditional=False)

    def traditional(self):
        return self.get_queryset().filter(is_traditional=True)


class Artwork(SrcsetModelMixin, PublishedModelMixin, SlugModelMixin, TimeStampModelMixin):
    title = models.CharField(max_length=50, unique=True)
    short_description = models.TextField(max_length=1000, blank=True)
    is_traditional = models.BooleanField(default=False)
    image = models.ImageField(upload_to=get_artwork_image_path, blank=True, null=True)
    ordering = models.PositiveIntegerField(
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
        super(SrcsetModelMixin, self).save(args, kwargs)
        super().save(args, kwargs)

        if self.image:
            create_image_variations(self)

    def get_absolute_url(self):
        return reverse('art:artwork-detail', kwargs={'slug': self.slug})


class ArtworkThumbnail(SrcsetModelMixin, PublishedModelMixin, TimeStampModelMixin):
    title = models.CharField(verbose_name='image title', max_length=100)
    image = models.ImageField(
        upload_to=get_artwork_thumbnail_path, blank=True, null=True,
        help_text='Use a jpeg or png image (960x960 or larger).'
    )
    ordering = models.PositiveIntegerField(
        default=0, help_text='Higher number equals higher position. Leave 0 for default.'
    )
    artwork = models.ForeignKey(
        'art.Artwork', on_delete=models.CASCADE, related_name='thumbnails'
    )

    class Meta:
        verbose_name = 'Artwork thumbnail'
        verbose_name_plural = 'Artwork thumbnails'
        ordering = ('-ordering', '-created_at', )

    def __str__(self):
        return '{}, {}'.format(self.title, self.artwork.title)

    def save(self, *args, **kwargs):
        super(SrcsetModelMixin, self).save(args, kwargs)
        super().save(args, kwargs)

        if self.image:
            create_image_variations(self, THUMBNAIL_WIDTH, THUMBNAIL_VARIATION_SETS)


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
