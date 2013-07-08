# coding: utf-8

from __future__ import division

from django.db import models
from core.models import User, Content
from datetime import datetime
from django.utils.dateformat import DateFormat
from math import ceil

def timestring(date):
    now = datetime.now()
    if now.date() == date.date():
        return DateFormat(date).format('H:i')
    elif now.year == date.year:
        return DateFormat(date).format('j. F')
    else:
        return DateFormat(date).format('F Y')


class Kudos(models.Model):
    '''Kudos class, inherit to add kudos'''
    kudos = models.ManyToManyField(User, editable=False, related_name='%(class)s_kudos')

    class Meta:
        abstract = True
        verbose_name = u'kudos'
        verbose_name_plural = u'kudos'


class Comment(Kudos):
    '''Comments to a discussion'''
    author = models.ForeignKey(User, null=True, editable=False)

    created_time = models.DateTimeField(auto_now_add=True, editable=False)
    published_time = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    edited_time = models.DateTimeField(auto_now=True, null=True, editable=False)

    status = models.PositiveSmallIntegerField(default=1, editable=False)

    body = models.TextField(u'Kommentar')

    def get_absolute_url(self):
        per_page = 10
        orphans = 3
        discussion = self.discussion_set.all()[0]
        count = discussion.comment_count - orphans + 1
        page = int(ceil(count / per_page))
        if page > 1:
            return '%s?side=%s#%s' % (discussion.get_absolute_url(), page, self.id)
        else:
            return '%s#%s' % (discussion.get_absolute_url(), self.id)

    def __unicode__(self):
        return u'%s...' % (self.body[0:50])

    def classname(self):
        return self.__class__.__name__.lower()

    def created_time_formatted(self):
        return timestring(self.created_time)

    class Meta:
        verbose_name = u'kommentar'
        verbose_name_plural = u'kommentarer'


class Discussion(Content, Kudos):
    '''The initial Content for a discussion'''
    comments = models.ManyToManyField(Comment, editable=False)
    last_comment = models.ForeignKey(Comment, null=True, editable=False, related_name='last_comment')
    last_commenter = models.ForeignKey(User, null=True, editable=False, related_name='last_commenter')
    last_commented = models.DateTimeField(auto_now=True, null=True, editable=False)

    def get_absolute_url(self):
        return '/diskusjon/%s' % self.id

    def classname(self):
        return self.__class__.__name__.lower()

    def created_time_formatted(self):
        return timestring(self.created_time)

    def last_commented_formatted(self):
        return timestring(self.created_time)

    class Meta:
        verbose_name = u'diskusjon'
        verbose_name_plural = u'diskusjoner'
