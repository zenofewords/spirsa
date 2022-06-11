from django.contrib import admin

from art.models import (
    Collection,
    Artwork,
    ArtworkThumbnail,
    Keyword,
)
from spirsa.mixins import AutoSlugAdminMixin
from spirsa.utils import get_preview_image


class ArtworkThumbnailInline(admin.TabularInline):
    model = ArtworkThumbnail
    fields = (
        'title', 'image', 'artwork', 'published', 'ordering', 'image_preview_thumb',
    )
    readonly_fields = ('image_preview_thumb', )

    def image_preview_thumb(self, obj):
        return get_preview_image(obj.image, 100)


class CollectionAdmin(AutoSlugAdminMixin):
    search_fields = ('title', 'slug', )
    list_display = ('title', 'slug', )
    fields = ('title', 'slug', 'artworks', )


class ArtworkAdmin(AutoSlugAdminMixin):
    search_fields = ('title', 'slug', )
    list_display = (
        'title', 'slug', 'published', 'ordering', 'created_at',
        'image_preview_thumb',
    )
    list_editable = ('published', 'ordering', )
    fields = (
        'title', 'slug', 'published', 'ordering',
        'short_description', 'image', 'image_preview', 'keywords',
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
        'artwork', 'published', 'ordering', 'created_at', 'image_preview_thumb',
    )
    list_editable = ('published', 'ordering', )
    fields = (
        'title', 'image', 'artwork', 'published', 'ordering', 'image_preview',
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
        '__str__', 'published', 'name', 'slug',
    )
    list_editable = (
        'published', 'name', 'slug',
    )
    fields = (
        'name', 'published', 'slug',
    )


admin.site.register(ArtworkThumbnail, ArtworkThumbnailAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(Keyword, KeywordAdmin)
