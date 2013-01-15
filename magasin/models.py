# -*- coding: utf-8 -*-

from core.models import Content

class Artikkel(Content):
    class Meta:
        verbose_name = u'artikkel'
        verbose_name_plural = u'artikler'