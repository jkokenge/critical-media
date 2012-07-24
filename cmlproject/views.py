from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, Http404

from mezzanine.conf import settings
from mezzanine.pages import page_processors
from .models import TeacherGuidePage
from mezzanine.utils.views import render


page_processors.autodiscover()


def admin_page_ordering(request):
    """
    Updates the ordering of pages via AJAX from within the admin.
    """
    get_id = lambda s: s.split("_")[-1]
    for ordering in ("ordering_from", "ordering_to"):
        ordering = request.POST.get(ordering, "")
        if ordering:
            for i, page in enumerate(ordering.split(",")):
                try:
                    LeafPage.objects.filter(id=get_id(page)).update(_order=i)
                except Exception, e:
                    return HttpResponse(str(e))
    try:
        moved_page = int(get_id(request.POST.get("moved_page", "")))
    except ValueError, e:
        pass
    else:
        moved_parent = get_id(request.POST.get("moved_parent", ""))
        if not moved_parent:
            moved_parent = None
        try:
            page = LeafPage.objects.get(id=moved_page)
            page.parent_id = moved_parent
            page.save()
            page.reset_slugs()
        except Exception, e:
            return HttpResponse(str(e))
    return HttpResponse("ok")
admin_page_ordering = staff_member_required(admin_page_ordering)

def teacherguide_list (request, tag=None, topic=None, template="cmlproject/teacherguide_list.html"):
    """
    Display a list of teacher guides or media artefacts that are filtered by tag or topic.
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

    # We want to iterate keywords and categories for each blog post
    # without triggering "num posts x 2" queries.
    # For Django 1.4 we just use prefetch related.

    if VERSION >= (1, 4):
        rel = ("keywords__keyword")
        teacherguides = teacherguides.select_related("user").prefetch_related(*rel)
    
    for i, teacherguide in enumerate(teacherguides):
        if VERSION < (1, 4):
            setattr(teacherguides[i], "keyword_list", keywords[post.id])
        else:
            setattr(teacherguides[i], "keyword_list",
                    [k.keyword for k in teacherguide.keywords.all()])

    teacherguides = paginate(teacherguides,
                          request.GET.get("page", 1),
                          5,
                          5)
    context = {"teacherguides": teacherguides,
               "tag": tag}
    templates.append(template)
    return render(request, templates, context)


def teacherguide_detail(request, slug,
                     template="cmlproject/teacherguide_detail.html"):
    
    teacherguides = TeacherGuidePage.objects.published(for_user=request.user)
    teacherguide = get_object_or_404(teacherguides, slug=slug)
    context = {"teacherguide": teacherguide}
    templates = [template]
    return render(request, templates, context)