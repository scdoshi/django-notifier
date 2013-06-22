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
class NotifierAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name', 'description', 'klass', 'enabled')
    prepopulated_fields = {'name': ('display_name',)}
admin.site.register(models.Notifier, NotifierAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name')
    prepopulated_fields = {'name': ('display_name',)}
admin.site.register(models.Notification, NotificationAdmin)


class GroupNotifyAdmin(admin.ModelAdmin):
    list_display = ('group', 'notification', 'notifier', 'notify')
    list_editable = ('notify',)
admin.site.register(models.GroupNotify, GroupNotifyAdmin)


class UserNotifyAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification', 'notifier', 'notify')
    list_editable = ('notify',)
admin.site.register(models.UserNotify, UserNotifyAdmin)


class SentNotifcationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification', 'notifier', 'success')
    readonly_fields = ('user', 'notification', 'notifier', 'success')
admin.site.register(models.SentNotification, SentNotifcationAdmin)
