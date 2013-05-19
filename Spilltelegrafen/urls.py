from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^imperavi/', include('imperavi.urls')),

    url(r'^$', 'forum.views.index', name='index'),
    url(r'^diskusjon/ny$', 'forum.views.post_discussion', name='post_discussion'),
    url(r'^diskusjon/(?P<discussion_id>[\d]+)$', 'forum.views.get_discussion', name='get_discussion'),
    
    url(r'^ajax/diskusjon/(?P<discussion_id>[\d]+)/ny$', 'forum.views.ajax_post_comment', name='ajax_post_comment'),
    
)
