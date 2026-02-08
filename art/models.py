from django.db import models
from django.urls import reverse

from spirsa.constants import (
    THUMBNAIL_VARIATION_SETS,
    THUMBNAIL_WIDTH,
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


class CollectionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def for_navigation(self):
        return self.get_queryset().filter(show_in_navigation=True)


class ArtworkManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("cls_dimension")

    def featured(self):
        return self.get_queryset().filter(collection__slug="featured")


class Collection(SlugModelMixin, TimeStampModelMixin):
    title = models.CharField(max_length=50, unique=True)
    artworks = models.ManyToManyField("art.Artwork", blank=True)
    show_in_navigation = models.BooleanField(default=False)
    ordering = models.PositiveIntegerField(default=1, help_text="Descending (largest to smallest)")

    objects = CollectionManager.from_queryset(models.QuerySet)()

    class Meta:
        verbose_name = "Collection"
        verbose_name_plural = "Collections"
        ordering = (
            "-ordering",
            "show_in_navigation",
        )

    def __str__(self):
        return self.title


class Artwork(SrcsetModelMixin, PublishedModelMixin, SlugModelMixin, TimeStampModelMixin):
    title = models.CharField(max_length=50, unique=True)
    short_description = models.TextField(max_length=1000, blank=True)
    image = models.ImageField(upload_to=get_artwork_image_path, blank=True, null=True)
    ordering = models.PositiveIntegerField(default=1, help_text="Descending (largest to smallest)")
    keywords = models.ManyToManyField("art.Keyword", blank=True)

    objects = ArtworkManager.from_queryset(PublishedQuerySet)()

    class Meta:
        verbose_name = "Artwork"
        verbose_name_plural = "Artworks"
        ordering = (
            "-ordering",
            "-created_at",
        )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(SrcsetModelMixin, self).save(args, kwargs)
        super().save(args, kwargs)

        if self.image:
            create_image_variations(self)

    def get_absolute_url(self, slug):
        return reverse("art:artwork-detail", kwargs={"slug": slug, "artwork_slug": self.slug})


class ArtworkThumbnail(SrcsetModelMixin, PublishedModelMixin, TimeStampModelMixin):
    title = models.CharField(verbose_name="image title", max_length=100)
    image = models.ImageField(
        upload_to=get_artwork_thumbnail_path,
        blank=True,
        null=True,
        help_text="Use a jpeg or png image (960x960 or larger).",
    )
    ordering = models.PositiveIntegerField(
        default=0, help_text="Higher number equals higher position. Leave 0 for default."
    )
    artwork = models.ForeignKey("art.Artwork", on_delete=models.CASCADE, related_name="thumbnails")

    class Meta:
        verbose_name = "Artwork thumbnail"
        verbose_name_plural = "Artwork thumbnails"
        ordering = (
            "-ordering",
            "-created_at",
        )

    def __str__(self):
        return f"{self.title}, {self.artwork.title}"

    def save(self, *args, **kwargs):
        super(SrcsetModelMixin, self).save(args, kwargs)
        super().save(args, kwargs)

        if self.image:
            create_image_variations(self, THUMBNAIL_WIDTH, THUMBNAIL_VARIATION_SETS)


class Keyword(PublishedModelMixin, SlugModelMixin):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Keyword"
        verbose_name_plural = "Keywords"
        ordering = ("name",)

    def __str__(self):
        return self.name


class CLSDimension(models.Model):
    list_height = models.IntegerField(blank=True, null=True)
    list_width = models.IntegerField(blank=True, null=True)
    detail_height = models.IntegerField(blank=True, null=True)
    detail_width = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "CLS dimension"
        verbose_name_plural = "CLS dimensions"

    def __str__(self):
        return f"list width: {self.list_width} height: {self.list_height}, detail width: {self.detail_width}, height: {self.detail_height}"
