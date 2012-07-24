from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("cmlproject.views",
    url("^admin_page_ordering/$", "admin_page_ordering",
        name="admin_page_ordering"),
    url("^teacherguides/tag/(?P<tag>.*)/$", "teacherguide_list", name="teacherguide_list_tag"),
    url("^teacherguide/(?P<slug>.*)/$", "teacherguide_detail", name="teacherguide_detail"),
    url("^teacherguides/topic/$", "teacherguide_list", name="teacherguide_list"),
    url("^mediaartefacts/tag/(?P<tag>.*)/$", "teacherguide_list", name="mediaartefacts_list_tag"),
    url("^media/(?P<slug>.*)/$", "teacherguide_detail", name="mediaartefacts_detail"),
    url("^mediaartefacts/topic/$", "teacherguide_list", name="mediaartefacts_list"),
)