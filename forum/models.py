# coding: utf-8

from django.db import models
from core.models import Content
from django.contrib.auth.models import User

class Kudos(models.Model):
    '''Kudos class, inherit to add kudos'''
    kudos = models.ManyToManyField(User, editable=False, related_name='%(class)s_kudos')
    given = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True
        verbose_name = u'kudos'
        verbose_name_plural = u'kudos'


class Comment(Kudos):
    '''Comments to a discussion'''
    author = models.ForeignKey(User, null=True, editable=False)

    created_time = models.DateTimeField(auto_now_add=True, editable=False)
    published_time = models.DateTimeField(auto_now_add=True, editable=False)
    edited_time = models.DateTimeField(auto_now=True, editable=False)

    body = models.TextField(u'Kommentar')

    def get_absolute_url(self):
        return '%s/kommentar/%s' % (self.discussion.get_absolute_url(), self.id)

    def __unicode__(self):
        return u'%s...' % (self.body[0:50])

    def classname(self):
        return self.__class__.__name__.lower()

    class Meta:
        verbose_name = u'kommentar'
        verbose_name_plural = u'kommentarer'


class Discussion(Content, Kudos):
    '''The initial Content for a discussion'''
    comments = models.ManyToManyField(Comment, editable=False)
    last_commenter = models.ForeignKey(User, null=True, editable=False, related_name='last_commenter')
    last_update = models.DateTimeField(auto_now=True, editable=False)

    def get_absolute_url(self):
        return '/diskusjon/%s' % self.id

    def classname(self):
        return self.__class__.__name__.lower()

    class Meta:
        verbose_name = u'diskusjon'
        verbose_name_plural = u'diskusjoner'
