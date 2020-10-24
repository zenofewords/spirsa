from django.views.generic import TemplateView

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
            'about_contact_information': obj,
        })

        if obj and obj.srcsets:
            context.update(**{key: ', '.join(srcsets) for key, srcsets in obj.srcsets.items()})
        return context
