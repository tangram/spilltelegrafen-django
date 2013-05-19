from django.contrib import admin
from forum.models import Discussion, Comment
from imperavi.admin import ImperaviAdmin

admin.site.register(Discussion, ImperaviAdmin)
admin.site.register(Comment, ImperaviAdmin)