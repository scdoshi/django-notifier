###############################################################################
## Imports
###############################################################################
# Django
from django.contrib import admin

# User
from notifier import models


###############################################################################
## Admin
###############################################################################
class BackendAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'enabled')
    readonly_fields = ('name', 'display_name', 'description', 'klass')
    list_editable = ('enabled',)
admin.site.register(models.Backend, BackendAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name')
    prepopulated_fields = {'name': ('display_name',)}
admin.site.register(models.Notification, NotificationAdmin)


class GroupPrefsAdmin(admin.ModelAdmin):
    list_display = ('group', 'notification', 'backend', 'notify')
    list_editable = ('notify',)
admin.site.register(models.GroupPrefs, GroupPrefsAdmin)


class UserPrefsAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification', 'backend', 'notify')
    list_editable = ('notify',)
admin.site.register(models.UserPrefs, UserPrefsAdmin)


class SentNotifcationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification', 'backend', 'success')
    readonly_fields = ('user', 'notification', 'backend', 'success')
admin.site.register(models.SentNotification, SentNotifcationAdmin)
