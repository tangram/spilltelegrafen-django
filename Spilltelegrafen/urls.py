from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'forum.views.index', name='index'),
    url(r'^(?P<slug>[\w-]+)$', 'forum.views.topic', name='topic'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^imperavi/', include('imperavi.urls')),
    
)
