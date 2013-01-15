from django.contrib import admin
from magasin.models import Artikkel
from imperavi.admin import ImperaviAdmin

admin.site.register(Artikkel, ImperaviAdmin)