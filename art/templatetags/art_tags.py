from django import template

register = template.Library()


@register.inclusion_tag('art/tags/artwork_tag.html')
def artwork_tag(obj):
    return {
        'artwork': obj,
        **{key: ', '.join(srcsets) for key, srcsets in obj.srcsets.items()},
    }
