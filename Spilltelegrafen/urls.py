from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'forum.views.index', name='index'),
    url(r'^diskusjon/ny$', 'forum.views.post_discussion', name='post_discussion'),
    url(r'^diskusjon/(?P<id>[\d]+)$', 'forum.views.get_discussion', name='get_discussion'),
    
)
