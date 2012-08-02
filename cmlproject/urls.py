from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("cmlproject.views",
    url("^admin_topic_ordering/$", "admin_topic_ordering",
        name="admin_topic_ordering"),
    url("^topicbackground/(?P<slug>.*)/$", "topic_background", name="topic_background"),
    url("^media/tag/(?P<tag>.*)/$", "mediaartefact_list", name="mediaartefact_list_tag"),
    url("^media/$", "mediaartefact_list", name="mediaartefact_list"),
    url("^media/topic/(?P<topic>.*)/$", "mediaartefact_list", name="mediaartefact_list_topic"),
    url("^media/(?P<slug>.*)/$", "mediaartefact_detail", name="mediaartefact_detail"),
    url("^glossary/$", "glossary_list", name="glossary_list"),
    url("^glossary/(?P<slug>.*)/$", "glossary_term", name="glossary_term"),
    
)