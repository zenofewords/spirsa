import re
import tempfile
import uuid
from pathlib import Path

from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.html import format_html

from art.models import (
    Artwork,
    ArtworkThumbnail,
    Collection,
    Keyword,
)
from spirsa.mixins import AutoSlugAdminMixin
from spirsa.utils import get_preview_image

UPLOAD_CACHE_DIR = Path(tempfile.gettempdir()) / "django_upload_cache"


def _is_valid_cache_key(key):
    return bool(re.match(r"^[0-9a-f]{32}$", key))


class CachedFileInput(AdminFileWidget):
    def value_from_datadict(self, data, files, name):
        upload = files.get(name)
        cache_key = data.get(f"_cached_{name}", "")

        if upload:
            key = uuid.uuid4().hex
            cache_dir = UPLOAD_CACHE_DIR / key
            cache_dir.mkdir(parents=True, exist_ok=True)
            with open(cache_dir / upload.name, "wb") as f:
                for chunk in upload.chunks():
                    f.write(chunk)
            upload.seek(0)
            self._cache_key = key
            self._cache_name = upload.name
        elif cache_key and _is_valid_cache_key(cache_key):
            cache_dir = UPLOAD_CACHE_DIR / cache_key
            if cache_dir.exists():
                for cached_file in cache_dir.iterdir():
                    with open(cached_file, "rb") as f:
                        files[name] = SimpleUploadedFile(
                            cached_file.name, f.read(), content_type="image/*"
                        )
                    self._cache_name = cached_file.name
                    break
            self._cache_key = cache_key
        else:
            self._cache_key = ""
            self._cache_name = ""

        return super().value_from_datadict(data, files, name)

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer=renderer)
        cache_key = getattr(self, "_cache_key", "")
        cache_name = getattr(self, "_cache_name", "")
        if cache_key:
            hidden = format_html(
                '<input type="hidden" name="_cached_{}" value="{}">',
                name,
                cache_key,
            )
            if cache_name:
                info = format_html(
                    '<p class="file-upload">Previously uploaded: {}</p>',
                    cache_name,
                )
                return info + html + hidden
            return html + hidden
        return html


class ArtworkForm(forms.ModelForm):
    collections = forms.ModelMultipleChoiceField(
        queryset=Collection.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Artwork
        fields = "__all__"
        widgets = {"image": CachedFileInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["collections"].initial = self.instance.collection_set.all()

    def _set_collections(self, instance):
        instance.collection_set.set(self.cleaned_data["collections"])

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        if instance.pk:
            self._set_collections(instance)
        else:
            old_save_m2m = self.save_m2m

            def save_m2m():
                old_save_m2m()
                self._set_collections(instance)

            self.save_m2m = save_m2m
        return instance


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
    form = ArtworkForm
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
        "collections",
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
