from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from spirsa.views import BaseView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', BaseView.as_view(), name='base'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
admin.site.enable_nav_sidebar = False

if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
