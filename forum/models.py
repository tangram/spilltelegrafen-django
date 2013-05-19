# coding: utf-8

from django.db import models
from core.models import Content
from django.contrib.auth.models import User

class Kudos(models.Model):
    '''Kudos class, inherit to add kudos'''
    kudos = models.ManyToManyField(User, editable=False)
    given = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = u'kudos'
        verbose_name_plural = u'kudos'


class Comment(Kudos):
    '''Comments to a discussion'''
    author = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, editable=False)

    created_time = models.DateTimeField(
        auto_now_add=True, editable=False)
    published_time = models.DateTimeField(
        auto_now_add=True, editable=False)
    edited_time = models.DateTimeField(
        auto_now=True, editable=False)

    body = models.TextField(u'Kommentar')

    def get_absolute_url(self):
        return '%s/kommentar/%s' % (self.discussion.get_absolute_url(), self.id)

    def __unicode__(self):
        return u'%s...' % (self.body[0:50])

    class Meta:
        verbose_name = u'kommentar'
        verbose_name_plural = u'kommentarer'


class Discussion(Content, Kudos):
    '''The initial Content for a discussion'''
    comments = models.ManyToManyField(Comment, editable=False)

    def get_absolute_url(self):
        return '/diskusjon/%s' % self.id

    class Meta:
        verbose_name = u'diskusjon'
        verbose_name_plural = u'diskusjoner'
