from django import template
from cmlproject.models import Topic, Tag
from mezzanine import template

register = template.Library()

@register.assignment_tag
def get_topics():
    topics = Topic.objects.filter(parent_topic=None).order_by("_order")
    return topics

@register.assignment_tag
def get_tags(type):
    tags = Tag.objects.filter(tag_type=type).order_by("name")
    print tags
    return tags

@register.simple_tag
def active(request, url_name, *myargs):
    from django.core.urlresolvers import reverse
    relative_url = reverse(url_name,args=myargs)
    print "does request path %s match relative url %s?" % (request.path, relative_url)
    if request.path == relative_url:
        return 'active'
    return ''
