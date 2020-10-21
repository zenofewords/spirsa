from django import template

from spirsa.constants import (
    FB_SHARE_URL,
    TT_SHARE_URL,
    IN_SHARE_URL,
    PT_SHARE_URL,
)
from spirsa.utils import get_site_url

register = template.Library()


@register.inclusion_tag('art/tags/artwork_tag.html', takes_context=True)
def artwork_tag(context, obj, decoding='async', detail=False):
    request = context.get('request')
    site_url = get_site_url(request)

    data = {
        'artwork': obj,
        'facebook_share_url': '{}{}/artwork/{}'.format(FB_SHARE_URL, site_url, obj.slug),
        'twitter_share_url': '{}{}/artwork/{}'.format(TT_SHARE_URL, site_url, obj.slug),
        'linkedin_share_url': '{}{}/artwork/{}'.format(IN_SHARE_URL, site_url, obj.slug),
        'pinterest_share_url': '{}{}/artwork/{}'.format(PT_SHARE_URL, site_url, obj.slug),
        'decoding': decoding,
        'detail': detail,
    }
    if obj.srcsets:
        data.update(**{key: ', '.join(srcsets) for key, srcsets in obj.srcsets.items()})
    return data
