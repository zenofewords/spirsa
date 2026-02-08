from django.contrib import admin

from spirsa.models import (
    AboutContactInformation,
    MetaInformation,
)


class AboutContactInformationAdmin(admin.ModelAdmin):
    fields = (
        "title",
        "image",
        "top_section_title",
        "top_section_text",
        "contact_email",
        "bottom_section_title",
        "bottom_section_text",
    )


admin.site.register(AboutContactInformation, AboutContactInformationAdmin)
admin.site.register(MetaInformation)
