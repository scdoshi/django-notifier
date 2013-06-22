"""
django-notifier is an app to manage notification preferences and permissions
per user and per group.

To send a notification:
notifier.create_notification('test-notif')
notifier.send('test-notif', [user1, user2, ..])

"""

###############################################################################
## Imports
###############################################################################
# Python
from collections import Iterable

# Django
from django.contrib.auth.models import Permission
from django.db.models.query import QuerySet

# User
from notifier.models import Notification, Notifier, UserNotify


###############################################################################
## Code
###############################################################################
def send(name, users, context=None):
    try:
        notification = Notification.objects.get(name=name)
    except Notification.DoesNotExist:
        # write debug message
        pass
    else:
        notification.send(users, context)


def clear_preferences(users):
    return UserNotify.objects.remove_user_prefs(users)


def create_notification(name, display_name=None,
        permissions=None, notifiers=None, public=True):

    if not display_name:
        display_name = name

    if not notifiers:
        notifiers = Notifier.objects.filter(enabled=True)

    if permissions:
        permissions = get_permission_queryset(permissions)
    else:
        permissions = []

    try:
        n = Notification.objects.get(name=name)
    except Notification.DoesNotExist:
        n = Notification.objects.create(name=name, display_name=display_name,
            public=public)
        n.permissions.add(*permissions)
        n.notifiers.add(*notifiers)
    else:
        n.name = name
        n.display_name = display_name
        n.public = public
        n.permissions = permissions
        n.notifiers = notifiers
        n.save()

    return n


def get_permission_queryset(permissions):
    if (permissions and
            not isinstance(permissions, QuerySet)):
        if isinstance(permissions, Permission):
            permissions = [permissions]
        else:
            if isinstance(permissions, basestring):
                permissions = [permissions]
            elif isinstance(permissions, Iterable):
                if not all(isinstance(x, basestring) for x in permissions):
                    raise TypeError
            else:
                raise TypeError
            permissions = Permission.objects.filter(codename__in=permissions)

    return permissions
