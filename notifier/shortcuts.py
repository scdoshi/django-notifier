###############################################################################
## Imports
###############################################################################
# Python
from collections import Iterable

# Django
from django.contrib.auth.models import Permission
from django.db.models.query import QuerySet

# User
from notifier.models import Notification, Backend, UserPrefs


###############################################################################
## Code
###############################################################################
def create_notification(name, display_name=None,
        permissions=None, backends=None, public=True):

    if not display_name:
        display_name = name

    if backends:
        backends = _get_backend_queryset(backends)
    else:
        backends = Backend.objects.filter(enabled=True)

    if permissions:
        permissions = _get_permission_queryset(permissions)
    else:
        permissions = []

    try:
        n = Notification.objects.get(name=name)
    except Notification.DoesNotExist:
        n = Notification.objects.create(name=name, display_name=display_name,
            public=public)
        n.permissions.add(*permissions)
        n.backends.add(*backends)
    else:
        n.name = name
        n.display_name = display_name
        n.public = public
        n.permissions = permissions
        n.backends = backends
        n.save()

    return n


def send_notification(name, users, context=None):
    try:
        notification = Notification.objects.get(name=name)
    except Notification.DoesNotExist:
        # write debug message
        pass
    else:
        notification.send(users, context)


def clear_preferences(users):
    return UserPrefs.objects.remove_user_prefs(users)


def _get_permission_queryset(permissions):
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


def _get_backend_queryset(backends):
    if (backends and
            not isinstance(backends, QuerySet)):
        if isinstance(backends, Backend):
            backends = [backends]
        else:
            if isinstance(backends, basestring):
                backends = [backends]
            elif isinstance(backends, Iterable):
                if not all(isinstance(x, basestring) for x in backends):
                    raise TypeError
            else:
                raise TypeError
            backends = Backend.objects.filter(name__in=backends)

    return backends
