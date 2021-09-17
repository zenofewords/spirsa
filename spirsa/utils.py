import copy
import math
import os
import re

from pathlib import Path
from PIL import Image

from django.apps import apps
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils import timezone, dateformat

from spirsa.constants import (
    BASE_HEIGHT,
    DEFAULT_TYPE,
    HOME_URL_NAME,
    LANDSCAPE_VARIATION_SETS,
    MEDIUM_WIDTH,
    RATIO_THRESHOLD,
    SRCSET_MAPPING,
    SRCSET_TYPES,
    VARIATION_SETS,
)


def create_image_variations(instance, default_width=MEDIUM_WIDTH, variations=None):
    timestamp = round(os.path.getctime(instance.image.file.name))
    if instance.image_timestamp == timestamp:
        return

    path = instance.image.path
    with Image.open(path) as original:
        instance.srcsets = create_srcsets(path, instance, original, variations)
        instance.image = get_new_path(instance.image.name, default_width, DEFAULT_TYPE)
        instance.image_timestamp = round(os.path.getctime(instance.image.file.name))
        instance.save()
        # remove original image
        os.remove(path)


def get_new_path(path, width, extension):
    return path.replace(
        os.path.basename(path), '{}_{}.{}'.format(Path(path).stem, width, extension)
    )


def create_srcsets(path, instance, image, variations):
    srcset_mapping = copy.deepcopy(SRCSET_MAPPING)
    ratio = image.width / image.height

    if not variations:
        variations = LANDSCAPE_VARIATION_SETS if ratio > RATIO_THRESHOLD else VARIATION_SETS
    set_cls_dimension(instance.cls_dimension, ratio, variations[1][1])

    for variation_set in variations:
        new_width = variation_set[2]

        if ratio != 1 or image.width != new_width:
            new_height = int(new_width / ratio)
            image = image.resize((new_width, new_height), resample=Image.LANCZOS)

        for srcset_type in SRCSET_TYPES:
            update_srcset_mapping(
                srcset_mapping,
                instance.image.url,
                variation_set,
                *create_image(image, path, new_width, srcset_type),
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

    if extension == DEFAULT_TYPE:
        # jpeg does not support transparency
        resized_image = resized_image.convert('RGB')
    resized_image.save(new_path, extension, method=6)

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
    artwork_ids = Artwork.objects.published().filter(
        is_traditional=obj.is_traditional
    ).values_list('pk', flat=True)

    try:
        artwork_index = list(artwork_ids).index(obj.pk)
    except ValueError:
        artwork_index = -1

    next_artwork_id = 0
    if artwork_index >= 0 and artwork_index < len(artwork_ids) - 1:
        next_artwork_id = artwork_ids[artwork_index + 1]
    next_artwork = Artwork.objects.filter(pk=next_artwork_id).first()

    previous_artwork_id = 0
    if artwork_index - 1 >= 0:
        previous_artwork_id = artwork_ids[artwork_index - 1]
    previous_artwork = Artwork.objects.filter(pk=previous_artwork_id).first()

    if next_artwork:
        data.update({
            'next_url': reverse_lazy('art:artwork-detail', kwargs={'slug': next_artwork.slug})
        })
    if previous_artwork:
        data.update({
            'previous_url': reverse_lazy(
                'art:artwork-detail', kwargs={'slug': previous_artwork.slug}
            )
        })
    return data


def get_full_size_image(srcsets):
    full_size_image = srcsets.get('jpeg_large')
    if not full_size_image:
        full_size_image = srcsets.get('jpeg_medium')

    return {'full_size_image': full_size_image[1][:-3] if full_size_image else None}


def get_upload_path(filename):
    name, dot, extension = filename.rpartition('.')

    return '{}/{}/{}_{}'.format(
        timezone.now().year,
        timezone.now().month,
        slugify(name),
        dateformat.format(timezone.now(), 'His')
    )


def get_artwork_image_path(instance, filename):
    return 'artwork/{}'.format(get_upload_path(filename))


def get_artwork_thumbnail_path(instance, filename):
    return 'artwork/thumbnail/{}'.format(get_upload_path(filename))


def get_contact_image_path(instance, filename):
    return 'spirsa/{}'.format(get_upload_path(filename))


def clean_meta_description(text):
    return re.sub(re.compile('<.*?>'), '', text)