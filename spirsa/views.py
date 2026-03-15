from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import TemplateView, View

from spirsa.constants import SMALL_WIDTH
from spirsa.mixins import MetaViewMixin
from spirsa.models import AboutContactInformation


class RobotsTxtView(View):
    def get(self, request):
        lines = [
            "User-agent: *",
            "Allow: /",
        ]
        return HttpResponse("\n".join(lines), content_type="text/plain")


class BaseView(MetaViewMixin):
    template_name = "spirsa/base.html"


class AboutContactView(MetaViewMixin, TemplateView):
    template_name = "spirsa/about_contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = AboutContactInformation.objects.first()
        context.update(
            {
                "meta_title": "About / Contact",
                "meta_url": reverse("about-contact"),
                "meta_type": "profile",
                "meta_description": obj.bottom_section_text,
                "about_contact_information": obj,
            }
        )

        if obj.image:
            context.update(
                {
                    "meta_image": obj.image,
                    "meta_image_title": obj.title,
                    "meta_image_height": SMALL_WIDTH,
                    "meta_image_width": SMALL_WIDTH,
                }
            )
        if obj and obj.srcsets:
            context.update(**{key: ", ".join(srcsets) for key, srcsets in obj.srcsets.items()})
        return context


class ErrorView(MetaViewMixin, TemplateView):
    error_status = 500

    def render_to_response(self, context, **response_kwargs):
        response_kwargs["status"] = self.error_status
        return super().render_to_response(context, **response_kwargs)


class NotFoundView(ErrorView):
    template_name = "errors/404.html"
    error_status = 404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "meta_title": "Not found",
            }
        )
        return context


class DeniedView(ErrorView):
    template_name = "errors/403.html"
    error_status = 403

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "meta_title": "Error",
            }
        )
        return context


class BadRequestView(ErrorView):
    template_name = "errors/400.html"
    error_status = 400

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "meta_title": "Error",
            }
        )
        return context
