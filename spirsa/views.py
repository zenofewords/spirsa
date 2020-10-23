from spirsa.mixins import MetaViewMixin


class BaseView(MetaViewMixin):
    template_name = 'spirsa/base.html'


class AboutContactView(MetaViewMixin):
    template_name = 'spirsa/about_contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'meta_title': 'About / Contact',
        })
        return context
