# -*- coding: utf-8 -*-

from django.db import models
from core.models import Content, Comment

class ForumTopic(Content):
    karma = models.IntegerField(editable=False)

    class Meta:
        verbose_name = u'forumemne'
        verbose_name_plural = u'forumemner'


class ForumComment(Comment):
    topic = models.ForeignKey(ForumTopic, editable=False)

    class Meta:
        verbose_name = u'forumkommentar'
        verbose_name_plural = u'forumkommentarer'