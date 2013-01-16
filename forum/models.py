# -*- coding: utf-8 -*-

from django.db import models
from core.models import Content, Comment

class ForumTopic(Content):
    '''The initial Content for a forum topic'''
    karma = models.SmallIntegerField(editable=False)

    class Meta:
        verbose_name = u'forumemne'
        verbose_name_plural = u'forumemner'


class ForumComment(Comment):
    '''Comments to a forum topic'''
    topic = models.ForeignKey(ForumTopic, editable=False)
    karma = models.SmallIntegerField(editable=False)

    class Meta:
        verbose_name = u'forumkommentar'
        verbose_name_plural = u'forumkommentarer'