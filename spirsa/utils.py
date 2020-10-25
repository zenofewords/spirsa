import copy
import math
import os

from pathlib import Path
from PIL import Image

from django.apps import apps
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from spirsa.constants import (
    BASE_HEIGHT,
    DEFAULT_QUALITY,
    DEFAULT_TYPE,
    HOME_URL_NAME,
    LANDSCAPE_VARIATION_SETS,
    RATIO_THRESHOLD,
    SRCSET_MAPPING,
    SRCSET_TYPES,
    VARIATION_SETS,
)


def create_image_variations(instance, DEFAULT_WIDTH, VARIATIONS=None):
    timestamp = round(os.path.getctime(instance.image.file.name))
    if instance.image_timestamp == timestamp:
        return

    path = instance.image.path
    with Image.open(path) as original:
        instance.srcsets = create_srcsets(path, instance, original, VARIATIONS)
        instance.image = get_new_path(instance.image.name, DEFAULT_WIDTH, DEFAULT_TYPE)
        instance.image_timestamp = round(os.path.getctime(instance.image.file.name))
        instance.save()
        # remove original image
        os.remove(path)


def get_new_path(path, width, extension):
    return path.replace(
        os.path.basename(path), '{}_{}.{}'.format(Path(path).stem, width, extension)
    )


def create_srcsets(path, instance, image, VARIATIONS):
    srcset_mapping = copy.deepcopy(SRCSET_MAPPING)
    ratio = image.width / image.height
    if not VARIATIONS:
        VARIATIONS = LANDSCAPE_VARIATION_SETS if ratio > RATIO_THRESHOLD else VARIATION_SETS
        set_cls_dimension(instance.cls_dimension, ratio, VARIATIONS[1][1])

    for variation_set in VARIATIONS:
        new_width = variation_set[2]

        if 0.99 < ratio < 1.01:
            new_image = image
        else:
            new_height = int(new_width / ratio)
            new_image = image.resize((new_width, new_height), resample=Image.BICUBIC)

        for srcset_type in SRCSET_TYPES:
            update_srcset_mapping(
                srcset_mapping,
                instance.image.url,
                variation_set,
                *create_image(new_image, path, new_width, srcset_type),
            )
    return srcset_mapping


def set_cls_dimension(cls_dimension, ratio, detail_width):
    cls_dimension.list_height = BASE_HEIGHT
    cls_dimension.list_width = math.ceil(BASE_HEIGHT * ratio)
    cls_dimension.detail_height = detail_width / ratio
    cls_dimension.detail_width = detail_width
    cls_dimension.save()


def create_image(resized_image, path, new_width, extension):
    new_path = get_new_path(path, new_width, extension)
    resized_image.save(new_path, extension, method=6, quality=DEFAULT_QUALITY)

    return new_width, extension


def update_srcset_mapping(srcset_mapping, relative_path, variation_set, width, extension):
    srcset_mapping['{}_{}'.format(extension, variation_set[0])].append(
        '{} {}x'.format(
            get_new_path(relative_path, width, extension),
            width // variation_set[1]
        )
    )


def get_preview_image(image, max_width):
    try:
        if not image:
            return ''

        original_width = image.width
        original_height = image.height

        width = original_width if original_width < max_width else max_width
        slot_ratio = original_width / width
        height = original_height / slot_ratio

        return mark_safe(
            '<img src={url} width={width} height={height} />'.format(
                url=image.url,
                width=width,
                height=height,
            )
        )
    except FileNotFoundError:  # noqa
        return ''


def get_site_url(request):
    return '{}://{}'.format(request.scheme, get_current_site(request))


def get_artwork_navigation_urls(data, obj):
    home = reverse_lazy('art:{}'.format(HOME_URL_NAME))
    data.update({
        'back_url': reverse_lazy('art:traditional') if obj.is_traditional else home
    })

    Artwork = apps.get_model('art.Artwork')
    next_artwork = Artwork.objects.filter(
        is_traditional=obj.is_traditional,
        ordering__lte=obj.ordering, created_at__lte=obj.created_at
    ).exclude(id=obj.pk).first()

    previous = Artwork.objects.filter(
        is_traditional=obj.is_traditional,
        ordering__gte=obj.ordering, created_at__gte=obj.created_at
    ).exclude(id=obj.pk).last()

    if next_artwork:
        data.update({
            'next_url': reverse_lazy('art:artwork-detail', kwargs={'slug': next_artwork.slug})
        })
    if previous:
        data.update({
            'previous_url': reverse_lazy('art:artwork-detail', kwargs={'slug': previous.slug})
        })
    return data
