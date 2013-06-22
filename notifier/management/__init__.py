###############################################################################
## Imports
###############################################################################
# Python
from importlib import import_module

# Django
from django.conf import settings
from django.db.models.signals import post_syncdb

# External
try:
    from south.signals import post_migrate
    South = True
except ImportError:
    South = False

# User
from notifier.models import Notifier
from notifier import settings as notifier_settings


###############################################################################
## Code
###############################################################################
def create_backends(app, **kwargs):
    """
    Creates/Updates Backend objects based on NOTIFIER_BACKENDS settings.

    All values except `enabled` are derived from the Backend class and
    not suppossed to be modified by user. They will be over-written on restart.
    """

    if not app == 'notifier':
        return

    for backend in notifier_settings.BACKEND_CLASSES:
        try:
            notifier = Notifier.objects.get(name=backend.name)
        except Notifier.DoesNotExist:
            notifier = Notifier()
            notifier.enabled = True
        finally:
            notifier.display_name = backend.display_name
            notifier.name = backend.name
            notifier.description = backend.description
            notifier.klass = ('.'.join([backend.__module__, backend.__name__]))
            notifier.save()


def create_notifications(app, **kwargs):
    """
    Creates all the notifications specified in notifiers.py for all apps
    in INSTALLED_APPS
    """

    if not app == 'notifier':
        return

    for installed_app in settings.INSTALLED_APPS:
        try:
            import_module(installed_app + '.notifiers')
        except ImportError:
            pass


if South:
    post_migrate.connect(create_backends,
        dispatch_uid="notifier.management.create_backends")
    post_migrate.connect(create_notifications,
        dispatch_uid="notifier.management.create_notifications")
else:
    post_syncdb.connect(create_backends,
        dispatch_uid="notifier.management.create_backends")
    post_syncdb.connect(create_notifications,
        dispatch_uid="notifier.management.create_notifications")
