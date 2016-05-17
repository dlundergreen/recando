from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.land, name='land'),
    url(r'prodash/$', views.prodash, name='prodash'),
    url(r'^grodash/(?P<club_id>[0-9]+)/$', views.grodash, name='grodash'),
    url(r'^creategroup/$', views.creategroup, name='creategroup'),
    url(r'^joingroup/$', views.joingroup, name='joingroup'),
    url(r'^createpost/$', views.createpost, name='createpost'),
    url(r'^post/(?P<post_id>[0-9]+)/$', views.post, name='post'),
    url(r'^addcomment/$', views.addcomment, name='addcomment'),
    url(r'^analytics/$', views.anal_dashboard, name='anal_dashboard'),
]
