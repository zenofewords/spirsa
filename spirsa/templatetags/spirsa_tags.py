from django import template

from spirsa.constants import HOME_URL_NAME

register = template.Library()


@register.inclusion_tag('spirsa/tags/menu_link_tag.html')
def menu_link_tag(name, path, base=''):
    return {
        'name': name,
        'reverse_url': '{}:{}'.format(base, name) if base else name,
        'current': name in path or name == HOME_URL_NAME and '/' == path,
    }
