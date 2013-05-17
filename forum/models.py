# -*- coding: utf-8 -*-

from django.db import models
from core.models import Content, Comment
from django.contrib.auth.models import User

class Kudos(models.Model):
    '''Kudos class, inherit to add kudos'''
    kudos = models.ManyToManyField(User, editable=False)
    given = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = u'kudos'
        verbose_name_plural = u'kudos'


class ForumComment(Comment, Kudos):
    '''Comments to a forum topic'''

    class Meta:
        verbose_name = u'forumkommentar'
        verbose_name_plural = u'forumkommentarer'


class ForumTopic(Content, Kudos):
    '''The initial Content for a forum topic'''
    topic = models.ManyToManyField(ForumComment, editable=False)

    class Meta:
        verbose_name = u'forumemne'
        verbose_name_plural = u'forumemner'
