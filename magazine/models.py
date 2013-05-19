# coding: utf-8

from django.db import models
from core.models import Content, Tag

class Article(Content):
    '''An article in the magazine'''
    image = models.ImageField('Headerbilde', upload_to='header')
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        verbose_name = u'artikkel'
        verbose_name_plural = u'artikler'