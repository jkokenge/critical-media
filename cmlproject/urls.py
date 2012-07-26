from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("cmlproject.views",
    url("^admin_topic_ordering/$", "admin_topic_ordering",
        name="admin_topic_ordering"),
    url("^topicbackground/(?P<parentslug>.*)/$", "topic_background", name="topic_background"),
    url("^teacherguides/tag/(?P<tag>.*)/$", "teacherguide_list", name="teacherguide_list_tag"),
    url("^teacherguides/$", "teacherguide_list", name="teacherguide_list"),
    url("^teacherguides/topic/(?P<topic>.*)/$", "teacherguide_list", name="teacherguide_list_topic"),
    url("^teacherguides/(?P<slug>.*)/$", "teacherguide_detail", name="teacherguide_detail"),
    url("^media/tag/(?P<tag>.*)/$", "mediaartefact_list", name="mediaartefact_list_tag"),
    url("^media/$", "mediaartefact_list", name="mediaartefact_list"),
    url("^media/topic/(?P<topic>.*)/$", "mediaartefact_list", name="mediaartefact_list_topic"),
    url("^media/(?P<slug>.*)/$", "mediaartefact_detail", name="mediaartefact_detail"),
    
)