from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from joy import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^watchdog$', views.watchdog),
    url(r'^webhook$', views.webhook),
    url(r'^privacypolicy$', views.privacypolicy),
    url(r'^magic$', views.magic),
    #url(r'^translate$', views.translate),
    #url(r'^translate_api$', views.translate_api),
    #url(r'^comments', views.comments),
    #url(r'^users/$', views.UserList.as_view()),
    #url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    #url(r'^groups/$', views.GroupList.as_view()),
    #url(r'^groups/(?P<pk>[0-9]+)/$', views.GroupDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)