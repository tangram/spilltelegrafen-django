from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'forum.views.index', name='index'),
    url(r'^mine-diskusjoner$', 'forum.views.get_own_discussions', name='my_discussions'),
    url(r'^mine-utkast$', 'forum.views.get_own_drafts', name='my_drafts'),
    url(r'^logg-ut$', 'forum.views.user_logout', name='logout'),
    url(r'^diskusjon/ny$', 'forum.views.post_discussion', name='post_discussion'),
    url(r'^diskusjon/(?P<discussion_id>[\d]+)$', 'forum.views.get_discussion', name='discussion'),
    url(r'^diskusjon/(?P<discussion_id>[\d]+)/rediger$', 'forum.views.update_discussion', name='update_discussion'),
    url(r'^diskusjon/(?P<discussion_id>[\d]+)/slett$', 'forum.views.delete_discussion', name='delete_discussion'),

    url(r'^diskusjon/(?P<discussion_id>[\d]+)/kommentar/ny$', 'forum.views.ajax_post_comment', name='ajax_post_comment'),
    url(r'^diskusjon/(?P<discussion_id>[\d]+)/kommentar/(?P<comment_id>[\d]+)/rediger$', 'forum.views.ajax_update_comment', name='update_comment'),
    url(r'^diskusjon/(?P<discussion_id>[\d]+)/kommentar/(?P<comment_id>[\d]+)/slett$', 'forum.views.ajax_delete_comment', name='delete_comment'),

    url(r'^diskusjon/(?P<discussion_id>[\d]+)/kudos$', 'forum.views.ajax_kudos', name='ajax_discussion_kudos'),
    url(r'^kommentar/(?P<comment_id>[\d]+)/kudos$', 'forum.views.ajax_kudos', name='ajax_comment_kudos'),
    url(r'^diskusjon/(?P<discussion_id>[\d]+)/kudos/slett$', 'forum.views.ajax_kudos', name='ajax_discussion_unkudos'),
    url(r'^kommentar/(?P<comment_id>[\d]+)/kudos/slett$', 'forum.views.ajax_kudos', name='ajax_comment_unkudos'),

    url(r'^bruker/(?P<user_id>[\d]+)$', 'forum.views.get_user', name='user'),
    url(r'^bruker/(?P<user_id>[\d]+)$', 'forum.views.update_user', name='update_user'),

)
