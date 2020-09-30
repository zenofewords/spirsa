from django.contrib import admin

from art.models import Artwork
from spirsa.constants import IMAGE_MIN_WIDTH
from spirsa.mixins import AutoSlugAdminMixin
from spirsa.utils import get_preview_image


class ArtworkAdmin(AutoSlugAdminMixin):
    list_display = (
        'title', 'slug', 'image_preview_thumb', 'is_published', 'created_at',
    )
    list_editable = ('is_published', )
    fields = (
        'title', 'slug', 'is_published', 'short_description', 'image', 'image_preview',
    )
    readonly_fields = ('image_preview', )

    def image_preview(self, obj):
        return get_preview_image(obj.image, IMAGE_MIN_WIDTH)

    def image_preview_thumb(self, obj):
        return get_preview_image(obj.image, IMAGE_MIN_WIDTH // 4)


admin.site.register(Artwork, ArtworkAdmin)
