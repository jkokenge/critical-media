from django import template
from cmlproject.models import Topic
from mezzanine import template

register = template.Library()

@register.assignment_tag
def get_topics():
    topics = Topic.objects.all()
    return topics