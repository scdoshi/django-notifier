"""
django-notifier is an app to manage notification preferences and permissions
per user and per group.

To send a notification:

from notifier.shortcuts import create_notification, send_notification
create_notification('test-notif')
send_notification('test-notif', [user1, user2, ..])

"""

VERSION = (0, 6, 0, 'f')  # following PEP 386
# VERSION = (0, 5, 2, "a", "1")


def get_version(short=False):
    version = "%s.%s" % (VERSION[0], VERSION[1])
    if short:
        return version
    if VERSION[2]:
        version = "%s.%s" % (version, VERSION[2])
    if VERSION[3] != "f":
        version = "%s%s%s" % (version, VERSION[3], VERSION[4])
    return version
