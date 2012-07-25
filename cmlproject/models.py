from django.db import models
from django.core.urlresolvers import resolve, reverse

from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField

from mezzanine.core.models import Displayable, Orderable, RichText, Slugged
from mezzanine.utils.models import AdminThumbMixin

from mezzanine.utils.urls import admin_url, slugify


# The members of Page will be inherited by the Author model, such
# as title, slug, etc. For authors we can use the title field to
# store the author's name. For our model definition, we just add
# any extra fields that aren't part of the Page model, in this
# case, date of birth.


class Topic(Orderable, Slugged, AdminThumbMixin):
    
    icon = FileField(verbose_name=_("Icon"),
                               upload_to="thumbs", format="Image",
                               max_length=255, null=True, blank=True)
    
    admin_thumb_field = "icon"
    
    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        
    def __unicode__(self):
        return self.title
    
    def reset_slugs(self):
        """
        Called when the parent page is changed in the admin and the slug
        plus all child slugs need to be recreated given the new parent.
        """
        if not self.overridden():
            self.slug = None
            self.save()
        for child in self.children.all():
            child.reset_slugs()
    
class LeafPage(Orderable, Displayable):
    """
    A page belonging to a topic. No child pages.
    """
    parent = models.ForeignKey("Topic",verbose_name=_("Parent Topic"),related_name="children")
    titles = models.CharField(editable=False, max_length=1000, null=True)
    content_model = models.CharField(editable=False, max_length=50, null=True)

    class Meta:
        ordering = ("titles",)
        order_with_respect_to = "parent"

    def __unicode__(self):
        return self.titles

    def get_absolute_url(self):
        """
        URL for a page - for ``Link`` page types, simply return its
        slug since these don't have an actual URL pattern. Also handle
        the special case of the homepage being a page object.
        """
        slug = self.slug
        
        if slug == "/":
            return reverse("home")
        else:
            return reverse("page", kwargs={"slug": slug})

    def get_admin_url(self):
        return admin_url(self, "change", self.id)

    def save(self, *args, **kwargs):
        """
        Create the titles field using the titles up the parent chain
        and set the initial value for ordering.
        """
        if self.id is None:
            self.content_model = self._meta.object_name.lower()
        titles = [self.title]
        parent = self.parent
        if parent is not None:
            titles.insert(0, unicode(self._meta.verbose_name_plural))
            titles.insert(0, parent.title)

        self.titles = " / ".join(titles)
        super(LeafPage, self).save(*args, **kwargs)

    @classmethod
    def get_content_models(cls):
        """
        Return all LeafPage subclasses.
        """
        is_content_model = lambda m: m is not Page and issubclass(m, Page)
        return filter(is_content_model, models.get_models())

    def get_content_model(self):
        """
        Provies a generic method of retrieving the instance of the custom
        content type's model for this page.
        """
        return getattr(self, self.content_model, None)

    def get_slug(self):
        """
        Recursively build the slug from the chain of parents.
        """
        slug = slugify(self.title)
        if self.parent is not None:
            return "%s/%s" % (self.parent.slug, slug)
        return slug

    def reset_slugs(self):
        """
        Called when the parent page is changed in the admin and the slug
        plus all child slugs need to be recreated given the new parent.
        """
        if not self.overridden():
            self.slug = None
            self.save()
        for child in self.children.all():
            child.reset_slugs()

    def overridden(self):
        """
        Returns ``True`` if the page's slug has an explicitly defined
        urlpattern and is therefore considered to be overridden.
        """
        from mezzanine.pages.views import page
        page_url = reverse("page", kwargs={"slug": self.slug})
        resolved_view = resolve(page_url)[0]
        return resolved_view != page

    def can_add(self, request):
        """
        Dynamic ``add`` permission for content types to override.
        """
        return self.slug != "/"

    def can_change(self, request):
        """
        Dynamic ``change`` permission for content types to override.
        """
        return True

    def can_delete(self, request):
        """
        Dynamic ``delete`` permission for content types to override.
        """
        return True
    

class TeacherGuidePage(LeafPage, RichText):
    
    class Meta:
        verbose_name = _("Teacher Guide Page")
        verbose_name_plural = _("Teacher Guide Pages")
        
    def __unicode__(self):
        return self.titles
    
    def get_absolute_url(self):
        slug = self.slug
        return reverse("teacherguide_detail", kwargs={"slug": slug})
        
class MediaArtefact(LeafPage, RichText, AdminThumbMixin):
    thumbnail = FileField(verbose_name=_("Thumbnail"),
                               upload_to="thumbs", format="Image",
                               max_length=255, null=True, blank=True)

    admin_thumb_field = "thumbnail"
    
    class Meta:
        verbose_name = _("Media Artefact")
        verbose_name_plural = _("Media Artefacts")
        
    def __unicode__(self):
        return self.titles
    
    def get_absolute_url(self):
        slug = self.slug
        return reverse("mediaartefact_detail", kwargs={"slug": slug})
 