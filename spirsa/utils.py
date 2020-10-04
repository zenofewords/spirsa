import copy
import os

from pathlib import Path
from PIL import Image

from django.contrib.sites.shortcuts import get_current_site
from django.utils.safestring import mark_safe

from spirsa.constants import (
    IMAGE_BREAKPOINT_WIDTH,
    IMAGE_MAX_WIDTH,
    IMAGE_MIN_WIDTH,
    IMAGE_QUALITY,
    IMAGE_VARIATION_WIDTHS,
    SRCSET_MAPPING,
)


def create_image_variations(instance):
    timestamp = os.path.getmtime(instance.image.file.name)
    if instance.image_timestamp == timestamp:
        return

    path = instance.image.path
    with Image.open(path) as original:
        # adjust width/height
        if original.width > IMAGE_MAX_WIDTH:
            new_height = get_new_height(original, IMAGE_MAX_WIDTH)
            original = original.resize((IMAGE_MAX_WIDTH, new_height), resample=Image.BICUBIC)

        instance.srcsets = create_srcsets(path, instance.image.url, original)
        instance.image = get_new_path(instance.image.name, '800', 'jpeg')
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

    for new_width in IMAGE_VARIATION_WIDTHS:
        new_height = get_new_height(image, new_width)
        resized_image = image.resize((new_width, new_height), resample=Image.BICUBIC)
        # create jpg variation
        update_srcset_mapping(
            srcset_mapping,
            relative_path,
            *create_image(resized_image, path, new_width, 'jpeg', {'optimize': True}),
        )
        # create webp variation
        update_srcset_mapping(
            srcset_mapping,
            relative_path,
            *create_image(resized_image, path, new_width, 'webp', {'method': 3}),
        )
    return srcset_mapping


def create_image(resized_image, path, new_width, extension, kwarg):
    new_path = get_new_path(path, new_width, extension)
    resized_image.save(new_path, extension, **kwarg, quality=IMAGE_QUALITY)

    return new_width, extension


def update_srcset_mapping(srcset_mapping, relative_path, width, extension):
    if width < IMAGE_BREAKPOINT_WIDTH:
        srcset_mapping['{}_{}'.format(extension, 'mobile')].append(
            '{} {}x'.format(
                get_new_path(relative_path, width, extension),
                width // IMAGE_MIN_WIDTH
            )
        )
    if width >= IMAGE_BREAKPOINT_WIDTH:
        srcset_mapping['{}_{}'.format(extension, 'desktop')].append(
            '{} {}x'.format(
                get_new_path(relative_path, width, extension),
                width // IMAGE_BREAKPOINT_WIDTH
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
