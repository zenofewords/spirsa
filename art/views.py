from django.views.generic import (
    DetailView,
    TemplateView,
)

from art.models import Artwork
from spirsa.mixins import MetaViewMixin


class ArtworkDetailView(MetaViewMixin, DetailView):
    model = Artwork
    template_name = 'art/artwork_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'meta_title': self.object.title,
            'meta_image': self.object.image if self.object.image else None,
            'meta_image_title': self.object.title,
        })
        if self.object.short_description:
            context.update({
                'meta_description': self.object.short_description,
            })
        if self.object.keywords.exists():
            context.update({
                'meta_keywords': ', '.join([k.name for k in self.object.keywords.all()]),
            })
        return context


class ArtworkListView(MetaViewMixin, TemplateView):
    template_name = 'art/artwork_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'artworks': Artwork.objects.digital().published(),
            'meta_title': 'Digital Art',
        })
        return context


class ArtworTraditionalkListView(MetaViewMixin, TemplateView):
    template_name = 'art/artwork_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'artworks': Artwork.objects.traditional().published(),
            'meta_title': 'Traditional Art',
        })
        return context
