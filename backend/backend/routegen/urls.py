from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


app_name = 'routegen'
urlpatterns = [
    url(r'^maps/$', views.map),
]

urlpatterns = format_suffix_patterns(urlpatterns)