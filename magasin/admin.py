from django.contrib import admin
from magasin.models import Article
from imperavi.admin import ImperaviAdmin

admin.site.register(Article, ImperaviAdmin)