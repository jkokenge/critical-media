from django.db import models
from django.core.urlresolvers import resolve, reverse

from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField

from mezzanine.core.models import Displayable, Orderable, RichText, Slugged
from mezzanine.utils.models import AdminThumbMixin

from mezzanine.utils.urls import admin_url, slugify

TOPIC_TAG = 0
GENRE_TAG = 1

TAG_TYPE_CHOICES = (
    (TOPIC_TAG, "Topic Tag"),
    (GENRE_TAG, "Genre Tag"),
)

VIDEO = 0
SOUND = 1
IMAGE = 2

MEDIA_TYPE_CHOICES = (
    (VIDEO, "Video"),
    (SOUND, "Sound"),
    (IMAGE, "Image"),
)


    
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
    
    def ordered_sub_topics(self):
        return self.sub_topics.order_by('_order')
    
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
    media_type = models.SmallIntegerField(choices=MEDIA_TYPE_CHOICES, default = VIDEO)
    
    embed_code = models.TextField("Embed Code",blank=True, null=True)
    
    tags = models.ManyToManyField("Tag", blank=True, null=True,related_name="tagged_media")
    
    
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
        
class Tag(Slugged):
    name = models.CharField(_("Tag Name"), max_length=100)
    tag_type = models.SmallIntegerField(choices=TAG_TYPE_CHOICES, default = TOPIC_TAG)
    
    class Meta:
        verbose_name = _("Media Tag")
        verbose_name_plural = _("Media Tags")
        
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """
        Create a unique slug by appending an index.
        """
        if not self.title:
            self.title = self.name
            
        super(Tag, self).save(*args, **kwargs)

 