from django.urls import reverse
from django.views.generic import TemplateView

from spirsa.constants import SMALL_WIDTH
from spirsa.mixins import MetaViewMixin
from spirsa.models import AbountContactInformation


class BaseView(MetaViewMixin):
    template_name = 'spirsa/base.html'


class AboutContactView(MetaViewMixin, TemplateView):
    template_name = 'spirsa/about_contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = AbountContactInformation.objects.first()
        context.update({
            'meta_title': 'About / Contact',
            'meta_url': reverse('about-contact'),
            'meta_type': 'profile',
            'meta_description': obj.bottom_section_text,
            'about_contact_information': obj,
        })

        if obj.image:
            context.update({
                'meta_image': obj.image,
                'meta_image_title': obj.image_title,
                'meta_image_height': SMALL_WIDTH,
                'meta_image_width': SMALL_WIDTH,
            })
        if obj and obj.srcsets:
            context.update(**{key: ', '.join(srcsets) for key, srcsets in obj.srcsets.items()})
        return context


class NotFoundView(MetaViewMixin, TemplateView):
    template_name = 'errors/404.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'meta_title': 'Not found',
        })
        return context


class DeniedView(MetaViewMixin, TemplateView):
    template_name = 'errors/403.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'meta_title': 'Error',
        })
        return context


class BadRequestView(MetaViewMixin, TemplateView):
    template_name = 'errors/400.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'meta_title': 'Error',
        })
        return context
