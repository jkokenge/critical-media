from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, Http404

from django.shortcuts import get_object_or_404
from django import VERSION

from mezzanine.conf import settings
from mezzanine.pages import page_processors
from .models import MediaArtefact, Topic, Tag, GlossaryTerm
from mezzanine.utils.views import render, paginate


page_processors.autodiscover()


def admin_topic_ordering(request):
    """
    Updates the ordering of topics via AJAX from within the admin.
    """
    get_id = lambda s: s.split("_")[-1]
    for ordering in ("ordering_from", "ordering_to"):
        ordering = request.POST.get(ordering, "")
        if ordering:
            for i, topic in enumerate(ordering.split(",")):
                try:
                    t = Topic.objects.get(id=get_id(topic))
                    t._order=i
                    t.save()
                    #print "updated topic %s with order %d" % (Topic.objects.get(id=get_id(topic)).title,i)
                except Exception, e:
                    return HttpResponse(str(e))
    try:
        moved_topic = int(get_id(request.POST.get("moved_topic", "")))
    except ValueError, e:
        pass
    else:
        moved_parent = get_id(request.POST.get("moved_parent", ""))
        if not moved_parent:
            moved_parent = None
        try:
            topic = Topic.objects.get(id=moved_topic)
            topic.parent_topic_id = moved_parent
            topic.save()
            topic.reset_slugs()
        except Exception, e:
            return HttpResponse(str(e))
    return HttpResponse("ok")
admin_topic_ordering = staff_member_required(admin_topic_ordering)

def topic_background(request, slug,
                     template="cmlproject/topic_background.html"):
    
    topics = Topic.objects.all()
    topic = get_object_or_404(topics, slug=slug)
    #print 'topic is %s' % topic.title
    context = {"topic": topic}
    templates = [template]
    return render(request, templates, context)

def mediaartefact_list (request, tag=None, topic=None, template="cmlproject/mediaartefact_list.html"):
    """
    Display a list of media artefacts that are filtered by tag or topic.
    """
    settings.use_editable()
    templates = []
    mediaartefacts = MediaArtefact.objects.published(for_user=request.user)
    if tag is not None:
        tag = get_object_or_404(Tag, slug=tag)
        mediaartefacts = mediaartefacts.filter(tags__in=[tag])
        print mediaartefacts
    
    if topic is not None:
        topic = get_object_or_404(Topic, slug=topic)
        mediaartefacts = mediaartefacts.filter(featured_in__in=[topic])

    mediaartefacts = paginate(mediaartefacts,
                          request.GET.get("page", 1),
                          5,
                          5)
    context = {"mediaartefacts": mediaartefacts,
               "tag": tag, "topic":topic}
    templates.append(template)
    return render(request, templates, context)

def glossary_list (request, template="cmlproject/glossary_list.html"):
    """
    Display an alphabetical list of glossary words.
    """
    templates = []
    terms = GlossaryTerm.objects.all().order_by("name")
    
    context = {"terms": terms,}
    templates.append(template)
    return render(request, templates, context)

def mediaartefact_detail(request, slug,
                     template="cmlproject/mediaartefact_detail.html"):
    
    mediaartefacts = MediaArtefact.objects.published(for_user=request.user)
    mediaartefact = get_object_or_404(mediaartefacts, slug=slug)
    context = {"mediaartefact": mediaartefact}
    templates = [template]
    return render(request, templates, context)