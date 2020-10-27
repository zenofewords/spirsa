from django import template

from spirsa.constants import HOME_URL_NAME

register = template.Library()


@register.inclusion_tag('spirsa/tags/menu_link_tag.html')
def menu_link_tag(name, path, base='', detail_type=None):
    detail = name == detail_type

    url = name.replace('/', '-')
    return {
        'name': name,
        'reverse_url': '{}:{}'.format(base, url) if base else url,
        'current': url in path or detail or url == HOME_URL_NAME and '/' == path,
    }
