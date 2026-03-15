from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin

from art.models import (
    Artwork,
    ArtworkThumbnail,
    Collection,
    Keyword,
)
from spirsa.mixins import AutoSlugAdminMixin
from spirsa.utils import get_preview_image


class ArtworkThumbnailInline(SortableInlineAdminMixin, admin.TabularInline):
    model = ArtworkThumbnail
    fields = (
        "ordering",
        "title",
        "image",
        "artwork",
        "published",
        "image_preview_thumb",
    )
    readonly_fields = ("image_preview_thumb",)

    def image_preview_thumb(self, obj):
        return get_preview_image(obj.image, 100)


class CollectionAdmin(SortableAdminMixin, AutoSlugAdminMixin):
    search_fields = (
        "title",
        "slug",
    )
    list_display = (
        "title",
        "slug",
        "show_in_navigation",
    )
    fields = (
        "title",
        "slug",
        "artworks",
        "show_in_navigation",
    )
    list_editable = ("show_in_navigation",)


class ArtworkAdmin(SortableAdminMixin, AutoSlugAdminMixin):
    search_fields = (
        "title",
        "slug",
    )
    list_display = (
        "title",
        "slug",
        "published",
        "created_at",
        "image_preview_thumb",
    )
    list_editable = ("published",)
    fields = (
        "title",
        "slug",
        "published",
        "short_description",
        "image",
        "image_preview",
        "keywords",
    )
    autocomplete_fields = ("keywords",)
    readonly_fields = ("image_preview",)
    inlines = [
        ArtworkThumbnailInline,
    ]

    def image_preview(self, obj):
        return get_preview_image(obj.image, 500)

    def image_preview_thumb(self, obj):
        return get_preview_image(obj.image, 100)


class ArtworkThumbnailAdmin(SortableAdminMixin, admin.ModelAdmin):
    search_fields = (
        "title",
        "artwork__title",
        "artwork__slug",
    )
    list_display = (
        "artwork",
        "published",
        "created_at",
        "image_preview_thumb",
    )
    list_editable = ("published",)
    fields = (
        "title",
        "image",
        "artwork",
        "published",
        "image_preview",
    )
    autocomplete_fields = ("artwork",)
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        return get_preview_image(obj.image, 500)

    def image_preview_thumb(self, obj):
        return get_preview_image(obj.image, 100)


class KeywordAdmin(AutoSlugAdminMixin):
    search_fields = (
        "name",
        "slug",
    )
    list_display_links = ("__str__",)
    list_display = (
        "__str__",
        "published",
        "name",
        "slug",
    )
    list_editable = (
        "published",
        "name",
        "slug",
    )
    fields = (
        "name",
        "published",
        "slug",
    )


admin.site.register(ArtworkThumbnail, ArtworkThumbnailAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(Keyword, KeywordAdmin)
