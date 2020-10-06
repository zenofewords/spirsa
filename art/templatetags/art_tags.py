from django import template
from django.urls import reverse_lazy

from spirsa.constants import HOME_URL_NAME
from spirsa.utils import get_site_url

register = template.Library()


@register.inclusion_tag('art/tags/artwork_tag.html', takes_context=True)
def artwork_tag(context, obj, detail=False):
    request = context.get('request')
    site_url = get_site_url(request)
    fb_share_url = 'https://www.facebook.com/sharer.php?u='
    tt_share_url = 'https://twitter.com/intent/tweet?url='
    li_share_url = 'https://www.linkedin.com/sharing/share-offsite/?url='
    pt_share_url = 'https://pinterest.com/pin/create/button/?url='

    data = {
        'artwork': obj,
        'facebook_share_url': '{}{}/artwork/{}'.format(fb_share_url, site_url, obj.slug),
        'twitter_share_url': '{}{}/artwork/{}'.format(tt_share_url, site_url, obj.slug),
        'linkedin_share_url': '{}{}/artwork/{}'.format(li_share_url, site_url, obj.slug),
        'pinterest_share_url': '{}{}/artwork/{}'.format(pt_share_url, site_url, obj.slug),
        'detail': detail,
    }
    if obj.srcsets:
        data.update(**{key: ', '.join(srcsets) for key, srcsets in obj.srcsets.items()})
    return data


@register.inclusion_tag('art/tags/artwork_breadcrumb.html')
def artwork_breadcrumb(obj):
    if obj.is_traditional:
        base_url = reverse_lazy('art:traditional')
        label = 'Traditional art'
    else:
        base_url = reverse_lazy('art:{}'.format(HOME_URL_NAME))
        label = 'Digital art'

    return {
        'artwork_title': obj.title,
        'base_url': base_url,
        'label': label,
    }
