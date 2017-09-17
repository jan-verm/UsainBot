from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from maps import views

urlpatterns = [
    url(r'^maps/(?P<longtitude>\w{0,50})/(?P<lat>\w{0,50})/(?P<km>\w{0,50})/(?P<monumentbool>\w{0,50})/(?P<nr_of_mutations>\w{0,50})/$', views.MapList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)