from copy import deepcopy
from django.utils.translation import ugettext_lazy as _

from django.contrib import admin

from .models import LeafPage, TeacherGuidePage, MediaArtefact, Topic

from mezzanine.core.admin import DisplayableAdmin, TabularDynamicInlineAdmin

page_fieldsets = (
        (None, {
            "fields": ["parent","title", "status"],
        }),
        (_("Meta data"), {
            "fields": ["keywords"],
            "classes": ("collapse-open",)
        }),
    )

class LeafPageAdmin(DisplayableAdmin):
    """
    Admin class for the ``LeafPage`` model and all subclasses of
    ``LeafPage``.
    """

    fieldsets = page_fieldsets

    def __init__(self, *args, **kwargs):
        """
        For ``LeafPage`` subclasses that are registered with an Admin class
        that doesn't implement fieldsets, add any extra model fields
        to this instance's fieldsets. This mimics Django's behaviour of
        adding all model fields when no fieldsets are defined on the
        Admin class.
        """
        super(LeafPageAdmin, self).__init__(*args, **kwargs)
        # Test that the fieldsets don't differ from PageAdmin's.
        if self.model is not LeafPage and self.fieldsets == LeafPageAdmin.fieldsets:
            # Make a copy so that we aren't modifying other Admin
            # classes' fieldsets.
            self.fieldsets = deepcopy(self.fieldsets)
            # Insert each field between the publishing fields and nav
            # fields. Do so in reverse order to retain the order of
            # the model's fields.
            for field in reversed(self.model._meta.fields):
                if field not in LeafPage._meta.fields and field.name != "leafpage_ptr":
                    self.fieldsets[0][1]["fields"].insert(3, field.name)

    def _check_permission(self, request, page, permission):
        """
        Runs the custom permission check and raises an
        exception if False.
        """
        if not getattr(page, "can_" + permission)(request):
            raise PermissionDenied

    def save_model(self, request, obj, form, change):
        """
        Set the ID of the parent page if passed in via querystring.
        """
        # Force parent to be saved to trigger handling of ordering and slugs.
        parent = request.GET.get("parent")
        if parent is not None and not change:
            obj.parent_id = parent
            obj.save()
        super(LeafPageAdmin, self).save_model(request, obj, form, change)

    def _maintain_parent(self, request, response):
        """
        Maintain the parent ID in the querystring for response_add and
        response_change.
        """
        location = response._headers.get("location")
        parent = request.GET.get("parent")
        if parent and location and "?" not in location[1]:
            url = "%s?parent=%s" % (location[1], parent)
            return HttpResponseRedirect(url)
        return response

    def response_add(self, request, obj):
        """
        Enforce page permissions and maintain the parent ID in the
        querystring.
        """
        response = super(LeafPageAdmin, self).response_add(request, obj)
        return self._maintain_parent(request, response)

    def response_change(self, request, obj):
        """
        Enforce page permissions and maintain the parent ID in the
        querystring.
        """
        response = super(LeafPage, self).response_change(request, obj)
        return self._maintain_parent(request, response)


# Drop the meta data fields, and move slug towards the stop.
link_fieldsets = deepcopy(page_fieldsets[:1])
link_fieldsets[0][1]["fields"] = link_fieldsets[0][1]["fields"][:-1]
link_fieldsets[0][1]["fields"].insert(1, "slug")

class TopicAdmin(admin.ModelAdmin):
    fields = ('title', 'icon')

admin.site.register(Topic, TopicAdmin)
admin.site.register(TeacherGuidePage, LeafPageAdmin)
admin.site.register(MediaArtefact,LeafPageAdmin)