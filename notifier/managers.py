###############################################################################
## Imports
###############################################################################
# Python
from collections import Iterable

# Django
from django.db import models
from django.db.models import Q


###############################################################################
## Managers
###############################################################################
class NotificationManager(models.Manager):
    def get_user_notifications(self, user):
        ret_list = []
        for notification in self.filter(public=True):
            if notification.deliverymethods.all() and notification.check_perms(user):
                ret_list.append(notification)
        return ret_list

    def get_user_prefs(self, user):
        return_dict = {}
        for notification in self.filter(public=True):
            if notification.check_perms(user):
                return_dict[notification] = notification.get_user_prefs(user)
        return return_dict

    def update_user_prefs(self, user, update_dict):
        created = 0
        updated = 0
        for notification, prefs in update_dict.items():
            ret_value = notification.update_user_prefs(user, prefs)
            if ret_value == 'created':
                created += 1
            elif ret_value == 'updated':
                updated += 1
        return {'created': created, 'updated': updated}


class UserPrefsManager(models.Manager):
    def remove_user_prefs(self, users):
        """
        Set to default by removing all User specific notification prefs.
        """
        if not isinstance(users, Iterable):
            users = [users]

        user_filter = Q()
        for user in users:
            user_filter = Q(user_filter | Q(user=user))

        self.filter(user_filter).delete()
