###############################################################################
## Imports
###############################################################################
# Python
from collections import Iterable

# Django
from django.contrib.auth.models import Group, Permission, User
from django.db.models.query import QuerySet

# User
from notifier.models import Notification, Backend, UserPrefs


###############################################################################
## Code
###############################################################################
def create_notification(name, display_name=None,
        permissions=None, backends=None, public=True):
    """
    Arguments

        :name: notification name, unique (string)
        :display_name: notification display name, can be non-unique (string)
        :permissions: list of permission names or objects
        :backends: list of backend names or objects
        :public: (boolean)

    Returns
        Notification object
    """

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
    """
    Arguments

        :name: notification name (string)
        :users: user object or list of user objects
        :context: additional context for notification templates (dict)

    Returns

        None
    """
    notification = Notification.objects.get(name=name)
    return notification.send(users, context)


def update_preferences(name, user, prefs_dict):
    """
    Arguments

        :name: notification name (string)
        :user: user or group object
        :prefs_dict: dict with backend obj or name as key with a boolean value.

            e.g. {'email': True, 'sms': False}, {email_backend_obj: True, sms_backend_obj: False}

    Returns

        dict with backend names that were created or updated. values that do not require change are skipped

        e.g. {'email': 'created', 'sms': updated}
    """
    notification = Notification.objects.get(name=name)

    if isinstance(user, User):
        return notification.update_user_prefs(user, prefs_dict)
    elif isinstance(user, Group):
        return notification.update_group_prefs(user, prefs_dict)


def clear_preferences(users):
    """
    Arguments

        :users: user object or list of user object

    Returns

        None
    """
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
