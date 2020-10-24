from django.contrib import admin

from spirsa.models import (
    AbountContactInformation,
    MetaInformation,
)


class AbountContactInformationAdmin(admin.ModelAdmin):
    fields = (
        'image_title', 'image', 'top_section_title', 'top_section_text', 'contact_email',
        'bottom_section_title', 'bottom_section_text',
    )


admin.site.register(AbountContactInformation, AbountContactInformationAdmin)
admin.site.register(MetaInformation)
