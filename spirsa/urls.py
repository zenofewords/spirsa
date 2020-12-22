from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from spirsa.views import (
    AboutContactView,
    BadRequestView,
    DeniedView,
    NotFoundView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('art.urls', 'art'), namespace='art')),
    path('about-contact/', AboutContactView.as_view(), name='about-contact'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_url = '/preview/'
admin.site.enable_nav_sidebar = False

handler400 = BadRequestView.as_view()
handler403 = DeniedView.as_view()
handler404 = NotFoundView.as_view()

if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

if settings.DEBUG:
    urlpatterns = [
        path('404', handler404),
    ] + urlpatterns
