from copy import deepcopy
from django.utils.translation import ugettext_lazy as _

from django.contrib import admin

from .models import MediaArtefact, Topic

from mezzanine.core.admin import DisplayableAdmin

media_fieldsets = (
        (None, {
            "fields": ["title", "status"],
        }),
        (_("Meta data"), {
            "fields": ["keywords"],
            "classes": ("collapse-open",)
        }),
    )

class MediaAdmin(DisplayableAdmin):
    fieldsets = (
                 (None, {
                         "fields": ["title", "status"],
                          }),
                 (_("Meta data"), {
                                    "fields": ["keywords"],
                                    "classes": ("collapse-open",)
                                    }),
                 )


class TopicAdmin(DisplayableAdmin):
    fieldsets = (
        (None, {
            "fields": ["parent_topic","title","icon", "content","featured_media"],
        }),
    )


admin.site.register(Topic, TopicAdmin)
admin.site.register(MediaArtefact,MediaAdmin)