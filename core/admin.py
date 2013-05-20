from django.contrib import admin
from core.models import Profile, Tag, StaticPage
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils import formats

UserAdmin.list_display = ('username', 'email', 'date_joined', 'last_login', 'is_active', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_email', 'user_date_joined', 'user_last_login', 'last_seen', 'discussion_count', 'comment_count', 'image')
    search_fields = ['user__username', 'user__email']

    def format_date(self, obj):
        return formats.date_format(obj, "DATETIME_FORMAT")

    def user_email(self, instance):
        return instance.user.email

    def user_date_joined(self, instance):
        return self.format_date(instance.user.date_joined)
    user_date_joined.admin_order_field = 'user__date_joined'

    def user_last_login(self, instance):
        return self.format_date(instance.user.last_login)
    user_last_login.admin_order_field = 'user__last_login'


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tag)
admin.site.register(StaticPage)