from django.views.generic import (
    DetailView,
    TemplateView,
)

from art.models import Artwork
from spirsa.mixins import MetaViewMixin


class ArtworkDetailView(MetaViewMixin, DetailView):
    queryset = Artwork.objects.published()
    template_name = 'art/artwork_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'meta_title': self.object.title,
            'meta_url': self.object.get_absolute_url(),
            'meta_type': 'article',
            'detail_type': 'traditional' if self.object.is_traditional else 'digital',
        })
        if self.object.image:
            context.update({
                'meta_image': self.object.image,
                'meta_image_title': self.object.title,
                'meta_image_height': self.object.cls_dimension.detail_height,
                'meta_image_width': self.object.cls_dimension.detail_width,
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
