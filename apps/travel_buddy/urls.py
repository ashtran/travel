from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),        #<--- render index.html
    url(r'^createuser$', views.createuser),     #<--- redirect /dashboard
    url(r'^login$', views.login),       #<--- redirect  /dashboard
    url(r'^dashboard$', views.dashboard),       #<--- render dashboard.html
    url(r'^addplan$', views.addplan),
    url(r'^processplan$', views.processplan),   #<-- redirect /reviews/<book_id>
    url(r'^destination/(?P<plan_id>\d+)$', views.destination),    #<--- render user.html
    url(r'^logout$', views.logout)
]
