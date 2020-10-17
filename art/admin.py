from django.contrib import admin

from art.models import (
    Artwork,
    Color,
    Tag,
)
from spirsa.mixins import AutoSlugAdminMixin
from spirsa.utils import get_preview_image


class ArtworkAdmin(AutoSlugAdminMixin):
    list_display = (
        'title', 'slug', 'is_traditional', 'is_published', 'ordering', 'created_at',
        'image_preview_thumb',
    )
    list_editable = ('is_traditional', 'is_published', 'ordering', )
    fields = (
        'title', 'slug', 'is_traditional', 'is_published', 'ordering', 'short_description',
        'tag', 'image', 'image_preview',
    )
    readonly_fields = ('image_preview', )

    def image_preview(self, obj):
        return get_preview_image(obj.image, 500)

    def image_preview_thumb(self, obj):
        return get_preview_image(obj.image, 100)


class ColorAdmin(admin.ModelAdmin):
    list_display_links = (
        '__str__',
    )
    list_display = (
        '__str__', 'is_published', 'name', 'hex_value',
    )
    list_editable = (
        'is_published', 'name', 'hex_value',
    )
    fields = (
        'name', 'is_published', 'hex_value',
    )


class TagAdmin(AutoSlugAdminMixin):
    list_display_links = (
        '__str__',
    )
    list_display = (
        '__str__', 'is_published', 'name', 'slug', 'color',
    )
    list_editable = (
        'is_published', 'name', 'slug', 'color',
    )
    fields = (
        'name', 'is_published', 'slug', 'color',
    )


admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Tag, TagAdmin)
