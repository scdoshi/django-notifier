###############################################################################
## Imports
###############################################################################
# Python
from collections import Iterable
from importlib import import_module

# Django
from django.contrib.auth.models import User, Group, Permission
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# External
from bits.models import BaseModel

# User
from notifier import managers


###############################################################################
## Models
###############################################################################
class Notifier(BaseModel):
    """
    Entries for various delivery backends (SMS, Email)
    """
    name = models.CharField(max_length=200, unique=True, db_index=True)
    display_name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=500, null=True)

    # This can be set to False to stop all deliveries using this
    # method, regardless of permissions and preferences
    enabled = models.BooleanField(default=True)

    # The klass value defines the class to be used to send the notification.
    klass = models.CharField(max_length=500,
        help_text='Example: notifier.methods.Backend')

    def __unicode__(self):
        return self.name

    def _get_notifierclass(self):
        """
        Return the python class from the string value in `self.klass`
        """
        module, klass = self.klass.rsplit('.', 1)
        return getattr(import_module(module), klass)
    notifierclass = property(_get_notifierclass)

    def send(self, user, notification, context=None):
        """
        Send the notification to the specified user using this notifier method.

        returns Boolean according to success of delivery.
        """

        notifierobject = self.notifierclass(notification)
        sent_success = notifierobject.send(user, context)

        SentNotification.objects.create(user=user, notification=notification,
            notifier=self, success=sent_success)

        return sent_success


class Notification(BaseModel):
    """
    Entries for various notifications
    """
    name = models.CharField(max_length=200, unique=True, db_index=True)
    display_name = models.CharField(max_length=200)

    # This field determines whether the notification is to be shown
    #   to users or it is private and only set by code.
    # This only affects UI, the notification is otherwise enabled
    #   and usable in all ways.
    public = models.BooleanField(default=True)

    # user should have all the permissions selected here to be able to change
    # the user prefs for this notification or see it in the UI
    permissions = models.ManyToManyField(Permission, blank=True)

    # These are the notifier delivery methods that are allowed for this type of
    # notification
    notifiers = models.ManyToManyField(Notifier, blank=True)

    objects = managers.NotificationManager()

    def __unicode__(self):
        return self.name

    def check_perms(self, user):
        # Need an iterable with permission strings to check using has_perms.
        # This makes it possible to take advantage of the cache.
        perm_list = set(
            ["%s.%s" % (p.content_type.app_label, p.codename) for p in self.permissions.select_related()]
        )

        if not user.has_perms(perm_list):
            return False
        return True

    def get_notifiers(self, user):
        """
        Returns notifiers after checking `User` and `Group` preferences
        as well as `notifier.enabled` flag.
        """
        user_settings = self.usernotify_set.filter(user=user)
        group_filter = Q()
        for group in user.groups.all():
            group_filter = Q(group_filter | Q(group=group))

        group_settings = self.groupnotify_set.filter(group_filter)

        notifiers = self.notifiers.filter(enabled=True)

        remove_notifiers = []
        for notifier in notifiers:
            try:
                usernotify = user_settings.get(notifier=notifier)
            except UserNotify.DoesNotExist:
                try:
                    group_settings.get(notifier=notifier, notify=True)
                except GroupNotify.DoesNotExist:
                    remove_notifiers.append(notifier.id)
            else:
                if not usernotify.notify:
                    remove_notifiers.append(notifier.id)

        return notifiers.exclude(id__in=remove_notifiers)

    def get_user_prefs(self, user):
        """
        Return a dictionary of all available notifier delivery methods with True
        or False values depending on preferences.
        """
        all_notifiers = self.notifiers.filter(enabled=True)
        selected_notifiers = self.get_notifiers(user)

        notifier_dict = dict(zip(all_notifiers, [False] * len(all_notifiers)))
        for notifier in all_notifiers:
            if notifier in selected_notifiers:
                notifier_dict[notifier] = True

        return notifier_dict

    def update_user_prefs(self, user, prefs_dict):
        """
        Update or create a `UserNotify` instance as required
        """
        for notifier, value in prefs_dict.items():
            try:
                userpref = self.usernotify_set.get(
                    user=user,
                    notifier=notifier)
            except UserNotify.DoesNotExist:
                UserNotify.objects.create(
                    user=user,
                    notification=self,
                    notifier=notifier,
                    notify=value)
                return 'created'
            else:
                if userpref.notify != value:
                    userpref.notify = value
                    userpref.save()
                    return 'updated'

    def send(self, users, context=None):
        if not isinstance(users, Iterable):
            users = [users]

        for user in users:
            for notifier in self.get_notifiers(user):
                notifier.send(user, self, context)


class GroupNotify(BaseModel):
    """
    Per group notification settings

    If notification is not explicitly set to True, then default to False.
    """
    group = models.ForeignKey(Group)
    notification = models.ForeignKey(Notification)
    notifier = models.ForeignKey(Notifier)
    notify = models.BooleanField(default=True)

    class Meta:
        unique_together = ('group', 'notification', 'notifier')

    def __unicode__(self):
        return '%s:%s:%s' % (self.group, self.notification, self.notifier)


class UserNotify(BaseModel):
    """
    Per user notification settings

    Supercedes group setting.
    If notification preference is not explicitly set, then use group setting.
    """
    user = models.ForeignKey(User)
    notification = models.ForeignKey(Notification)
    notifier = models.ForeignKey(Notifier)
    notify = models.BooleanField(default=True)

    objects = managers.UserNotifyManager()

    class Meta:
        unique_together = ('user', 'notification', 'notifier')

    def __unicode__(self):
        return '%s:%s:%s' % (self.user, self.notification, self.notifier)

    def save(self, *args, **kwargs):
        if not self.notification.check_perms(self.user):
            raise PermissionDenied
        super(UserNotify, self).save(*args, **kwargs)


class SentNotification(BaseModel):
    """
    Record of every notification sent.
    """
    user = models.ForeignKey(User)
    notification = models.ForeignKey(Notification)
    notifier = models.ForeignKey(Notifier)
    success = models.BooleanField()

    def __unicode__(self):
        return '%s:%s:%s' % (self.user, self.notification, self.notifier)


###############################################################################
## Signal Recievers
###############################################################################
@receiver(pre_delete, sender=Notifier,
    dispatch_uid='notifier.models.notifier_pre_delete')
def notifier_pre_delete(sender, instance, **kwargs):
    raise PermissionDenied(
        'Cannot delete notifier %s. Remove from settings.' % instance.name)
