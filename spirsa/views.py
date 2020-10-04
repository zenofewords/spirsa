from spirsa.mixins import MetaViewMixin


class BaseView(MetaViewMixin):
    template_name = 'spirsa/base.html'


class ContactView(MetaViewMixin):
    template_name = 'spirsa/contact.html'
