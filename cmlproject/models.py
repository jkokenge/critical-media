import os,re
from django.db import models
from django.core.urlresolvers import resolve, reverse

from django.db.models import URLField
from django.conf import settings

from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField

from mezzanine.core.models import Displayable, Orderable, RichText, Slugged
from mezzanine.utils.models import AdminThumbMixin

from mezzanine.utils.urls import admin_url, slugify

from .exceptions import MediaURLFetchError

import micawber

TOPIC_TAG = 0
GENRE_TAG = 1

TAG_TYPE_CHOICES = (
    (TOPIC_TAG, "Topic Tag"),
    (GENRE_TAG, "Genre Tag"),
)

VIDEO = 0
RICH = 1
IMAGE = 2

MEDIA_TYPE_CHOICES = (
    (VIDEO, "Video"),
    (RICH, "Rich"),
    (IMAGE, "Image"),
)

WISTIA_REGEX = "https?:\/\/(.+)?(wistia\.com|wi\.st)\/(medias|embed)\/.*"


    
class Topic(Orderable, Displayable, RichText, AdminThumbMixin):
    
    parent_topic = models.ForeignKey("self", blank=True, null=True, related_name="sub_topics", limit_choices_to={"parent_topic":None})
    featured_media = models.ManyToManyField("MediaArtefact", blank=True, null=True,related_name="featured_in")
    related_tag = models.ForeignKey("Tag",related_name="linked_topic", blank=True, null=True, limit_choices_to={"tag_type":TOPIC_TAG })
    
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
    
    def save(self, *args, **kwargs):
        
        if not self.related_tag:
            tag = Tag.objects.create(name=self.title, tag_type=TOPIC_TAG)
            tag.save();
            self.related_tag=tag

        super(Topic, self).save(*args, **kwargs)
        
class MediaArtefact(Orderable, Displayable, RichText):
    media_url = URLField(verbose_name=_("Media URL"),blank=True, null=True)

    media_type = models.SmallIntegerField(choices=MEDIA_TYPE_CHOICES, default = RICH)
    embed_code = models.TextField("Embed Code")
    thumbnail_url = URLField(verbose_name=_("Thumbnail"),blank=True, null=True)
    
    tags = models.ManyToManyField("Tag", blank=True, null=True,related_name="tagged_media")
    
    
    class Meta:
        verbose_name = _("Media Artifact")
        verbose_name_plural = _("Media Artifacts")
        
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        slug = self.slug
        return reverse("mediaartefact_detail", kwargs={"slug": slug})
    
    def get_admin_url(self):
        return admin_url(self, "change", self.id)
    
    def save(self, *args, **kwargs):
        providers = micawber.bootstrap_basic()
        providers.register(WISTIA_REGEX, micawber.Provider("http://fast.wistia.com/oembed/"))
        
        oembed_response = providers.request(self.media_url,maxwidth=600, maxheight=500, width=600)
        self.embed_code=oembed_response["html"]
        
        if oembed_response["type"]=="photo":
            self.media_type = IMAGE
            
            #request the image again, add full-size link to the embed code
            second_oembed_response = providers.request(self.media_url)
            link_text = '<div class="viewfullsize-link"><a href="%s">View full-size image</a></div>' % second_oembed_response["url"]
            self.embed_code = "".join([self.embed_code,link_text])
            
        elif oembed_response["type"]=="video":
            self.media_type = VIDEO
            
        elif oembed_response["type"]=="rich":
            self.media_type = RICH
            
        
        try:
            if "thumbnail_url" in oembed_response:
                self.thumbnail_url=oembed_response["thumbnail_url"]
                
            elif oembed_response["type"]=="photo":
                self.thumbnail_url = oembed_response["url"]
            else:
                self.thumbnail_url = os.path.join(settings.STATIC_URL,"images/rich.png")

        except:
            self.thumbnail_url=""
        
        '''
        TODO some hacky Wistia-specific additions here
        '''
        if re.match(WISTIA_REGEX,self.media_url):
            self.thumbnail_url = "%s?image_crop_resized=260x180" % self.thumbnail_url.split("?")[0]
            
            if self.media_type == IMAGE:
                self.embed_code = re.sub("image_crop_resized","image_resize",self.embed_code)
                
            elif self.media_type == RICH:
                
                if oembed_response["url"]:
                    link_text = '<div class="viewfullsize-link"><a href="%s">Download this file</a></div>' % oembed_response["url"]
                    self.embed_code = "".join([self.embed_code,link_text])

        super(MediaArtefact, self).save(*args, **kwargs)
        
class Tag(Slugged):
    name = models.CharField(_("Tag Name"), max_length=100)
    tag_type = models.SmallIntegerField(choices=TAG_TYPE_CHOICES, default = TOPIC_TAG)
    
    class Meta:
        verbose_name = _("Media Tag")
        verbose_name_plural = _("Media Tags")
        
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.name
            
        super(Tag, self).save(*args, **kwargs)
        
class GlossaryTerm(Slugged):
    name = models.CharField(_("Term"), max_length=1000, unique=True)
    explanation = models.TextField(_("Explanation"))
    
    class Meta:
        verbose_name = _("Glossary Term")
        verbose_name_plural = _("Glossary Terms")
        
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.name
            
        super(GlossaryTerm, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        slug = self.slug
        return reverse("glossary_term", kwargs={"slug": slug})

 