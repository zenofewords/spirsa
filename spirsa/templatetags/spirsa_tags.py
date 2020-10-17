from django import template

from art.models import Artwork
from spirsa.constants import HOME_URL_NAME

register = template.Library()


@register.inclusion_tag('spirsa/tags/menu_link_tag.html')
def menu_link_tag(name, path, base=''):
    split_path = list(filter(None, path.split('/')))
    detail = None

    if len(split_path) > 1:
        artwork = Artwork.objects.filter(slug=split_path.pop()).first()

        if artwork and name == 'digital':
            detail = not artwork.is_traditional
        if artwork and name == 'traditional':
            detail = artwork.is_traditional

    return {
        'name': name,
        'reverse_url': '{}:{}'.format(base, name) if base else name,
        'current': name in path or detail or name == HOME_URL_NAME and '/' == path,
    }
