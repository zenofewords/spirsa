from spirsa.mixins import MetaViewMixin


class BaseView(MetaViewMixin):
    template_name = 'spirsa/base.html'


class AboutContactView(MetaViewMixin):
    template_name = 'spirsa/about_contact.html'
