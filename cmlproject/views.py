from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, Http404

from django.shortcuts import get_object_or_404
from django import VERSION

from mezzanine.conf import settings
from mezzanine.pages import page_processors
from .models import TeacherGuidePage, MediaArtefact, Topic
from mezzanine.utils.views import render, paginate


page_processors.autodiscover()


def admin_topic_ordering(request):
    """
    Updates the ordering of topics via AJAX from within the admin.
    """
    print "here"
    get_id = lambda s: s.split("_")[-1]
    ordering = request.POST.get("ordering_from", "")
    if ordering:
        for i, topic in enumerate(ordering.split(",")):
            try:
                Topic.objects.filter(id=get_id(topic)).update(_order=i)
                print"updated topic"
            except Exception, e:
                return HttpResponse(str(e))
    try:
        moved_topic = int(get_id(request.POST.get("moved_topic", "")))
    except ValueError, e:
        pass
    
    return HttpResponse("ok")
admin_topic_ordering = staff_member_required(admin_topic_ordering)

def teacherguide_list (request, tag=None, topic=None, template="cmlproject/teacherguide_list.html"):
    """
    Display a list of teacher guides that are filtered by tag or topic.
    """
    settings.use_editable()
    templates = []
    teacherguides = TeacherGuidePage.objects.published(for_user=request.user)
    if tag is not None:
        tag = get_object_or_404(Keyword, slug=tag)
        teacherguides = teacherguides.filter(keywords__in=tag.assignments.all())
    
    if topic is not None:
        topic = get_object_or_404(Topic, slug=topic)
        teacherguides = teacherguides.filter(parent=topic)

    #TODO prefetch tags

    teacherguides = paginate(teacherguides,
                          request.GET.get("page", 1),
                          5,
                          5)
    context = {"teacherguides": teacherguides,
               "tag": tag, "topic":topic}
    templates.append(template)
    return render(request, templates, context)


def teacherguide_detail(request, slug,
                     template="cmlproject/teacherguide_detail.html"):
    
    teacherguides = TeacherGuidePage.objects.published(for_user=request.user)
    teacherguide = get_object_or_404(teacherguides, slug=slug)
    context = {"teacherguide": teacherguide}
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
        tag = get_object_or_404(Keyword, slug=tag)
        mediaartefacts = mediaartefacts.filter(keywords__in=tag.assignments.all())
    
    if topic is not None:
        print topic
        topic = get_object_or_404(Topic, slug=topic)
        mediaartefacts = mediaartefacts.filter(parent=topic)

    #TODO prefetch tags

    mediaartefacts = paginate(mediaartefacts,
                          request.GET.get("page", 1),
                          5,
                          5)
    context = {"mediaartefacts": mediaartefacts,
               "tag": tag, "topic":topic}
    templates.append(template)
    return render(request, templates, context)


def mediaartefact_detail(request, slug,
                     template="cmlproject/mediaartefact_detail.html"):
    
    mediaartefacts = MediaArtefact.objects.published(for_user=request.user)
    mediaartefact = get_object_or_404(mediaartefacts, slug=slug)
    context = {"mediaartefact": mediaartefact}
    templates = [template]
    return render(request, templates, context)