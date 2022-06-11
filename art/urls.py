from django.urls import path

from art.views import (
    AsyncArtworkListView,
    ArtworkDetailView,
    ArtworkListView,
)
from spirsa.constants import (
    HOME_URL_NAME,
)


urlpatterns = [
    path('async-artworks', AsyncArtworkListView.as_view(), name='async-artwork-list'),
    path('', ArtworkListView.as_view(), name=HOME_URL_NAME),
    path('<slug:slug>', ArtworkListView.as_view(), name='artwork-list'),
    path('<slug:slug>/<slug:artwork_slug>', ArtworkDetailView.as_view(), name='artwork-detail'),
]
