from django.views.generic import DetailView

from spirsa.mixins import MetaViewMixin
from art.models import Artwork


class ArtworkDetailView(DetailView):
    model = Artwork
    template_name = 'art/artwork_detail.html'


class ArtworkListView(MetaViewMixin):
    template_name = 'art/artwork_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'artworks': Artwork.objects.digital().published(),
        })
        return context


class ArtworTraditionalkListView(MetaViewMixin):
    template_name = 'art/artwork_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'artworks': Artwork.objects.traditional().published(),
        })
        return context
