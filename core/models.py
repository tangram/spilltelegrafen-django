# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

#from imagekit.models import ImageSpecField
#from imagekit.processors import ResizeToFill

#from autoslug import AutoSlugField

# USERS
class Profile(models.Model):
    '''User profile, connected to a User'''
    user = models.OneToOneField(User)
    #slug = AutoSlugField(populate_from=lambda instance: instance.user.username, unique=True)

    image = models.ImageField(
        u'Brukerbilde', upload_to='brukerbilder')
    #avatar_image = ImageSpecField([ResizeToFill(50, 50)], image_field='image', options={'quality': 85})
    #avatar_large_image = ImageSpecField([ResizeToFill(200, 200)], image_field='image', options={'quality': 85})

    mail_on_comment = models.BooleanField(
        u'Få mail ved svar på kommentar eller innlegg?', default=True)

    last_seen = models.DateTimeField(auto_now=True, editable=False)
    discussion_count = models.PositiveSmallIntegerField(default=0, editable=False)
    comment_count = models.PositiveSmallIntegerField(default=0, editable=False)

    def get_absolute_url(self):
        return '/profil/%s' % self.user

    class Meta:
        verbose_name = u'brukerprofil'
        verbose_name_plural = u'brukerprofiler'


# CONTENT
class Content(models.Model):
    '''Abstract base class for content (e.g. page, post)'''
    title = models.CharField(u'Tittel', max_length=255)
    #slug = AutoSlugField(populate_from='title', unique=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, editable=False)

    created_time = models.DateTimeField(auto_now_add=True, editable=False)
    publish_time = models.DateTimeField(auto_now_add=True)
    edited_time = models.DateTimeField(auto_now=True, editable=False)

    status = models.PositiveSmallIntegerField(default=1, editable=False)  # seems like a good idea
    comment_count = models.PositiveSmallIntegerField(default=0, editable=False)
    view_count = models.PositiveSmallIntegerField(default=0, editable=False)

    body = models.TextField(u'Brødtekst')

    published = models.BooleanField(u'Publisert', default=False)

    def __unicode__(self):
        return u'%s' % (self.title)

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


# FLAGS
class Flag(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content = generic.GenericForeignKey()
    created_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s, %s, %s' % (self.creator, self.name, self.content.title)

    class Meta:
        verbose_name = u'flagg'
        verbose_name_plural = u'flagg'
