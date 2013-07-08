from django.contrib import admin
from django.contrib.auth.models import Group
from core.models import User, Tag, StaticPage
from django.utils import formats
from django import forms
from suit.widgets import SuitSplitDateTimeWidget


class WYMLoader(admin.ModelAdmin):
    class Media:
        css = {
            "all": (
                "http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/themes/smoothness/jquery-ui.css",
                '/static/wymeditor/skins/default/skin.css'
            )
        }
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.5/jquery.min.js',
            '/static/wymeditor/jquery.wymeditor.js',
            '/static/wymeditor/plugins/embed/jquery.wymeditor.embed.js',
            '/static/js/wymeditor_setup.js',
        )


class UserForm(forms.ModelForm):
    class Meta:
        widgets = {
            'date_joined': SuitSplitDateTimeWidget,
            'last_login': SuitSplitDateTimeWidget,
        }


class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ('username', 'email', 'date_joined', 'last_login', 'last_seen', 'discussion_count', 'comment_count', 'image')
    search_fields = ['username', 'email']

    def format_date(self, obj):
        return formats.date_format(obj, "DATETIME_FORMAT")

    def date_joined(self, instance):
        return self.format_date(instance.date_joined)
    date_joined.admin_order_field = 'date_joined'

    def last_login(self, instance):
        return self.format_date(instance.last_login)
    last_login.admin_order_field = 'last_login'


class StaticPageAdmin(WYMLoader):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Tag)
admin.site.register(StaticPage, WYMLoader)
