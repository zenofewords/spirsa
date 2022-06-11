import math

from django.views.generic import (
    DetailView,
    ListView,
)
from django.utils.text import slugify

from art.models import (
    Artwork,
)
from spirsa.mixins import (
    MetaViewMixin,
)
from spirsa.utils import clean_meta_description, show_preview


class ArtworkDetailView(MetaViewMixin, DetailView):
    queryset = Artwork.objects.published()
    template_name = 'art/artwork_detail.html'

    def get_object(self):
        self.slug = self.kwargs.get('slug')
        self.artwork_slug = self.kwargs.get('artwork_slug')

        if show_preview(self.request):
            return Artwork.objects.get(slug=self.artwork_slug)
        return Artwork.objects.published().get(slug=self.artwork_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'meta_title': '{} | {}'.format(self.slug.title(), self.object.title),
            'meta_url': self.object.get_absolute_url(self.slug),
            'meta_type': 'article',
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
    meta_title = 'Featured'
    paginate_by = 6
    queryset = Artwork.objects.featured()
    template_name = 'art/artwork_list.html'

    def get_queryset(self):
        self.path = slugify(self.request.GET.get('path') or self.request.path)
        if self.path:
            self.queryset = Artwork.objects.filter(collection__slug=self.path)

        if show_preview(self.request):
            return self.queryset
        return self.queryset.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'meta_title': self.path.title() or self.meta_title,
            'page_count': math.ceil(self.queryset.count() / self.paginate_by),
        })
        return context


class AsyncArtworkListView(ArtworkListView):
    template_name = 'art/includes/artworks.html'
