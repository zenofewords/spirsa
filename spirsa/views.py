from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import TemplateView


class MetaMixin(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = {
            'meta_url': '{}://{}'.format(self.request.scheme, get_current_site(self.request)),
            'meta_title': '',
            'meta_description': '',
            'meta_image_alt': '',
        }
        context.update(data)
        return context


class BaseView(MetaMixin):
    template_name = 'spirsa/base.html'
