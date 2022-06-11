from django import template
from django.urls import reverse

from spirsa.constants import HOME_URL_NAME

register = template.Library()


@register.inclusion_tag('spirsa/tags/menu_link_tag.html')
def menu_link_tag(name, path, dynamic=False):
    url = name.replace('/', '-')
    return {
        'name': name,
        'url': reverse(url) if dynamic else '/{}'.format(url),
        'current': url in path,
    }
