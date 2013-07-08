from django.contrib import admin
from magazine.models import Article
from core.models import Tag
from django import forms
from django_select2.fields import ModelSelect2MultipleField
from core.admin import WYMLoader


class ArticleForm(forms.ModelForm):
    tags = ModelSelect2MultipleField(queryset=Tag.objects)


class ArticleAdmin(WYMLoader):
    form = ArticleForm


admin.site.register(Article, ArticleAdmin)
