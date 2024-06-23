from django import template
from django.urls import reverse

from art.models import Collection

register = template.Library()


@register.inclusion_tag('spirsa/tags/menu_link_tag.html')
def menu_link_tag(name, path, dynamic=False):
    url = name.replace('/', '-')
    return {
        'name': name.replace('-', ' '),
        'url': reverse(url) if dynamic else '/{}'.format(url),
        'current': url in path,
    }


@register.inclusion_tag('spirsa/tags/navigation_tag.html', takes_context=True)
def navigation_tag(context, mobile=False):
    request = context.get('request')
    collections = Collection.objects.for_navigation()

    return {
        'mobile': mobile,
        'request_path': request.path,
        'navigation_slugs': [collection.slug for collection in collections]
    }
