from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic.base import RedirectView

from RestAPI import urls

urlpatterns = [
    url(r'^', include("RestAPI.urls")),
    url(r'^admin/', include(admin.site.urls))
]

urlpatterns = format_suffix_patterns(urlpatterns)
