from django.contrib import admin
from core.models import UserProfile, Tag, StaticPage
from imperavi.admin import ImperaviAdmin

admin.site.register(UserProfile)
admin.site.register(Tag)
admin.site.register(StaticPage, ImperaviAdmin)