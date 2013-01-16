# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
# from imagekit.models import ImageSpecField

# USERS
class UserProfile(models.Model):
    '''User profile, connected to a User'''
    user = models.OneToOneField(User, editable=False)
    user_img = models.ImageField(
        u'Brukerbilde', upload_to='brukerbilder')
    # avatar = ImageSpecField(
    #     u'Avatar', [ResizeToFill(50, 50)], image_field='user_img')

    allow_private_messages = models.BooleanField(
        u'Tillat private meldinger?', default=True)
    mail_on_private_message = models.BooleanField(
        u'Få mail når du mottar private meldinger?', default=True)
    mail_on_comment = models.BooleanField(
        u'Få mail ved svar på kommentar eller innlegg?', default=True)

    class Meta:
        app_label = u'auth'
        verbose_name = u'brukerprofil'
        verbose_name_plural = u'brukerprofiler'


# CONTENT
class Content(models.Model):
    '''Abstract base class for content (e.g. page, post)'''
    title = models.CharField(u'Tittel', max_length=255)
    author = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, editable=False)

    created_time = models.DateTimeField(auto_now_add=True, editable=False)
    edited_time = models.DateTimeField(auto_now=True, editable=False)
    publish_time = models.DateTimeField(
        u'Publikasjonstidspunkt', auto_now_add=True)
    # comments_allowed = models.BooleanField(editable=False)

    body = models.TextField(u'Brødtekst')

    published = models.BooleanField(u'Publisert', default=False)

    def __unicode__(self):
        return u'%s' % (self.title)

    class Meta:
        abstract = True


class Comment(models.Model):
    '''Abstract base class for comments.
       Needs a ForeignKey to subclass of Content,
       i.e. the Content to which it is a comment.'''
    author = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, editable=False)
    # content = models.ForeignKey(Content, editable=False)

    created_time = models.DateTimeField(
        auto_now_add=True, editable=False)
    edited_time = models.DateTimeField(
        auto_now=True, editable=False)

    body = models.TextField(u'Kommentar')

    def __unicode__(self):
        return u'%s...' % (self.body[0:50])

    class Meta:
        abstract = True


class Tag(models.Model):
    '''Generic tag model'''
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        verbose_name = u'tag'


class StaticPage(Content):
    '''Generic static page model'''
    class Meta:
        verbose_name = u'fast side'
        verbose_name_plural = u'faste sider'
