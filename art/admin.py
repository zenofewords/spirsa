from django.contrib import admin

from art.models import (
    Artwork,
    ArtworkThumbnail,
    Keyword,
)
from spirsa.mixins import AutoSlugAdminMixin
from spirsa.utils import get_preview_image


class ArtworkThumbnailInline(admin.TabularInline):
    model = ArtworkThumbnail
    fields = (
        'title', 'image', 'artwork', 'is_published', 'ordering', 'image_preview_thumb',
    )
    readonly_fields = ('image_preview_thumb', )

    def image_preview_thumb(self, obj):
        return get_preview_image(obj.image, 100)


class ArtworkAdmin(AutoSlugAdminMixin):
    search_fields = ('title', 'slug', )
    list_display = (
        'title', 'slug', 'is_traditional', 'is_published', 'ordering', 'created_at',
        'image_preview_thumb',
    )
    list_editable = ('is_traditional', 'is_published', 'ordering', )
    fields = (
        'title', 'slug', 'is_traditional', 'is_published', 'ordering', 'short_description',
        'image', 'image_preview', 'keywords',
    )
    autocomplete_fields = ('keywords', )
    readonly_fields = ('image_preview', )
    inlines = [ArtworkThumbnailInline, ]

    def image_preview(self, obj):
        return get_preview_image(obj.image, 500)

    def image_preview_thumb(self, obj):
        return get_preview_image(obj.image, 100)


class ArtworkThumbnailAdmin(admin.ModelAdmin):
    search_fields = ('title', 'artwork__title', 'artwork__slug', )
    list_display = (
        'artwork', 'is_published', 'ordering', 'created_at', 'image_preview_thumb',
    )
    list_editable = ('is_published', 'ordering', )
    fields = (
        'title', 'image', 'artwork', 'is_published', 'ordering', 'image_preview',
    )
    autocomplete_fields = ('artwork', )
    readonly_fields = ('image_preview', )

    def image_preview(self, obj):
        return get_preview_image(obj.image, 500)

    def image_preview_thumb(self, obj):
        return get_preview_image(obj.image, 100)


class KeywordAdmin(AutoSlugAdminMixin):
    search_fields = ('name', 'slug', )
    list_display_links = (
        '__str__',
    )
    list_display = (
        '__str__', 'is_published', 'name', 'slug',
    )
    list_editable = (
        'is_published', 'name', 'slug',
    )
    fields = (
        'name', 'is_published', 'slug',
    )


admin.site.register(ArtworkThumbnail, ArtworkThumbnailAdmin)
admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(Keyword, KeywordAdmin)
