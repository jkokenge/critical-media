from copy import deepcopy
from django.utils.translation import ugettext_lazy as _

from django.contrib import admin

from .models import MediaArtefact, Topic, Tag

from mezzanine.core.admin import DisplayableAdmin


class MediaAdmin(DisplayableAdmin):
    fieldsets = (
                 (None, {
                         "fields": ["title", "status","thumbnail","content","tags"],
                          }),
                 )


class TopicAdmin(DisplayableAdmin):
    fieldsets = (
        (None, {
            "fields": ["parent_topic","title","icon", "content","featured_media"],
        }),
    )
    
class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Topic, TopicAdmin)
admin.site.register(MediaArtefact,MediaAdmin)
admin.site.register(Tag, TagAdmin)