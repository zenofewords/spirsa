import math

from django.views.generic import (
    DetailView,
    ListView,
)

from art.models import Artwork
from spirsa.mixins import (
    MetaViewMixin,
    StaffPreViewMixin,
)
from spirsa.utils import clean_meta_description


class ArtworkDetailView(MetaViewMixin, DetailView):
    queryset = Artwork.objects.published()
    template_name = 'art/artwork_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        detail_type = 'Traditional' if self.object.is_traditional else 'Digital'
        meta_title = '{} | {}'.format(detail_type, self.object.title)

        context.update({
            'meta_title': meta_title if self.object.is_traditional else self.object.title,
            'meta_url': self.object.get_absolute_url(),
            'meta_type': 'article',
            'detail_type': detail_type,
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
                'meta_description': clean_meta_description(self.object.short_description),
            })
        if self.object.keywords.exists():
            context.update({
                'meta_keywords': ', '.join([k.name for k in self.object.keywords.all()]),
            })
        return context


class ArtworkListView(MetaViewMixin, ListView):
    context_object_name = 'artworks'
    meta_title = 'Digital'
    paginate_by = 6
    queryset = Artwork.objects.digital().published()
    template_name = 'art/artwork_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'meta_title': self.meta_title,
            'page_count': math.ceil(self.queryset.count() / self.paginate_by),
        })
        return context


class ArtworkTraditionalListView(ArtworkListView):
    meta_title = 'Traditional'
    queryset = Artwork.objects.traditional().published()


class ArtworkListPreView(StaffPreViewMixin, ArtworkListView):
    queryset = Artwork.objects.digital().all()


class ArtworkTraditionalListPreView(StaffPreViewMixin, ArtworkTraditionalListView):
    queryset = Artwork.objects.traditional().all()


class ArtworkDetailPreView(StaffPreViewMixin, ArtworkDetailView):
    queryset = Artwork.objects.all()


class AsyncArtworkListView(ArtworkListView):
    template_name = 'art/includes/artworks.html'


class AsyncArtworkTraditionalListView(ArtworkTraditionalListView):
    template_name = 'art/includes/artworks.html'