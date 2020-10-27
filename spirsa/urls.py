from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.decorators.cache import cache_page
from django.urls import path

from spirsa.constants import CACHE_SECONDS
from spirsa.views import (
    AboutContactView,
    BadRequestView,
    DeniedView,
    NotFoundView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('art.urls', 'art'), namespace='art')),
    path(
        'about-contact/',
        cache_page(CACHE_SECONDS)(AboutContactView.as_view()),
        name='about-contact'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
admin.site.enable_nav_sidebar = False

handler400 = BadRequestView.as_view()
handler403 = DeniedView.as_view()
handler404 = NotFoundView.as_view()

if settings.DEBUG_TOOLBAR:
    print('ajmo')
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
