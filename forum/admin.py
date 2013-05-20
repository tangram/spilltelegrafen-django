from django.contrib import admin
from forum.models import Discussion, Comment

class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_time', 'edited_time', 'comment_count', 'last_commented', 'last_commenter', 'last_comment', 'status')
    search_fields = ['author__username', 'title']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('excerpt', 'author', 'created_time', 'edited_time', 'discussion', 'status')
    search_fields = ['discussion', 'author__username']

    def discussion(self, instance):
        return instance.discussion_set.all()[0]

    def excerpt(self, instance):
        return instance.body[:100]


admin.site.register(Discussion, DiscussionAdmin)
admin.site.register(Comment, CommentAdmin)