from spirsa.mixins import MetaViewMixin
from art.models import Artwork


class ArtworkView(MetaViewMixin):
    template_name = 'art/artwork.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'artworks': Artwork.objects.published(),
        })
        return context
