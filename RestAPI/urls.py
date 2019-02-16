from django.conf.urls import url

from RestAPI import views

urlpatterns = [
    url(r'^events/$', views.events, name='events'),
    url(r'^events/actors/(\d{1,})/$', views.events_detail, name='events'),
    url(r'^actors/$', views.actors, name='events'),
    url(r'^actors/streak/$', views.actors_detail, name='events'),
    url(r'^erase/$', views.events, name='erase')
]
