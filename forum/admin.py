from django.contrib import admin
from forum.models import ForumTopic, ForumComment
from imperavi.admin import ImperaviAdmin

admin.site.register(ForumTopic, ImperaviAdmin)
admin.site.register(ForumComment, ImperaviAdmin)