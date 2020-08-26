from django import template

register = template.Library()


@register.inclusion_tag('spirsa/tags/external_link_tag.html')
def external_link_tag(url, title, terminator=''):
    return {
        'url': url,
        'title': title,
        'terminator': terminator,
    }
