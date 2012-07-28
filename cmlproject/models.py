from django.db import models
from django.core.urlresolvers import resolve, reverse

from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField

from mezzanine.core.models import Displayable, Orderable, RichText, Slugged
from mezzanine.utils.models import AdminThumbMixin

from mezzanine.utils.urls import admin_url, slugify

    
class Topic(Orderable, Displayable, RichText, AdminThumbMixin):
    
    parent_topic = models.ForeignKey("self", blank=True, null=True, related_name="sub_topics", limit_choices_to={"parent_topic":None})
    featured_media = models.ManyToManyField("MediaArtefact", blank=True, null=True,related_name="featured_in")
    
    icon = FileField(verbose_name=_("Icon"),
                               upload_to="thumbs", format="Image",
                               max_length=255, null=True, blank=True)
    
    admin_thumb_field = "icon"
    
    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        ordering = ("title",)
        order_with_respect_to = "parent_topic"
        
    def __unicode__(self):
        return self.title
    
    def get_slug(self):
        """
        Recursively build the slug from the chain of parents.
        """
        slug = slugify(self.title)
        if self.parent_topic is not None:
            return "%s/%s" % (self.parent_topic.slug, slug)
        return slug
  
    def reset_slugs(self):
        """
        Called when the parent page is changed in the admin and the slug
        plus all child slugs need to be recreated given the new parent.
        """
        if not self.overridden():
            self.slug = None
            self.save()
        for child in self.sub_topics.all():
            child.reset_slugs()
            
    def get_titles(self):
        titles = [self.title]
        parent = self.parent_topic
        if parent is not None:
            titles.insert(0, unicode(self._meta.verbose_name_plural))
            titles.insert(0, parent.title)

        self.titles = " / ".join(titles)
        return titles
        
    def get_absolute_url(self):
        slug = self.slug
        return reverse("topic_background", kwargs={"slug": slug})
                       
    def get_admin_url(self):
        return admin_url(self, "change", self.id)
        
        
class MediaArtefact(Orderable, Displayable, RichText, AdminThumbMixin):
    thumbnail = FileField(verbose_name=_("Thumbnail"),
                               upload_to="thumbs", format="Image",
                               max_length=255, null=True, blank=True)

    admin_thumb_field = "thumbnail"
    
    class Meta:
        verbose_name = _("Media Artefact")
        verbose_name_plural = _("Media Artefacts")
        
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        slug = self.slug
        return reverse("mediaartefact_detail", kwargs={"slug": slug})
    
    def get_admin_url(self):
        return admin_url(self, "change", self.id)
    
    def get_slug(self):
        slug = slugify(self.title)

 