from django.contrib import admin
from core.models import Profile, Tag, StaticPage
from imperavi.admin import ImperaviAdmin

admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(StaticPage, ImperaviAdmin)