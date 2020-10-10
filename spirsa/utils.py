import copy
import os

from pathlib import Path
from PIL import Image

from django.contrib.sites.shortcuts import get_current_site
from django.utils.safestring import mark_safe

from spirsa.constants import (
    DEFAULT_QUALITY,
    DEFAULT_SIZE,
    DEFAULT_TYPE,
    SRCSET_MAPPING,
    SRCSET_TYPES,
    VARIATION_SETS,
)


def create_image_variations(instance):
    timestamp = os.path.getmtime(instance.image.file.name)
    if instance.image_timestamp == timestamp:
        return

    path = instance.image.path
    with Image.open(path) as original:
        instance.srcsets = create_srcsets(path, instance.image.url, original)
        instance.image = get_new_path(instance.image.name, DEFAULT_SIZE, DEFAULT_TYPE)
        instance.image_timestamp = os.path.getmtime(instance.image.file.name)
        instance.save()
        # remove original image
        os.remove(path)


def get_new_height(image, new_width):
    ratio = image.width / image.height
    return int(new_width / ratio)


def get_new_path(path, width, extension):
    return path.replace(
        os.path.basename(path), '{}_{}.{}'.format(Path(path).stem, width, extension)
    )


def create_srcsets(path, relative_path, image):
    srcset_mapping = copy.deepcopy(SRCSET_MAPPING)

    for variation_set in VARIATION_SETS:
        new_width = variation_set[2]

        new_height = get_new_height(image, new_width)
        resized_image = image.resize((new_width, new_height), resample=Image.BICUBIC)

        for srcset_type in SRCSET_TYPES:
            update_srcset_mapping(
                srcset_mapping,
                relative_path,
                variation_set,
                *create_image(resized_image, path, new_width, srcset_type),
            )
    return srcset_mapping


def create_image(resized_image, path, new_width, extension):
    new_path = get_new_path(path, new_width, extension)
    resized_image.save(new_path, extension, quality=DEFAULT_QUALITY)

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
