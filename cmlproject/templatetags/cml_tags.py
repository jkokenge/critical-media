from django import template
from cmlproject.models import Topic, Tag, GlossaryTerm
from mezzanine import template
import re

register = template.Library()

@register.assignment_tag
def get_topics():
    topics = Topic.objects.filter(parent_topic=None).order_by("_order")
    return topics

@register.assignment_tag
def get_tags(type):
    tags = Tag.objects.filter(tag_type=type).order_by("name")
    return tags

@register.simple_tag
def active(request, url_name, *myargs):
    from django.core.urlresolvers import reverse
    relative_url = reverse(url_name,args=myargs)
    if request.path == relative_url:
        return 'active'
    return ''

@register.filter
def add_glossary_tooltips(text):
    terms = dict((t.name.upper(), [t.explanation, t.get_absolute_url()]) for t in GlossaryTerm.objects.all())
    words = re.split('(\W)',text)
        
    for i in range(len(words)):
        if (not words[i]==" ") and (words[i].upper() in terms):
            words[i] = '<a href="%s" rel="tooltip" title="%s">%s</a>' % (terms[words[i].upper()][1],terms[words[i].upper()][0], words[i])
                                                                                
    return "".join(words)
