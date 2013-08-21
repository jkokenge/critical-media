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
    terms = dict((t.name.upper().strip(), [t.explanation, t.get_absolute_url()]) for t in GlossaryTerm.objects.filter(auto_highlight=True))
    def chunks():
        for chunk in re.split('(<.*?>)',text):
            if not chunk.startswith("<"):
                words = re.split('(\W)',chunk)
                
                for i in range(len(words)):
                    if (not words[i]==" ") and (words[i].upper() in terms):
                        words[i] = '<a href="%s" rel="tooltip" title="%s">%s</a>' % (terms[words[i].upper()][1],terms[words[i].upper()][0], words[i])
                                                                                        
                chunk = "".join(words)
            yield chunk
    return ''.join(chunks())

@register.filter
def add_title_classes(text):
    words = re.split('(?:\W)',text)
    print words
    output=''
        
    for i in range(len(words)):
        if i % 2 ==0:
            titleclass='even'
        else:
            titleclass='odd'
        
        output += '<span class="%s">%s</span>' % (titleclass, words[i])
                                                                                
    return output

@register.filter
def partition(thelist, n):
    """
    http://djangosnippets.org/snippets/6/
    
    Break a list into ``n`` pieces. The last list may be larger than the rest if
    the list doesn't break cleanly. That is::

        >>> l = range(10)

        >>> partition(l, 2)
        [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]

        >>> partition(l, 3)
        [[0, 1, 2], [3, 4, 5], [6, 7, 8, 9]]

        >>> partition(l, 4)
        [[0, 1], [2, 3], [4, 5], [6, 7, 8, 9]]

        >>> partition(l, 5)
        [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]

    """
    try:
        n = int(n)
        thelist = list(thelist)
    except (ValueError, TypeError):
        return [thelist]
    p = len(thelist) / n
    return [thelist[p*i:p*(i+1)] for i in range(n - 1)] + [thelist[p*(i+1):]]
