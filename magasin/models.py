# -*- coding: utf-8 -*-

from django.db import models
from core.models import Content, Tag

class Article(Content):
    '''An article in the magazine'''
    # Every article needs a representative image
    image = models.ImageField('Headerbilde', upload_to='header')

    # TODO: Add gallery functionality?

    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        verbose_name = u'artikkel'
        verbose_name_plural = u'artikler'