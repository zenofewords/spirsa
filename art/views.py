from django.views.generic import DetailView

from art.models import Artwork
from spirsa.mixins import MetaViewMixin
from spirsa.utils import get_site_url


class ArtworkDetailView(DetailView):
    model = Artwork
    template_name = 'art/artwork_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'meta_url': get_site_url(self.request),
            'meta_title': self.object.title,
            'meta_description': self.object.short_description,
            'meta_keywords': ', '.join([k.name for k in self.object.keywords.all()]),
            'meta_image': self.object.image,
            'meta_image_title': self.object.title,
        })
        return context


class ArtworkListView(MetaViewMixin):
    template_name = 'art/artwork_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'artworks': Artwork.objects.digital().published(),
            'meta_title': 'Digital Art',
        })
        return context


class ArtworTraditionalkListView(MetaViewMixin):
    template_name = 'art/artwork_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'artworks': Artwork.objects.traditional().published(),
            'meta_title': 'Traditional Art',
        })
        return context
