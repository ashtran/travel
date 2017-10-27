from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^createuser$', views.createuser),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^dashboard/(?P<plan_id>\d+)/delete$', views.delete),
    url(r'^dashboard/(?P<plan_id>\d+)/add$', views.join),
    url(r'^addplan$', views.addplan),
    url(r'^processplan$', views.processplan),
    url(r'^destination/(?P<plan_id>\d+)$', views.destination),
    url(r'^logout$', views.logout)
]
